# fmt: off
import cv2
import numpy as np
# import CxConfManager

import CxConfManager
# fmt: on

CAMERA = CxConfManager.cameraConf["last-used"]
print(CAMERA)


def connect_cam():
    global cap
    if 'cap' in locals():
        cap.release()
    cap = cv2.VideoCapture(CAMERA)


def get_image():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    return frame


if __name__ != "__main__":
    connect_cam()

if __name__ == "__main__":
    connect_cam()
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow("window", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
