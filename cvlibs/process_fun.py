
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

def smooth(img, ksize):
    return cv2.medianBlur(img, ksize)

def morphology(img, operation, ksize):
    kernel = np.ones((ksize, ksize), np.uint8)
    return cv2.morphologyEx(img, operation, kernel)

def equalize_histogram(img):
    if len(img.shape) == 3:
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    else:
        return cv2.equalizeHist(img)

def sobel_edge_detection(img, dx, dy, ksize):
    return cv2.Sobel(img, cv2.CV_64F, dx, dy, ksize=ksize)

def laplacian_edge_detection(img, ksize):
    return cv2.Laplacian(img, cv2.CV_64F, ksize=ksize)

def scharr_edge_detection(img, dx, dy):
    return cv2.Scharr(img, cv2.CV_64F, dx, dy)

def pyramid(img, operation, level):
    if operation == "上采样":
        return cv2.pyrUp(img, dstsize=(img.shape[1]*2, img.shape[0]*2))
    else:
        return cv2.pyrDown(img, dstsize=(img.shape[1]//2, img.shape[0]//2))