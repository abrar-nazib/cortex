# fmt: off
import cv2
import numpy as np
import time
# import CxConfManager

import CxConfManager
# fmt: on
CAM_NUM = CxConfManager.cameraConf["last-used"]


def connect_cam(cam_num):
    global cap
    if 'cap' in locals():
        cap.release()
    cap = cv2.VideoCapture(cam_num)
    # print(f"Connected camera: {cam_num}")


def get_image():
    ret, frame = cap.read()
    # frame = cv2.flip(frame, 1)
    return frame


if __name__ != "__main__":
    connect_cam(CAM_NUM)
#     time.sleep(2)
#     frame = get_image()
#     print(frame)
#     time.sleep(2)


if __name__ == "__main__":
    connect_cam(CAM_NUM)
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow("window", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
