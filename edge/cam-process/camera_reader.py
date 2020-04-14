import sys
import pickle
import time
import logging
import cv2
import numpy as np

import requests


logging.getLogger().setLevel(logging.INFO)

EDGE_MASTER_SERVICE = 'http://localhost:5000/process-image'
DEBUG = True
SKIP = 5 #Number of frames to skip between 2 frames processed. 

def distMap(frame1, frame2):
    """outputs distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = (np.abs(diff32[:,:,0]) + np.abs(diff32[:,:,1]) + np.abs(diff32[:,:,2]))/765
    dist = np.uint8(norm32*255)
    return dist

def motion(frame1, frame2, sdThresh=10):
    dist = distMap(frame1, frame2)

    mod = cv2.GaussianBlur(dist, (9,9), 0)

    _, thresh = cv2.threshold(mod, 100, 255, 0)

    _, stDev = cv2.meanStdDev(mod)

    if DEBUG:
        cv2.imshow('dist', mod)
        cv2.putText(frame2, "Standard Deviation - {}".format(round(stDev[0][0],0)), (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 1, cv2.LINE_AA)
    if stDev > sdThresh:
        
        return True
    else:
        return False

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
        cap.read()
        cap.read()
        _, frame1 = cap.read()
        _, frame2 = cap.read()
        while True:
            if motion(frame1, frame2):
                logging.info("Motion detected on " + str(cam_id));
                try:
                    frame = cv2.resize(frame2, (299, 299))
                    #frame = cv2.resize(frame2, (149, 149))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = frame.reshape(1, 299, 299, 3)
                    #frame = frame.reshape(1, 149, 149, 3)
                    resp = requests.post(EDGE_MASTER_SERVICE, json={
                        'cam_id': cam_id,
                        'image': pickle.dumps(frame, protocol=pickle.HIGHEST_PROTOCOL).decode('latin-1')
                    })
                    logging.info("Status: %d, response: %s", resp.status_code, resp.text.strip())

                except Exception as e:
                    logging.error("Camera %d failed to publish image to Edge Master Service", cam_id)
                    raise e
            
            if DEBUG:
                cv2.imshow("Crow" + str(cam_id), frame2)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            
            frame1 = frame2
            for _ in range(SKIP):
                cap.read()
            _, frame2 = cap.read()
            for _ in range(SKIP):
                cap.read()
            
    else:
        logging.error("Failed to open capture camera: %d", cam_id)


if __name__ == '__main__':
    time.sleep(5)  # warm up time for other services
    main()
