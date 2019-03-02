import cv2
import numpy as np
from camera import Camera


class ImageProcessor:
    def __init__(self, properties):
        ''' properties is a dictionary of properties '''
        self.properties = properties


    def updateProperties(self, properties):
        self.properties = properties


    def change_contrast(self, image):
        alpha = 2.2
        beta=  50
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


    def read(self):
        pass