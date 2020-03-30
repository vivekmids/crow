import os
import uuid
import time

from flask import Flask, jsonify, request
import requests

from starting_scripts import CAM_PROC_STATUSES, start_camera_processes, start_inference_service, start_deterrent_service


def env_or_default(name, default):
    return os.environ[name] if name in os.environ else default


INFERENCE_SERVICE = env_or_default('INFERENCE_SERVICE', 'http://localhost:5050')
DETERRENT_SERVICE = env_or_default('DETERRENT_SERVICE', 'http://localhost:5100')
CLOUD_ENDPOINT = env_or_default('CLOUD_ENDPOINT', 'http://169.63.11.147:8000/api/infer')
DEVICE_ID = env_or_default('DEVICE_ID', "edge-device-" + str(uuid.uuid4())[:5])

# service to keep track of these bad bois
app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_running_apps():
    return jsonify({
        cam_id: {
            'process': stuff['proc'].pid,
            'last_status': stuff['last_status']
        }
        for cam_id, stuff in CAM_PROC_STATUSES.items()
    })


@app.route('/process-image', methods=['POST'])
def update_status():
    inference_response = None
    deterrent_response = None

    # Step 1 - update status
    data = request.get_json(force=True)
    cam_id = int(data.pop('cam_id'))
    CAM_PROC_STATUSES[cam_id]['last_status'] = data

    # Step 2 - get inference
    resp = requests.post(INFERENCE_SERVICE, json={
        'image': data['image']
    })

    if resp.status_code != 200:
        # TODO: What do we do when we have a failure though?
        pass
    else:
        inference_response = resp.json()

    if inference_response['found_something']:
        # Step 3 - deploy a deterrent maybe
        resp = requests.post(DETERRENT_SERVICE, json={
            'detected_animals': inference_response['detected_animals'],
        })

        if resp.status_code != 200:
            # TODO: handle error case
            pass
        else:
            deterrent_response = resp.json()

        # TODO: post data to cloud
        if CLOUD_ENDPOINT:
            resp = requests.post(CLOUD_ENDPOINT, json={
                'updated': True,
                'device_id': DEVICE_ID,
                'cam_id': cam_id,
                'image': data['image'],
                'inference_response': inference_response,
                'deterrent_response': deterrent_response
            })
            print('After sending image to cloud ' + str(resp.text))

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
    start_deterrent_service()

    # kick off all camera processes
    start_camera_processes()

    # this service needs to start finally
    app.run('0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
