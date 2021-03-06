import pickle
import logging
import io
import random
import string
import base64
from datetime import datetime
from collections import defaultdict

import numpy as np
import boto3
import psycopg2
import pytz
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


def get_summary_stats(conn, tz):
    """Here we should return a list of images the customer has already seen
    """
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute(f"""
        SELECT
            COUNT(*) AS totalCount,
            MIN(date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}') AS minFromDate,
            MAX(date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}') AS maxToDate
        FROM crow
    """)
    row = [dict(item) for item in cur][0]
    return {
        'minFromDate': row['minfromdate'],
        'maxToDate': row['maxtodate'],
        'totalCount': row['totalcount'],
    }


def get_ui_state(conn, min_date, max_date, tz):
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute(f"""
        SELECT
            COUNT(*) AS filteredCount
        FROM crow
        WHERE DATE(date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}') >= %s
            AND DATE(date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}') <= %s
    """, (min_date, max_date))
    filtered_counts = {
        'filteredCount': [dict(item) for item in cur][0]['filteredcount']
    }

    cur.execute(f"""
        SELECT DISTINCT
            detected_animals
        FROM crow
        WHERE DATE(date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}') >= %s
            AND DATE(date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}') <= %s
    """, (min_date, max_date))
    detected_animals = [item['detected_animals'] for item in cur]

    return {
        **filtered_counts,
        "filteredPests": detected_animals
    }


def get_pest_data(conn, min_date, max_date, tz):
    cur = conn.cursor(cursor_factory=DictCursor)

    cur.execute(f"""
        SELECT
            DATE(date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}') AS date,
            detected_animals,
            date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}' AS date_time
        FROM crow
        WHERE DATE(date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}') >= %s
            AND DATE(date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}') <= %s
    """, (min_date, max_date))
    date_animal_times = defaultdict(lambda: defaultdict(list))
    for item in cur.fetchall():
        date_animal_times[str(item['date'])][item['detected_animals']].append(str(item['date_time']))

    return date_animal_times


def get_image_info(s3_client, conn, min_date, max_date, tz, num_rows=DEFAULT_API_ROW_COUNT, fetch_images=False):
    cur = conn.cursor(cursor_factory=DictCursor)

    postgres_select_query = f"""
    SELECT
        rowid,
        device_id,
        cam_id,
        date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}' AS date_time,
        detected_animals,
        deterrent_type,
        soundfile_name,
        key_name,
        bucket_name,
        updated,
        found_something
    FROM crow
    WHERE DATE(date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}') >= %s
        AND DATE(date_time AT TIME ZONE 'UTC' AT TIME ZONE '{tz}') <= %s
    ORDER BY rowid DESC
    LIMIT {num_rows}
    """
    cur.execute(postgres_select_query, (min_date, max_date))

    rows = [
        {
            **row,
            'date_time': pytz.timezone(tz).localize(row['date_time']).isoformat(' '),
        }
        for row in cur
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
        tz = request.args.get('tz', 'America/New_York')
        db_summary = get_summary_stats(conn, tz=tz)

        min_date = request.args.get('fromDate', db_summary['minFromDate'])
        max_date = request.args.get('toDate', db_summary['maxToDate'])

        ui_state = {
            **db_summary,
            **get_ui_state(conn, min_date=min_date, max_date=max_date, tz=tz)
        }
        pest_data = get_pest_data(conn, min_date=min_date, max_date=max_date, tz=tz)
        images = get_image_info(
            s3_client,
            conn,
            min_date=min_date,
            max_date=max_date,
            tz=tz,
            num_rows=request.args.get('rows', DEFAULT_API_ROW_COUNT),
            fetch_images='fetch_images' in request.args
        )

        return jsonify({
            'uiState': ui_state,
            'pestData': pest_data,
            'imageList': images
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
