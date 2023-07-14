import tkinter as tk
from tkinter import filedialog
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

        self.open_button = tk.Button(self.button_frame, text="Open Image", command=self.open_image, width=15, height=2)
        self.open_button.pack(pady=5)

        self.save_button = tk.Button(self.button_frame, text="Save Image", command=self.save_image, width=15, height=2)
        self.save_button.pack(pady=5)

        self.gray_button = tk.Button(self.button_frame, text="Grayscale", command=self.convert_grayscale, width=15, height=2)
        self.gray_button.pack(pady=5)

        self.edge_button = tk.Button(self.button_frame, text="Edge Detection", command=self.edge_detection, width=15, height=2)
        self.edge_button.pack(pady=5)

        self.rotate_button = tk.Button(self.button_frame, text="Rotate", command=self.rotate_image, width=15, height=2)
        self.rotate_button.pack(pady=5)

        self.flip_button = tk.Button(self.button_frame, text="Flip", command=self.flip_image, width=15, height=2)
        self.flip_button.pack(pady=5)

        self.scale_button = tk.Button(self.button_frame, text="Scale", command=self.scale_image, width=15, height=2)
        self.scale_button.pack(pady=5)

        self.hist_eq_button = tk.Button(self.button_frame, text="Histogram Equalization", command=self.hist_eq_image, width=15, height=2)
        self.hist_eq_button.pack(pady=5)

        self.morph_button = tk.Button(self.button_frame, text="Morphology (Dilate/Erode)", command=self.morph_image, width=15, height=2)
        self.morph_button.pack(pady=5)

        self.blur_button = tk.Button(self.button_frame, text="Blur", command=self.blur_image, width=15, height=2)
        self.blur_button.pack(pady=5)

        self.sharpen_button = tk.Button(self.button_frame, text="Sharpen", command=self.sharpen_image, width=15, height=2)
        self.sharpen_button.pack(pady=5)

        self.brightness_label = tk.Label(self.button_frame, text="Brightness")
        self.brightness_label.pack()

        self.brightness_slider = tk.Scale(self.button_frame, from_=-100, to=100, orient=tk.HORIZONTAL, length=150)
        self.brightness_slider.set(0)
        self.brightness_slider.pack()

        self.brightness_button = tk.Button(self.button_frame, text="Apply Brightness", command=self.adjust_brightness, width=15, height=2)
        self.brightness_button.pack(pady=5)

        self.threshold_label = tk.Label(self.button_frame, text="Threshold")
        self.threshold_label.pack()

        self.threshold_slider = tk.Scale(self.button_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=150)
        self.threshold_slider.pack()

        self.threshold_button = tk.Button(self.button_frame, text="Apply Threshold", command=self.apply_threshold, width=15, height=2)
        self.threshold_button.pack(pady=5)

        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack(side=tk.RIGHT)

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

    def scale_image(self):
        if self.original_image:
            width, height = self.original_image.size
            self.processed_image = cv2.resize(np.array(self.original_image), (width // 2, height // 2),
                                              interpolation=cv2.INTER_AREA)
            self.processed_image = Image.fromarray(self.processed_image)
            self.show_images()

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

    def adjust_brightness(self):
        if self.original_image:
            brightness = self.brightness_slider.get()
            enhancer = ImageEnhance.Brightness(self.original_image)
            self.processed_image = enhancer.enhance((brightness + 100) / 100)
            self.show_images()

    def apply_threshold(self):
        if self.original_image:
            threshold = self.threshold_slider.get()
            img = self.original_image.convert("L")
            self.processed_image = img.point(lambda p: p > threshold and 255)
            self.show_images()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageProcessingGUI(root)
    root.mainloop()