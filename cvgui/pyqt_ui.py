import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget, \
    QScrollArea, QAction, QMessageBox, QHBoxLayout, QInputDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # 添加打开图像的动作
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.select_image)
        file_menu.addAction(open_action)

        # 添加保存图像的动作
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_image)
        file_menu.addAction(save_action)

        # 添加旋转图像的动作
        rotate_action = QAction('Rotate', self)
        rotate_action.triggered.connect(self.rotate_image)
        file_menu.addAction(rotate_action)

        # 添加镜像翻转图像的动作
        flip_action = QAction('Flip', self)
        flip_action.triggered.connect(self.flip_image)
        file_menu.addAction(flip_action)

        # 创建按钮
        self.process_button = QPushButton('Process Image')
        self.process_button.clicked.connect(self.process_image)

        self.previous_button = QPushButton('Previous')
        self.next_button = QPushButton('Next')
        self.previous_button.clicked.connect(self.previous_image)
        self.next_button.clicked.connect(self.next_image)

        # 创建可滚动的画布区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 创建画布
        self.canvas_label = QLabel()
        self.canvas_label.setAlignment(Qt.AlignCenter)

        # 设置画布为可滚动区域的子控件
        self.scroll_area.setWidget(self.canvas_label)

        # 创建主布局并添加控件
        layout = QVBoxLayout()
        layout.addWidget(self.process_button)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.previous_button)
        path_layout.addWidget(self.next_button)
        layout.addLayout(path_layout)

        layout.addWidget(self.scroll_area)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image_paths = []  # 图像路径列表
        self.current_index = 0  # 当前图像索引

        self.selected_image = None

    def select_image(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        if file_dialog.exec_():
            dir_names = file_dialog.selectedFiles()
            if dir_names:
                dir_name = dir_names[0]
                self.load_image_paths(dir_name)  # 加载指定路径下的图像文件
                self.show_image(self.image_paths[self.current_index])

    def load_image_paths(self, dir_name):
        self.image_paths = []
        for filename in os.listdir(dir_name):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                file_path = os.path.join(dir_name, filename)
                self.image_paths.append(file_path)

    def previous_image(self):
        if len(self.image_paths) == 0:
            return

        self.current_index = (self.current_index - 1) % len(self.image_paths)
        self.show_image(self.image_paths[self.current_index])

    def next_image(self):
        if len(self.image_paths) == 0:
            return

        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.show_image(self.image_paths[self.current_index])

    def process_image(self):
        if self.selected_image is None:
            QMessageBox.warning(self, 'Warning', 'Please select an image first!')
            return

        processed_image = self.selected_image
        # TODO: Add image processing operations here

        # 显示处理结果
        self.show_windows_image(processed_image)


    def show_windows_image(self, image):
        self.selected_image = image

        image_rgb = cv2.cvtColor(self.selected_image, cv2.COLOR_BGR2RGB)
        pixmap = QPixmap.fromImage(QImage(image_rgb.data, image_rgb.shape[1], image_rgb.shape[0], QImage.Format_RGB888))
        self.canvas_label.setPixmap(pixmap.scaled(self.canvas_label.width(), self.canvas_label.height(),
                                                  Qt.KeepAspectRatio, Qt.SmoothTransformation))




    def show_image(self, image_path):
        src_img = cv2.imread(image_path)
        self.selected_image = src_img

        image_rgb = cv2.cvtColor(self.selected_image, cv2.COLOR_BGR2RGB)
        pixmap = QPixmap.fromImage(QImage(image_rgb.data, image_rgb.shape[1], image_rgb.shape[0], QImage.Format_RGB888))
        self.canvas_label.setPixmap(pixmap.scaled(self.canvas_label.width(), self.canvas_label.height(),
                                                  Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def save_image(self):
        if self.selected_image is None:
            QMessageBox.warning(self, 'Warning', 'Please select an image first!')
            return

        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()[0]

            # 保存图像
            cv2.imwrite(file_name, self.selected_image)

    def rotate_image(self):
        if self.selected_image is None:
            QMessageBox.warning(self, 'Warning', 'No image selected!')
            return

        rotation_angle, ok = QInputDialog.getInt(self, 'Rotate Image', 'Enter rotation angle:', 0, -360, 360)
        if ok:
            # 使用OpenCV旋转图像
            rows, cols, _ = self.selected_image.shape
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation_angle, 1)
            rotated_image = cv2.warpAffine(self.selected_image, M, (cols, rows))
            self.selected_image = rotated_image

            # 显示旋转后的图像
            self.show_windows_image(rotated_image)

    def flip_image(self):
        if self.selected_image is None:
            QMessageBox.warning(self, 'Warning', 'No image selected!')
            return

        choice, ok = QInputDialog.getItem(self, 'Flip Image', 'Choose flip direction:', ['Horizontal', 'Vertical'])
        if ok:
            # 使用OpenCV镜像翻转图像
            if choice == 'Horizontal':
                flipped_image = cv2.flip(self.selected_image, 1)
            else:  # choice == 'Vertical'
                flipped_image = cv2.flip(self.selected_image, 0)

            self.selected_image = flipped_image

            # 显示翻转后的图像
            self.show_windows_image(flipped_image)

    def adjust_brightness(self):
        if self.selected_image is None:
            QMessageBox.warning(self, 'Warning', 'No image selected!')

            brightness, ok = QInputDialog.getInt(self, 'Adjust Brightness', 'Enter brightness value (-255 to 255):', 0, -255, 255)
            if ok:
                # 使用OpenCV调整亮度
                adjusted_image = cv2.convertScaleAbs(self.selected_image, alpha=1, beta=brightness)
                self.selected_image = adjusted_image

                # 显示调整后的图像
                self.show_windows_image(adjusted_image)

    def adjust_contrast(self):
        if self.selected_image is None:
            QMessageBox.warning(self, 'Warning', 'No image selected!')

            contrast, ok = QInputDialog.getDouble(self, 'Adjust Contrast', 'Enter contrast value (1.-3.):', 1., 1.,
                                                      3.)
            if ok:
            # 使用OpenCV调整对比度
                adjusted_image = cv2.convertScaleAbs(self.selected_image, alpha=contrast, beta=0)
                self.selected_image = adjusted_image

                # 显示调整后的图像
                self.show_windows_image(adjusted_image)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())