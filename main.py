

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance
import cv2
import numpy as np

class ImageProcessingGUI:
    def __init__(self, master):
        self.master = master
        master.title("Image Processing GUI")

        self.original_image = None
        self.processed_image = None

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # 顶部按钮
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(side=tk.TOP, pady=10)

        self.open_button = tk.Button(self.top_frame, text="Open Image", command=self.open_image, width=10, height=1)
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.top_frame, text="Save Image", command=self.save_image, width=10, height=1)
        self.save_button.pack(side=tk.RIGHT, padx=5)

        # 第一列按钮
        self.gray_button = tk.Button(self.button_frame, text="Grayscale", command=self.convert_grayscale, width=10,
                                     height=1)
        self.gray_button.grid(row=0, column=0, pady=5)

        self.edge_button = tk.Button(self.button_frame, text="Edge Detection", command=self.edge_detection, width=10,
                                     height=1)
        self.edge_button.grid(row=1, column=0, pady=5)

        self.rotate_button = tk.Button(self.button_frame, text="Rotate", command=self.rotate_image, width=10, height=1)
        self.rotate_button.grid(row=2, column=0, pady=5)

        # 第二列按钮
        self.flip_button = tk.Button(self.button_frame, text="Flip", command=self.flip_image, width=10, height=1)
        self.flip_button.grid(row=0, column=1, pady=5)

        self.scale_button = tk.Button(self.button_frame, text="Scale", command=self.scale_image, width=10, height=1)
        self.scale_button.grid(row=1, column=1, pady=5)

        self.hist_eq_button = tk.Button(self.button_frame, text="Histogram Equalization", command=self.hist_eq_image,
                                        width=10, height=1)
        self.hist_eq_button.grid(row=2, column=1, pady=5)

        # 第三列按钮
        self.morph_button = tk.Button(self.button_frame, text="Morphology", command=self.morph_image,width=10, height=1)
        self.morph_button.grid(row=0, column=2, pady=5)

        self.blur_button = tk.Button(self.button_frame, text="Blur", command=self.blur_image, width=10, height=1)
        self.blur_button.grid(row=1, column=2, pady=5)

        self.sharpen_button = tk.Button(self.button_frame, text="Sharpen", command=self.sharpen_image, width=10,height=1)
        self.sharpen_button.grid(row=2, column=2, pady=5)

        # 底部输入框和滑动条
        self.brightness_label = tk.Label(self.button_frame, text="Brightness")
        self.brightness_label.grid(row=3, column=0)
        self.brightness_slider = tk.Scale(self.button_frame, from_=-100, to=100, orient=tk.HORIZONTAL, length=150)
        self.brightness_slider.set(0)
        self.brightness_slider.grid(row=3, column=1)
        self.brightness_button = tk.Button(self.button_frame, text="Apply Brightness", command=self.adjust_brightness,
                                           width=10, height=1)
        self.brightness_button.grid(row=3, column=2, pady=5)

        self.threshold_label = tk.Label(self.button_frame, text="Threshold")
        self.threshold_label.grid(row=4, column=0)
        self.threshold_slider = tk.Scale(self.button_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=150)
        self.threshold_slider.grid(row=4, column=1)
        self.threshold_button = tk.Button(self.button_frame, text="Apply Threshold", command=self.apply_threshold,
                                          width=10, height=1)
        self.threshold_button.grid(row=4, column=2, pady=5)

        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack(side=tk.RIGHT)

        # 在底部添加自定义缩放输入框和按钮
        self.scale_label = tk.Label(self.button_frame, text="Scale Ratio")
        self.scale_label.grid(row=7, column=0)
        self.scale_entry = tk.Entry(self.button_frame)
        self.scale_entry.grid(row=7, column=1)
        self.scale_button = tk.Button(self.button_frame, text="Custom Scale", command=self.custom_scale_image, width=15,
                                          height=2)
        self.scale_button.grid(row=7, column=2, pady=5)

        # 在底部添加自适应阈值按钮
        self.adaptive_threshold_button = tk.Button(self.button_frame, text="Adaptive Threshold",
                                                       command=self.adaptive_threshold, width=15, height=2)
        self.adaptive_threshold_button.grid(row=8, column=0, pady=5)
    # def __init__(self, master):
    #     self.master = master
    #     master.title("Image Processing GUI")
    #
    #     self.original_image = None
    #     self.processed_image = None
    #
    #     self.button_frame = tk.Frame(master)
    #     self.button_frame.pack(side=tk.LEFT, padx=10, pady=10)
    #
    #     # 顶部按钮
    #     self.open_button = tk.Button(self.button_frame, text="Open Image", command=self.open_image, width=15, height=2)
    #     self.open_button.grid(row=0, column=0, columnspan=3, pady=5)
    #
    #     self.save_button = tk.Button(self.button_frame, text="Save Image", command=self.save_image, width=15, height=2)
    #     self.save_button.grid(row=1, column=0, columnspan=3, pady=5)
    #
    #     # 第一列按钮
    #     self.gray_button = tk.Button(self.button_frame, text="Grayscale", command=self.convert_grayscale, width=15, height=2)
    #     self.gray_button.grid(row=2, column=0, pady=5)
    #
    #     self.edge_button = tk.Button(self.button_frame, text="Edge Detection", command=self.edge_detection, width=15, height=2)
    #     self.edge_button.grid(row=3, column=0, pady=5)
    #
    #     self.rotate_button = tk.Button(self.button_frame, text="Rotate", command=self.rotate_image, width=15, height=2)
    #     self.rotate_button.grid(row=4, column=0, pady=5)
    #
    #     # 第二列按钮
    #     self.flip_button = tk.Button(self.button_frame, text="Flip", command=self.flip_image, width=15, height=2)
    #     self.flip_button.grid(row=2, column=1, pady=5)
    #
    #     self.scale_button = tk.Button(self.button_frame, text="Scale", command=self.scale_image, width=15, height=2)
    #     self.scale_button.grid(row=3, column=1, pady=5)
    #
    #     self.hist_eq_button = tk.Button(self.button_frame, text="Histogram Equalization", command=self.hist_eq_image, width=15, height=2)
    #     self.hist_eq_button.grid(row=4, column=1, pady=5)
    #
    #     # 第三列按钮
    #     self.morph_button = tk.Button(self.button_frame, text="Morphology (Dilate/Erode)", command=self.morph_image, width=15, height=2)
    #     self.morph_button.grid(row=2, column=2, pady=5)
    #
    #     self.blur_button = tk.Button(self.button_frame, text="Blur", command=self.blur_image, width=15, height=2)
    #     self.blur_button.grid(row=3, column=2, pady=5)
    #
    #     self.sharpen_button = tk.Button(self.button_frame, text="Sharpen", command=self.sharpen_image, width=15, height=2)
    #     self.sharpen_button.grid(row=4, column=2, pady=5)
    #
    #     # 底部输入框和滑动条
    #     self.brightness_label = tk.Label(self.button_frame, text="Brightness")
    #     self.brightness_label.grid(row=5, column=0)
    #     self.brightness_slider = tk.Scale(self.button_frame, from_=-100, to=100, orient=tk.HORIZONTAL, length=150)
    #     self.brightness_slider.set(0)
    #     self.brightness_slider.grid(row=5, column=1)
    #     self.brightness_button = tk.Button(self.button_frame, text="Apply Brightness", command=self.adjust_brightness, width=15, height=2)
    #     self.brightness_button.grid(row=5, column=2, pady=5)
    #
    #     self.threshold_label = tk.Label(self.button_frame, text="Threshold")
    #     self.threshold_label.grid(row=6, column=0)
    #     self.threshold_slider = tk.Scale(self.button_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=150)
    #     self.threshold_slider.grid(row=6, column=1)
    #     self.threshold_button = tk.Button(self.button_frame, text="Apply Threshold", command=self.apply_threshold, width=15, height=2)
    #     self.threshold_button.grid(row=6, column=2, pady=5)
    #
    #     self.canvas = tk.Canvas(master, width=800, height=600)
    #     self.canvas.pack(side=tk.RIGHT)
    #
    #     # 在底部添加自定义缩放输入框和按钮
    #     self.scale_label = tk.Label(self.button_frame, text="Scale Ratio")
    #     self.scale_label.grid(row=7, column=0)
    #     self.scale_entry = tk.Entry(self.button_frame)
    #     self.scale_entry.grid(row=7, column=1)
    #     self.scale_button = tk.Button(self.button_frame, text="Custom Scale", command=self.custom_scale_image, width=15,
    #                                   height=2)
    #     self.scale_button.grid(row=7, column=2, pady=5)
    #
    #     # 在底部添加自适应阈值按钮
    #     self.adaptive_threshold_button = tk.Button(self.button_frame, text="Adaptive Threshold",
    #                                                command=self.adaptive_threshold, width=15, height=2)
    #     self.adaptive_threshold_button.grid(row=8, column=0, pady=5)
    #
    #     # 其他功能的按钮可以按照上述方式继续添加

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.processed_image = self.original_image.copy()
            self.show_images()

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.processed_image.save(file_path)

    def show_images(self):
        if self.original_image and self.processed_image:
            original_image = self.original_image.resize((400, 300), Image.ANTIALIAS)
            processed_image = self.processed_image.resize((400, 300), Image.ANTIALIAS)

            original_photo = ImageTk.PhotoImage(original_image)
            processed_photo = ImageTk.PhotoImage(processed_image)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=original_photo)
            self.canvas.create_image(400, 0, anchor=tk.NW, image=processed_photo)

            self.canvas.image1 = original_photo
            self.canvas.image2 = processed_photo

    def hist_eq_image(self):
        if self.original_image:
            img = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)
            img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
            img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
            self.processed_image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
            self.processed_image = Image.fromarray(self.processed_image)
            self.show_images()

    def morph_image(self):
        if self.original_image:
            kernel = np.ones((5, 5), np.uint8)
            img = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)
            dilation = cv2.dilate(img, kernel, iterations=1)
            erosion = cv2.erode(img, kernel, iterations=1)
            self.processed_image = cv2.absdiff(dilation, erosion)
            self.processed_image = Image.fromarray(self.processed_image)
            self.show_images()

    def blur_image(self):
        if self.original_image:
            self.processed_image = self.original_image.filter(ImageFilter.BLUR)
            self.show_images()

    def sharpen_image(self):
        if self.original_image:
            self.processed_image = self.original_image.filter(ImageFilter.SHARPEN)
            self.show_images()

    def convert_grayscale(self):
        if self.original_image:
            self.processed_image = ImageOps.grayscale(self.original_image)
            self.show_images()

    def edge_detection(self):
        if self.original_image:
            img = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)
            edges = cv2.Canny(img, 100, 200)
            self.processed_image = Image.fromarray(cv2.cvtColor(edges, cv2.COLOR_BGR2RGB))
            self.show_images()

    def rotate_image(self):
        if self.original_image:
            self.processed_image = self.original_image.rotate(90)
            self.show_images()

    def flip_image(self):
        if self.original_image:
            self.processed_image = cv2.flip(np.array(self.original_image), 1)
            self.processed_image = Image.fromarray(self.processed_image)
            self.show_images()

    def adjust_brightness(self):
        if self.original_image:
            brightness = self.brightness_slider.get()
            enhancer = ImageEnhance.Brightness(self.original_image)
            self.processed_image = enhancer.enhance((brightness + 100) / 100)
            self.show_images()

    def scale_image(self):
        if self.original_image:
            width, height = self.original_image.size
            self.processed_image = cv2.resize(np.array(self.original_image), (width // 2, height // 2),
                                              interpolation=cv2.INTER_AREA)
            self.processed_image = Image.fromarray(self.processed_image)
            self.show_images()

    def noise_reduction(self):
        if self.original_image:
            img = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)
            self.processed_image = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
            self.processed_image = Image.fromarray(self.processed_image)
            self.show_images()

    def contour_detection(self):
        if self.original_image:
            img = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 127, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
            self.processed_image = Image.fromarray(img)
            self.show_images()

    def color_space_conversion(self):
        if self.original_image:
            img = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)
            self.processed_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            self.processed_image = Image.fromarray(self.processed_image)
            self.show_images()

    def show_label(self):
        if self.original_image:
            with open('labels.txt', 'r') as f:
                labels = f.readlines()
            label = labels[np.random.randint(len(labels))].strip()
            self.canvas.create_text(200, 350, text=f"Label: {label}", font=("Arial", 14), fill="blue")

    def hist_eq_image(self):
        if self.original_image:
            img = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)
            img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
            img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
            self.processed_image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
            self.processed_image = Image.fromarray(self.processed_image)
            self.show_images()

    def apply_threshold(self):
        if self.original_image:
            threshold = self.threshold_slider.get()
            img = self.original_image.convert("L")
            self.processed_image = img.point(lambda p: p > threshold and 255)
            self.show_images()

    # 定义一个处理函数，用于执行自定义缩放任务
    def custom_scale_image(self):
        if self.original_image:
            try:
                scale_ratio = float(self.scale_entry.get())
                width, height = self.original_image.size
                new_width = int(width * scale_ratio)
                new_height = int(height * scale_ratio)
                self.processed_image = cv2.resize(np.array(self.original_image), (new_width, new_height),
                                                  interpolation=cv2.INTER_AREA)
                self.processed_image = Image.fromarray(self.processed_image)
                self.show_images()
            except ValueError:
                # 如果输入的缩放比例无效，显示一个错误消息
                messagebox.showerror("Error", "Invalid scale ratio. Please enter a valid number.")

    # 定义一个处理函数，用于执行自适应阈值任务
    def adaptive_threshold(self):
        if self.original_image:
            img = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                                    11, 2)
            self.processed_image = Image.fromarray(adaptive_thresh)
            self.show_images()


if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageProcessingGUI(root)
    root.mainloop()