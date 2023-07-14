from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import cv2
import numpy as np

class CVProcess:
    def __init__(self):
        pass

    def open_image(self, file_path):
        return Image.open(file_path)

    def save_image(self, image, file_path):
        image.save(file_path)

    def resize_image(self, image, width, height):
        return image.resize((width, height), Image.ANTIALIAS)

    def convert_grayscale(self, image):
        return ImageOps.grayscale(image)

    def edge_detection(self, image):
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        edges = cv2.Canny(img, 100, 200)
        return Image.fromarray(cv2.cvtColor(edges, cv2.COLOR_BGR2RGB))

    def rotate_image(self, image):
        return image.rotate(90)

    def flip_image(self, image):
        flipped_image = cv2.flip(np.array(image), 1)
        return Image.fromarray(flipped_image)

    def adjust_brightness(self, image, brightness):
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance((brightness + 100) / 100)

    def scale_image(self, image):
        width, height = image.size
        scaled_image = cv2.resize(np.array(image), (width // 2, height // 2), interpolation=cv2.INTER_AREA)
        return Image.fromarray(scaled_image)

    def noise_reduction(self, image):
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        processed_image = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        return Image.fromarray(processed_image)

    def contour_detection(self, image):
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
        return Image.fromarray(img)

    def color_space_conversion(self, image):
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        processed_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return Image.fromarray(processed_image)

    def hist_eq_image(self, image):
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        processed_image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        return Image.fromarray(processed_image)

    def apply_threshold(self, image, threshold):
        img = image.convert("L")
        return img.point(lambda p: p > threshold and 255)

    def custom_scale_image(self, image, scale_ratio):
        width, height = image.size
        new_width = int(width * scale_ratio)
        new_height = int(height * scale_ratio)
        processed_image = cv2.resize(np.array(image), (new_width, new_height), interpolation=cv2.INTER_AREA)
        return Image.fromarray(processed_image)

    def adaptive_threshold(self, image):
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return Image.fromarray(adaptive_thresh)

    def blur_image(self, image):
        return image.filter(ImageFilter.BLUR)

    def sharpen_image(self, image):
        return image.filter(ImageFilter.SHARPEN)

    def morph_image(self, image, operation="dilate_erode"):
        kernel = np.ones((5, 5), np.uint8)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        if operation == "dilate_erode":
            dilation = cv2.dilate(img, kernel, iterations=1)
            erosion = cv2.erode(img, kernel, iterations=1)
            processed_image = cv2.absdiff(dilation, erosion)
        # 添加其他形态学操作，如膨胀、腐蚀、开运算和闭运算
        # ...

            return Image.fromarray(processed_image)