
import cv2
import numpy as np

def open_image(file_path):
    img = cv2.imread(file_path)
    img = cv2.resize(img, (400, 400))
    return img

def convert_image_to_bytes(img):
    ret, buf = cv2.imencode(".png", img)
    return buf.tobytes()

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def rotate(img, angle):
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, M, (w, h))

def scale(img, factor):
    h, w = img.shape[:2]
    new_size = (int(w * factor), int(h * factor))
    return cv2.resize(img, new_size)

def flip(img, direction):
    return cv2.flip(img, direction)

def gaussian_blur(img, ksize):
    return cv2.GaussianBlur(img, (ksize, ksize), 0)

def adjust_contrast_brightness(img, alpha, beta):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def canny_edge_detection(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)

def threshold(img, thresh_value):
    _, thresh_img = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY)
    return thresh_img