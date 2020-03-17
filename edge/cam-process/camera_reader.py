import sys
import pickle
import time
import logging
import cv2

import requests


logging.getLogger().setLevel(logging.INFO)

EDGE_MASTER_SERVICE = 'http://localhost:5000/process-image'

def main():
    DEBUG = True
    try:
        cam_id = int(sys.argv[1])
    except:
        cam_id = 0
        logging.warning('No camera specified. Defaulting to ' + str(cam_id))

    cap = cv2.VideoCapture(cam_id)
# if capture failed to open, try again
    if not cap.isOpened():
        cap.open(cam_id)

    if cap.isOpened():
        while True:
            ret, rawframe = cap.read()
            if ret:
                try:
                    frame = cv2.resize(rawframe, (299,299))
                    frame = frame.reshape(1,299,299,3)  
                    resp = requests.post(EDGE_MASTER_SERVICE, json={
                    'cam_id': cam_id,
                    'image': pickle.dumps(frame, protocol=pickle.HIGHEST_PROTOCOL).decode('latin-1')
                    })
                    logging.info("Status: %d, response: %s", resp.status_code, resp.text.strip())

                except Exception as e:
                    logging.error("Camera %d failed to publish image to Edge Master Service", cam_id)
                    raise e

                if DEBUG:
                    cv2.imshow("Crow", rawframe)
            else:
                print ("Error reading capture device")
                break
            cv2.waitKey(10)
    else:
        logging.error("Failed to open capture camera: %d", cam_id)

if __name__ == '__main__':
    main()
