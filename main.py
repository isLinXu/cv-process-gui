import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from cvlibs.process import CVProcess  # 导入CVProcess类


class ImageProcessingGUI:
    def __init__(self, master):
        self.master = master
        master.title("Image Processing GUI(©️islinxu)")

        self.original_image = None
        self.processed_image = None
        # 创建CVProcess类的实例
        self.cv_process = CVProcess()
        # 初始化界面布局
        self.gui_init()

    def gui_init(self):
        master = self.master
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
        self.gray_button = tk.Button(self.button_frame, text="Grayscale", command=self.convert_grayscale, width=10,height=1)
        self.gray_button.grid(row=0, column=0, pady=5)

        self.edge_button = tk.Button(self.button_frame, text="Edge Detection", command=self.edge_detection, width=10,
                                     height=1)
        self.edge_button.grid(row=1, column=0, pady=5)

        self.rotate_button = tk.Button(self.button_frame, text="Rotate", command=self.rotate_image, width=10, height=1)
        self.rotate_button.grid(row=2, column=0, pady=5)

        self.flip_button = tk.Button(self.button_frame, text="Flip", command=self.flip_image, width=10, height=1)
        self.flip_button.grid(row=3, column=0, pady=5)

        self.scale_button = tk.Button(self.button_frame, text="Scale", command=self.scale_image, width=10, height=1)
        self.scale_button.grid(row=4, column=0, pady=5)

        self.hist_eq_button = tk.Button(self.button_frame, text="Histogram Equalization", command=self.hist_eq_image,
                                        width=15, height=1)
        self.hist_eq_button.grid(row=5, column=0, pady=5)

        self.morph_button = tk.Button(self.button_frame, text="Morphology", command=self.morph_image, width=10,
                                      height=1)
        self.morph_button.grid(row=6, column=0, pady=5)

        self.blur_button = tk.Button(self.button_frame, text="Blur", command=self.blur_image, width=10, height=1)
        self.blur_button.grid(row=7, column=0, pady=5)

        self.sharpen_button = tk.Button(self.button_frame, text="Sharpen", command=self.sharpen_image, width=10,
                                        height=1)
        self.sharpen_button.grid(row=8, column=0, pady=5)

        self.noise_button = tk.Button(self.button_frame, text="noise reduction", command=self.noise_reduction, width=10,
                                      height=1)
        self.noise_button.grid(row=9, column=0, pady=5)

        self.contour_detection_button = tk.Button(self.button_frame, text="contour_detection",
                                                  command=self.contour_detection, width=10, height=1)
        self.contour_detection_button.grid(row=10, column=0, pady=5)

        self.color_space_conversion_button = tk.Button(self.button_frame, text="color_space_conversion",
                                                       command=self.color_space_conversion, width=15, height=1)
        self.color_space_conversion_button.grid(row=11, column=0, pady=5)

        self.adaptive_threshold_button = tk.Button(self.button_frame, text="Adaptive Threshold",
                                                   command=self.adaptive_threshold, width=10, height=1)
        self.adaptive_threshold_button.grid(row=12, column=0, pady=5)

        self.canvas = tk.Canvas(master, width=1080, height=800, borderwidth=1, relief="solid")
        self.canvas.pack(side=tk.RIGHT)

        # 底部输入框和滑动条
        self.common_label = tk.Label(self.master, text="input number:")
        self.common_label.place(relx=0.2, rely=0.83)

        self.common_entry = tk.Entry(self.master)
        self.common_entry.place(relx=0.3, rely=0.83)

        self.common_label = tk.Button(self.master, text="Apply Scale", command=self.custom_scale_image, width=10,height=1)
        self.common_label.place(relx=0.7, rely=0.83)

        self.brightness_label = tk.Label(self.master, text="slider:")
        self.brightness_label.place(relx=0.2, rely=0.9)

        self.common_slider = tk.Scale(self.master, from_=-255, to=255, orient=tk.HORIZONTAL, length=400)
        self.common_slider.set(0)
        self.common_slider.place(relx=0.3, rely=0.9)

        self.brightness_button = tk.Button(self.master, text="Apply Brightness", command=self.adjust_brightness, width=10, height=1)
        self.brightness_button.place(relx=0.7, rely=0.88)

        self.threshold_label = tk.Label(self.master, text="Threshold")
        self.threshold_button = tk.Button(self.master, text="Apply Threshold", command=self.apply_threshold, width=10, height=1)
        self.threshold_button.place(relx=0.7, rely=0.93)



    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = self.cv_process.open_image(file_path)
            self.processed_image = self.original_image.copy()
            self.show_images()

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.cv_process.save_image(self.processed_image, file_path)

    def show_images(self):
        if self.original_image and self.processed_image:
            original_image = self.cv_process.resize_image(self.original_image, 540, 480)
            processed_image = self.cv_process.resize_image(self.processed_image, 540, 480)

            original_photo = ImageTk.PhotoImage(original_image)
            processed_photo = ImageTk.PhotoImage(processed_image)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=original_photo)
            self.canvas.create_image(540, 0, anchor=tk.NW, image=processed_photo)
            self.canvas.image1 = original_photo
            self.canvas.image2 = processed_photo

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
            brightness = self.common_slider.get()
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
            # threshold = self.threshold_slider.get()
            threshold = self.common_slider.get()
            self.processed_image = self.cv_process.apply_threshold(self.original_image, threshold)
            self.show_images()

    def custom_scale_image(self):
        if self.original_image:
            try:
                scale_ratio = float(self.common_entry.get())
                self.processed_image = self.cv_process.custom_scale_image(self.original_image, scale_ratio)
                self.show_images()
            except ValueError:
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
