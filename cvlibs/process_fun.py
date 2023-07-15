
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

def find_contours(img):
    img_gray = grayscale(img)
    img_canny = canny_edge_detection(img_gray, 100, 200)
    contours, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = img.copy()
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)
    return img_contours

def template_matching(img, template_path):
    img_gray = grayscale(img)
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    img_matched = img.copy()
    cv2.rectangle(img_matched, top_left, bottom_right, (0, 255, 0), 2)
    return img_matched

def hough_lines(img):
    img_gray = grayscale(img)
    img_canny = canny_edge_detection(img_gray, 100, 200)
    lines = cv2.HoughLinesP(img_canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    img_lines = img.copy()
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return img_lines

def hough_circles(img):
    img_gray = grayscale(img)
    img_blur = cv2.medianBlur(img_gray, 5)
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    img_circles = img.copy()
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(img_circles, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(img_circles, (i[0], i[1]), 2, (0, 0, 255), 3)
        return img_circles

