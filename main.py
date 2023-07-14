import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from cvlibs.process import CVProcess  # 导入CVProcess类

class ImageProcessingGUI:
    def __init__(self, master):
        self.master = master
        master.title("Image Processing GUI")

        self.original_image = None
        self.processed_image = None
        self.cv_process = CVProcess()  # 创建CVProcess类的实例

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



    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = self.cv_process.open_image(file_path)  # 使用CVProcess类的实例打开图像
            self.processed_image = self.original_image.copy()
            self.show_images()

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.cv_process.save_image(self.processed_image, file_path)

    def show_images(self):
        if self.original_image and self.processed_image:
            original_image = self.cv_process.resize_image(self.original_image, 400, 300)
            processed_image = self.cv_process.resize_image(self.processed_image, 400, 300)

            original_photo = ImageTk.PhotoImage(original_image)
            processed_photo = ImageTk.PhotoImage(processed_image)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=original_photo)
            self.canvas.create_image(400, 0, anchor=tk.NW, image=processed_photo)

            self.canvas.image1 = original_photo
            self.canvas.image2 = processed_photo

    # 在处理函数中，使用CVProcess类的实例调用图像处理方法
    def convert_grayscale(self):
        if self.original_image:
            self.processed_image = self.cv_process.convert_grayscale(self.original_image)
            self.show_images()

    def edge_detection(self):
        if self.original_image:
            self.processed_image = self.cv_process.edge_detection(self.original_image)
            self.show_images()

    def rotate_image(self):
        if self.original_image:
            self.processed_image = self.cv_process.rotate_image(self.original_image)
            self.show_images()

    def flip_image(self):
        if self.original_image:
            self.processed_image = self.cv_process.flip_image(self.original_image)
            self.show_images()

    def adjust_brightness(self):
        if self.original_image:
            brightness = self.brightness_slider.get()
            self.processed_image = self.cv_process.adjust_brightness(self.original_image, brightness)
            self.show_images()

    def scale_image(self):
        if self.original_image:
            self.processed_image = self.cv_process.scale_image(self.original_image)
            self.show_images()

    def noise_reduction(self):
        if self.original_image:
            self.processed_image = self.cv_process.noise_reduction(self.original_image)
            self.show_images()

    def contour_detection(self):
        if self.original_image:
            self.processed_image = self.cv_process.contour_detection(self.original_image)
            self.show_images()

    def color_space_conversion(self):
        if self.original_image:
            self.processed_image = self.cv_process.color_space_conversion(self.original_image)
            self.show_images()

    def hist_eq_image(self):
        if self.original_image:
            self.processed_image = self.cv_process.hist_eq_image(self.original_image)
            self.show_images()

    def apply_threshold(self):
        if self.original_image:
            threshold = self.threshold_slider.get()
            self.processed_image = self.cv_process.apply_threshold(self.original_image, threshold)
            self.show_images()

    def custom_scale_image(self):
        if self.original_image:
            try:
                scale_ratio = float(self.scale_entry.get())
                self.processed_image = self.cv_process.custom_scale_image(self.original_image, scale_ratio)
                self.show_images()
            except ValueError:
                # 如果输入的缩放比例无效，显示一个错误消息
                messagebox.showerror("Error", "Invalid scale ratio. Please enter a valid number.")

    def adaptive_threshold(self):
        if self.original_image:
            self.processed_image = self.cv_process.adaptive_threshold(self.original_image)
            self.show_images()

    def blur_image(self):
        if self.original_image:
            self.processed_image = self.cv_process.blur_image(self.original_image)
            self.show_images()

    def sharpen_image(self):
        if self.original_image:
            self.processed_image = self.cv_process.sharpen_image(self.original_image)
            self.show_images()

    def morph_image(self):
        if self.original_image:
            self.processed_image = self.cv_process.morph_image(self.original_image, operation="dilate_erode")
            self.show_images()


if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageProcessingGUI(root)
    root.mainloop()
