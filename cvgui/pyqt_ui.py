import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget, \
    QScrollArea, QAction, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2


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

        # 创建按钮
        self.process_button = QPushButton('Process Image')
        self.process_button.clicked.connect(self.process_image)

        # 创建路径切换按钮
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

        # 创建路径切换布局
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.previous_button)
        path_layout.addWidget(self.next_button)
        layout.addLayout(path_layout)

        layout.addWidget(self.scroll_area)

        # 创建中心窗口并设置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image_paths = []  # 图像路径列表
        self.current_index = 0  # 当前图像索引

        self.selected_image = None

    def select_image(self):
        # 弹出文件选择对话框
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

        # 在这里对图像进行处理，比如使用OpenCV进行图像算法处理
        processed_image = self.selected_image

        # 显示处理结果
        self.show_image(processed_image)

    def show_image(self, image_path):
        # 从图像路径加载图像数据
        self.selected_image = cv2.imread(image_path)

        # 将OpenCV图像对象转换为QPixmap对象并在画布上显示图像
        image_rgb = cv2.cvtColor(self.selected_image, cv2.COLOR_BGR2RGB)
        pixmap = QPixmap.fromImage(QImage(image_rgb.data, image_rgb.shape[1], image_rgb.shape[0], QImage.Format_RGB888))
        self.canvas_label.setPixmap(pixmap.scaled(self.canvas_label.width(), self.canvas_label.height(),
                                                  Qt.KeepAspectRatio, Qt.SmoothTransformation))




# 创建应用程序和主窗口
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())