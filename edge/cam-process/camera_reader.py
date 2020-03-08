import sys
import pickle
import time
import logging

import requests


logging.getLogger().setLevel(logging.INFO)

EDGE_MASTER_SERVICE = 'http://localhost:5000/process-image'


def initialize_webcam(cam_id):
    video_capture = None

    # TODO: initialize video_capture

    return video_capture


def fetch_image(video_capture):
    # TODO: detect with camera
    pass


def main():
    cam_id = sys.argv[1]
    video_capture = initialize_webcam(cam_id)

    while True:
        img = fetch_image(video_capture)

        resp = requests.post(EDGE_MASTER_SERVICE, json={
            'cam_id': cam_id,
            'image': pickle.dumps(img, protocol=pickle.HIGHEST_PROTOCOL).decode('latin-1')
        })

        logging.info("Status: %d, response: %s", resp.status_code, resp.text.strip())

        time.sleep(5)


if __name__ == '__main__':
    main()
