import pickle
import logging
import boto3
import psycopg2
import json
import numpy as np
import os
from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)

endpoint = 'https://s3.us.cloud-object-storage.appdomain.cloud'
s3 = boto3.resource('s3',endpoint_url=endpoint)


def get_images():
    """Here we should return a list of images the customer has already seen
    """
    stat_summary = get_image_info()
    stat_summary = json.dumps(stat_summary, indent=4, sort_keys=True, default=str)
    print(stat_summary)
    return stat_summary

def get_image_info(one=False):
    conn = psycopg2.connect(host="169.63.11.147", database="postgres", user="postgres", password="scarecrow",
                            sslmode="disable")
    cur = conn.cursor()

    postgres_select_query = """select * from crow"""
    cur.execute(postgres_select_query)
    r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    return (r[0] if r else None) if one else r


def save_image(image_array):

    bucket = 'w210-bucket'
    object_name = None
    #convert numpy array to PNG/jpg
    #print(image_array.shape)
    logging.error(image_array.shape)
    img = image_array.resize(size=(299, 299))
    img = np.array(img)
    img = Image.fromarray(img)
    file_name ='image.jpeg'
    img.save(file_name)
    cwd = os.getcwd()
    file = cwd +'/'+file_name
    print('in save_image before calling s3')

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file

    # Upload the file
    s3_client = boto3.client('s3',endpoint_url=endpoint)
    print('s3 client instantiated')
    try:
        response = s3_client.upload_file(file, bucket,object_name)
    except Exception as e:
        logging.error(e)
        return False
    return True

    #return {}


def insert_to_db(DEVICE_ID,cam_id,detterent_type,date_time,soundfile_name,key,detected_animals,updated,found_something,bucket='w210-bucket'):
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


   for bucket in s3.buckets.all():
    for key in bucket.objects.all():
        print(key.key)
        print(key)

   try:
       conn = psycopg2.connect(host="169.63.11.147",database="postgres",user="postgres",password="scarecrow",sslmode="disable")
       cur = conn.cursor()

       postgres_insert_query ="""insert into crow(device_id,cam_id,detterent_type,date_time,soundfile_name,key_name,detected_animals,updated,found_something,bucket_name) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"""
       record_to_insert = (DEVICE_ID,cam_id,detterent_type,date_time,soundfile_name,key,detected_animals,updated,found_something,bucket)
       cur.execute(postgres_insert_query,record_to_insert)
       conn.commit()
       count = cur.rowcount
       print (count, "Record inserted successfully into crow table")

   except (Exception, psycopg2.Error) as error :
       if(conn):
           print("Failed to insert record into mobile table", error)

   finally:
       #closing database connection.
       if(conn):
           cur.close()
           conn.close()
           print("PostgreSQL connection is closed")


@app.route('/', methods=['GET', 'POST'])
def handle_route():
    print("inside handle")
    if request.method == 'GET':
        return jsonify(get_images())
    elif request.method == 'POST':
        print('inside POST')
        payload = request.get_json(force=True)
        print("here")
        payload['image'] = pickle.loads(payload['image'].encode('latin-1'))
        print("here1")
        return jsonify({
        "image": save_image(payload['image']),
        "db_row_id": insert_to_db(payload['DEVICE_ID','cam_id','detterent_type','date_time','soundfile_name','key','detected_animals','updated','found_something','bucket_name'])
        })

@app.route('/xyz', methods=['GET', 'POST'])
def test():
    print("inside test")
    return jsonify([])


def main():
    app.run('0.0.0.0', 8000,debug=True)


if __name__ == '__main__':
    main()
