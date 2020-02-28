import cv2
import subprocess
import atexit


CAM_PROC_STATUSES = {}


def start_camera_processes():
    """This starts all the camera processes that talk back at this master"""
    # detect which cameras are available for use. Unfortunately cv2 doesn't have any
    # good interface to do so, so we'll have to "open" up to 10 cameras, and see if
    # if they were successfully opened
    for i in range(11):
        capture = cv2.VideoCapture(i)
        if capture.isOpened():
            CAM_PROC_STATUSES[i] = {'proc': None, 'last_status': 'Not Started'}
        capture.release()
    print("Detected cameras: " + str(list(CAM_PROC_STATUSES.keys())))

    # creates a child process for each camera
    for cam_id in list(CAM_PROC_STATUSES.keys()):
        proc = subprocess.Popen([
            'python',
            'cam-process/camera_reader.py',
            str(cam_id)
        ])
        CAM_PROC_STATUSES['proc'] = proc

    # I _think_ these processes should be killed gracefully since we are
    # dealing with system devices
    @atexit.register
    def kill_processes():
        for cam_id in CAM_PROC_STATUSES:
            proc = CAM_PROC_STATUSES[cam_id]['proc']
            proc.terminate()
            proc.wait()


def start_inference_service():
    """Starts the inference service that runs locally on the edge device"""
    proc = subprocess.Popen([
        'python',
        'inference-service/inference_app.py'
    ])

    @atexit.register
    def kill_inference_app():
        proc.terminate()
        proc.wait()


def start_deterrent_service():
    """Starts the deterrent service that runs locally on the edge device"""
    proc = subprocess.Popen([
        'python',
        'deterrent-service/deterrent_app.py'
    ])

    @atexit.register
    def kill_inference_app():
        proc.terminate()
        proc.wait()
