import cv2
import numpy as np
from image_processor import process_image
from processor_properties import ProcessorProperties


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
        props = ProcessorProperties()
        # props.brightness_factor.update(1.5)
        # props.contrast_factor.update(1.5)
        # props.scaling_factor.update(3.0)
        frame = process_image(frame, props)
        cv2.imshow('image', frame)