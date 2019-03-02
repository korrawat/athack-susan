import cv2
import numpy as np


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)


    def snapshot(self):
        ret, frame = self.cap.read()
        return frame


if __name__ == '__main__':
    camera = Camera()
    while True:
        k = cv2.waitKey(1)
        if k == 27:
            break
        frame = camera.snapshot()
        cv2.imshow('image', frame)