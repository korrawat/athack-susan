import cv2
import numpy as np
from camera import Camera
from processor_properties import ProcessorProperties


class ProcessedStream:
    def __init__(self, camera, properties):
        ''' properties is a dictionary of properties '''
        self.camera = camera
        self.properties = properties


    def read(self):
        ''' returns a tuple of original and processed images '''
        return self.camera.snapshot(),\
            process_image(self.camera.snapshot(), self.properties)


def brightness(image, factor):
    # if use `image * factor`, need to cast to int
    # return image * factor
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)


def contrast(image, factor, midpoint=127):
    ''' midpoint doesn't need to be exposed to user (too complicated) '''
    # return midpoint + factor * (image - midpoint);
    beta = midpoint * (1 - factor)
    return cv2.convertScaleAbs(image, alpha=factor, beta=beta)

def grayscale(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return np.stack((gray_img,)*3, axis=-1)


# TODO
# - contrast increases noise! maybe add bilateral filter (slow)?
# - gamma correction?

def process_image(image, properties):
    out = np.copy(image)
    out = brightness(out, properties.brightness_factor.value)
    out = contrast(out, properties.contrast_factor.value)
    if properties.grayscale.value:
        out = grayscale(out)
    return out
