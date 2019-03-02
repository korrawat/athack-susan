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

def scale(image, scaling_factor):
    # better but slower option: interpolation=cv2.INTER_CUBIC
    height, width, _ = np.shape(image)
    new_height = int(1.0 * height / scaling_factor)
    new_width = int(1.0 * width / scaling_factor)
    start_y = (height - new_height) / 2
    start_x = (width - new_width) / 2
    cropped = image[start_y: start_y + new_height, start_x: start_x + new_width, :]
    zoomed = cv2.resize(cropped, (0,0), fx=scaling_factor, fy=scaling_factor,\
        interpolation=cv2.INTER_CUBIC)
    return zoomed


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


def threshold(image, blocksize=15, C=5):
    # https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html?highlight=adaptivethreshold#cv2.adaptiveThreshold
    grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    output = cv2.adaptiveThreshold(grayscale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
            cv2.THRESH_BINARY, blocksize, C)
    return np.stack((output,)*3, axis=-1)


# TODO
# - contrast increases noise! maybe add bilateral filter (slow)?
# - gamma correction?

def process_image(image, properties):
    out = np.copy(image)
    if properties.scaling_factor.value > 1.0:
        out = scale(out, properties.scaling_factor.value)
    if properties.brightness_factor.value != 1.0:
        out = brightness(out, properties.brightness_factor.value)
    if properties.contrast_factor.value != 1.0:
        out = contrast(out, properties.contrast_factor.value)
    if properties.grayscale.value:
        out = grayscale(out)
    out = threshold(image)
    return out
