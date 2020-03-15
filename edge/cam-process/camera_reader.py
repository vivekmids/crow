import sys
import pickle
import time
import logging
import cv2

import requests


logging.getLogger().setLevel(logging.INFO)

EDGE_MASTER_SERVICE = 'http://localhost:5000/process-image'

def main():
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
            ret, frame = cap.read()
            if ret:
                try:
                    resp = requests.post(EDGE_MASTER_SERVICE, json={
                    'cam_id': cam_id,
                    'image': pickle.dumps(img, protocol=pickle.HIGHEST_PROTOCOL).decode('latin-1')
                    })
                    logging.info("Status: %d, response: %s", resp.status_code, resp.text.strip())

                except:
                    logging.error("Camera %d failed to publish image to Edge Master Service", cam_id)

                cv2.imshow("Crow", frame)
            else:
                print ("Error reading capture device")
                break
            k = cv2.waitKey(10) & 0xFF
            if k == 27:
                break
    else:
        logging.error("Failed to open capture camera: %d", cam_id)

if __name__ == '__main__':
    main()
