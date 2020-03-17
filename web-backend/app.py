import pickle
import logging
import boto3
import pprint as pp
#import psycopg2


from flask import Flask, request, jsonify
from PIL import Image


app = Flask(__name__)

endpoint = 'https://s3.us.cloud-object-storage.appdomain.cloud'
s3 = boto3.resource('s3',endpoint_url=endpoint)



def get_images():
    """Here we should return a list of images the customer has already seen
    """
    return []


def save_image(payload,file_name, bucket='w210-bucket', object_name=None):
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
    #convert numpy array to RGB image and store it as PNG/jpg
    image ='' #numpy array of image
    img = Image.fromarray(image)
    file_name= img.save(file_name+'.png')

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3',endpoint_url=endpoint)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        logging.error(e)
        return False
    return True

    #return {}


# def insert_to_db(bucket='w210-bucket'):
#     device_id=''
#     cam_id=''
#     detterent_type=''
#     date_time=''
#     soundfile_name=''
#
#     for bucket in s3.buckets.all():
#         for key in bucket.objects.all():
#             print(key.key)
#             print(key)
#
#     try:
#         conn = psycopg2.connect(host="169.63.11.147",database="postgres",user="postgres",password="scarecrow",sslmode="disable")
#         cur = conn.cursor()
#
#         postgres_insert_query ="""insert into crow(device_id,cam_id,detterent_type,date_time,soundfile_name,key_name,bucket_name) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
#         record_to_insert = (device_id,cam_id,detterent_type,date_time,soundfile_name,key,bucket)
#         cur.execute(postgres_insert_query,record_to_insert)
#         conn.commit()
#         count = cur.rowcount
#         print (count, "Record inserted successfully into crow table")
#
#     except (Exception, psycopg2.Error) as error :
#         if(conn):
#             print("Failed to insert record into mobile table", error)
#
#     finally:
#         #closing database connection.
#         if(conn):
#             cur.close()
#             conn.close()
#             print("PostgreSQL connection is closed")


@app.route('/', methods=['GET', 'POST'])
def handle_route():
    if request.method == 'GET':
        return jsonify(get_images())
    elif request.method == 'POST':
        payload = request.get_json(force=True)
        payload['image'] = pickle.loads(payload['image'].encode('latin-1'))
        return jsonify(save_image(payload,file_name, bucket='w210-bucket'))


def main():
    app.run('0.0.0.0', 8000)


if __name__ == '__main__':
    main()
