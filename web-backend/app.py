import pickle
import logging
import io
import random
import string
import base64
from datetime import datetime

import numpy as np
import boto3
import psycopg2
from psycopg2.extras import DictCursor
from flask import Flask, request, jsonify
from PIL import Image

S3_ENDPOINT = 'https://s3.us.cloud-object-storage.appdomain.cloud'
POSTGRES_HOST = "169.63.11.147"
POSTGRES_DATABASE = "postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "scarecrow"

DEFAULT_API_ROW_COUNT = 10

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(host=POSTGRES_HOST, database=POSTGRES_DATABASE,
                            user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                            sslmode="disable")


def get_s3_client():
    return boto3.resource('s3', endpoint_url=S3_ENDPOINT)


def rand_str_generator(size, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))


def get_summary_stats(conn):
    """Here we should return a list of images the customer has already seen
    """
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("""
        SELECT
            COUNT(*) AS total_count,
            MAX(date_time) AS max_date_time,
            MIN(date_time) AS min_date_time,
            COUNT(DISTINCT detected_animals) AS num_distinct_animals,
            COUNT(CASE WHEN deterrent_type = 'sound' THEN 1 ELSE 0 END) AS count_sound_deployed,
            COUNT(CASE WHEN deterrent_type = 'light' THEN 1 ELSE 0 END) AS count_light_deployed
        FROM crow
    """)
    summaries = [dict(item) for item in cur][0]

    cur.execute("""
        SELECT
            detected_animals,
            COUNT(*) AS count
        FROM crow
        GROUP BY detected_animals
    """)
    counts_by_detected_animal = {item['detected_animals']: item['count'] for item in cur}

    return {
        'summary_stats': summaries,
        'animal_counts': counts_by_detected_animal
    }


def get_image_info(s3_client, conn, num_rows=DEFAULT_API_ROW_COUNT, fetch_images=False):
    cur = conn.cursor()

    postgres_select_query = f"""
    SELECT * FROM crow
    ORDER BY rowid DESC
    LIMIT {num_rows}
    """
    cur.execute(postgres_select_query)

    rows = [
        dict((cur.description[i][0], value) for i, value in enumerate(row))
        for row in cur.fetchall()
    ]
    cur.close()

    # fetch image data for each row
    if fetch_images:
        for row in rows:
            row['base64_encoded_image'] = None
            bucket = row['bucket_name']
            key_name = row['key_name']

            try:
                img_obj = s3_client.Bucket(bucket).Object(key_name)
                img_bytes = img_obj.get()['Body'].read()
                row['base64_encoded_image'] = base64.b64encode(img_bytes).decode('utf8')
            except Exception as e:
                logging.error(f"Unable to fetch image from s3: {key_name}", e)

    return rows


def save_image(s3_client, image_array, device_id, cam_id, detected_animals, time_stamp):
    bucket = 'w210-bucket'
    object_name = f'image/{device_id}/{cam_id}/{detected_animals}/{time_stamp}_{rand_str_generator(3)}.jpeg'
    object_name = object_name.replace(' ', '_')

    img = image_array.reshape(299, 299, 3)
    img = np.array(img)
    img = Image.fromarray(img)

    bytes_file = io.BytesIO()
    img.save(bytes_file, format="jpeg")
    logging.error(len(bytes_file.getvalue()))

    # Upload the file
    try:
        s3_client.Bucket(bucket).put_object(
            Key=object_name,
            Body=bytes_file.getvalue()
        )
    except Exception as e:
        logging.error(e)
        return None

    return object_name


def insert_to_db(conn, device_id, cam_id, deterrent_type, date_time, soundfile_name, key, detected_animals, updated,
                 found_something, bucket='w210-bucket'):
    """Here we save the images. The input data will be:
            {
                'updated': True,
                'device_id': device_id,
                'cam_id': cam_id,
                'image': numpy array of image RGB values,
                'inference_response': inference_response,
                'deterrent_response': deterrent_response
            }

    return:
        Any useful metadata that will be useful for the edge device
        We will simply be logging this data so it doesn't really matter
    """
    try:
        cur = conn.cursor()

        postgres_insert_query = """
        INSERT INTO crow (device_id, cam_id, deterrent_type, date_time, soundfile_name, key_name, detected_animals,
                          updated, found_something, bucket_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING rowid
        """
        record_to_insert = (device_id, cam_id, deterrent_type, date_time, soundfile_name, key, detected_animals,
                            updated, found_something, bucket)
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        row_id = cur.fetchone()[0]

        logging.info(f"Saved row_id to database: {row_id}")

        return row_id
    except (Exception, psycopg2.Error) as error:
        if conn:
            logging.error("Failed to insert record into mobile table", error)
            raise error
    finally:
        # closing database connection.
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")


@app.route('/api/inferences/', methods=['GET', 'POST'])
def api_data():
    s3_client = get_s3_client()
    conn = get_conn()

    if request.method == 'GET':
        db_summary = get_summary_stats(conn)
        images = get_image_info(
            s3_client,
            conn,
            request.args.get('rows', DEFAULT_API_ROW_COUNT),
            'fetch_images' in request.args
        )

        return jsonify({
            **db_summary,
            'images': images
        })
    elif request.method == 'POST':
        payload = request.get_json(force=True)
        payload['image'] = pickle.loads(payload['image'].encode('latin-1'))

        time_stamp = datetime.now()
        detected_animals = payload['inference_response']['detected_animals']
        cam_id = payload['cam_id']
        device_id = payload['device_id']
        image = payload['image']

        image_key = save_image(s3_client, image, device_id, cam_id, detected_animals, time_stamp)
        db_row_id = insert_to_db(
            conn,
            device_id,
            cam_id,
            payload['deterrent_response']['deployed_deterrent']['type'],
            time_stamp,
            payload['deterrent_response']['deployed_deterrent'].get('played_sound', None),  # default None
            image_key,
            detected_animals,
            payload['updated'],
            payload['inference_response']['found_something']
        )

        return jsonify({
            "image": image_key,
            "db_row_id": db_row_id
        })


def main():
    app.run('0.0.0.0', 8000, debug=True)


if __name__ == '__main__':
    main()
