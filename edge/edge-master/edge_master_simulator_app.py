import os
import uuid
import time
import logging
import pickle

from flask import Flask, jsonify, request
from PIL import Image
import numpy as np
import requests

from starting_scripts import start_inference_service, start_deterrent_simulator_service


def env_or_default(name, default):
    return os.environ[name] if name in os.environ else default


INFERENCE_SERVICE = env_or_default('INFERENCE_SERVICE', 'http://localhost:5050')
DETERRENT_SERVICE = env_or_default('DETERRENT_SERVICE', 'http://localhost:5100')
CLOUD_ENDPOINT = env_or_default('CLOUD_ENDPOINT', 'http://169.63.11.147:8000/api/inferences/')
DEVICE_ID = env_or_default('DEVICE_ID', "edge-device-simulator-" + str(uuid.uuid4())[:5])

# sim constants
DEFAULT_CAM_ID = env_or_default('CAM_ID', 0)
SAMPLE_PESTS_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# service to keep track of these bad bois
app = Flask(__name__)


@app.route('/simulator/process-image/', methods=['GET'])
def update_status():
    inference_response = None
    deterrent_response = None

    # Step 1 - get params
    image_id = request.args.get('image_id')
    if not image_id:
        raise Exception(f"Unable to find image_id {image_id}")

    cam_id = DEFAULT_CAM_ID
    save_to_cloud = request.args.get('save_to_cloud', False)

    # Step 2 - get inference
    image = Image.open(f"{SAMPLE_PESTS_PATH}/web-frontend/assets/images/sample_pests/pest-{image_id}.jpg")
    image = image.resize(size=(299, 299))
    image = np.array(image).reshape((1, 299, 299, 3))
    pickled_img = pickle.dumps(image, protocol=pickle.HIGHEST_PROTOCOL).decode('latin-1')

    resp = requests.post(INFERENCE_SERVICE, json={
        'image': pickled_img
    })

    if resp.status_code != 200:
        # TODO: What do we do when we have a failure though?
        pass
    else:
        inference_response = resp.json()

    if inference_response and inference_response['found_something']:
        # Step 3 - deploy a deterrent maybe
        resp = requests.post(DETERRENT_SERVICE, json={
            'detected_animals': inference_response['detected_animals'],
        })

        if resp.status_code != 200:
            # TODO: handle error case
            pass
        else:
            deterrent_response = resp.json()

        if save_to_cloud and CLOUD_ENDPOINT:
            resp = requests.post(CLOUD_ENDPOINT, json={
                'updated': True,
                'device_id': DEVICE_ID,
                'cam_id': cam_id,
                'image': pickled_img,
                'inference_response': inference_response,
                'deterrent_response': deterrent_response
            })
            logging.info('After sending image to cloud ' + str(resp.text))

    return jsonify({
        'updated': True,
        'device_id': DEVICE_ID,
        'cam_id': cam_id,
        'inference_response': inference_response,
        'deterrent_response': deterrent_response
    })


def main():
    # kick off all supporting services first
    start_inference_service()
    time.sleep(10)
    start_deterrent_simulator_service()

    # this service needs to start finally
    app.run('0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
