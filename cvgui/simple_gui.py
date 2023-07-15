import cv2
import json
import PySimpleGUI as sg
from cvlibs.process_fun import *

# GUI布局
layout = [
    [sg.Image(filename="", key="-IMAGE-ORIGINAL-"), sg.Image(filename="", key="-IMAGE-PROCESSED-")],
    [sg.Text("图像处理工具")],
    [sg.Button("打开图片", key="-OPEN-"), sg.Button("保存图片", key="-SAVE-"), sg.Button("打开JSON", key="-OPENJSON-"), sg.Button("灰度", key="-GRAYSCALE-"), sg.Button("旋转", key="-ROTATE-"), sg.Button("缩小", key="-SCALE-"), sg.Button("翻转", key="-FLIP-"), sg.Button("高斯模糊", key="-BLUR-"), sg.Button("对比度调整", key="-CONTRAST-"), sg.Button("亮度调整", key="-BRIGHTNESS-"), sg.Button("Canny边缘检测", key="-CANNY-"), sg.Button("阈值处理", key="-THRESHOLD-"), sg.Button("退出", key="-EXIT-")],
]

window = sg.Window("图像处理", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "-EXIT-":
        break
    elif event == "-OPEN-":
        file_path = sg.popup_get_file("选择图片文件")
        if file_path:
            img_original = open_image(file_path)
            img_processed = img_original.copy()
            window["-IMAGE-ORIGINAL-"].update(data=convert_image_to_bytes(img_original))
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
    elif event == "-SAVE-":
        if img_processed is not None:
            save_path = sg.popup_get_file("保存图片", save_as=True, default_extension=".png")
            if save_path:
                cv2.imwrite(save_path, img_processed)
                sg.popup("图片已保存")
    elif event == "-OPENJSON-":
        json_path = sg.popup_get_file("选择JSON标签文件")
        if json_path:
            with open(json_path, "r") as f:
                json_data = json.load(f)
            sg.popup("JSON文件已加载")
    elif event == "-GRAYSCALE-":
        if img_processed is not None:
            img_processed = grayscale(img_processed)
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
    elif event == "-ROTATE-":
        if img_processed is not None:
            angle = sg.popup_get_text("输入旋转角度")
            if angle:
                img_processed = rotate(img_processed, float(angle))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
    elif event == "-SCALE-":
        if img_processed is not None:
            factor = sg.popup_get_text("输入缩放因子（0-1）")
            if factor:
                img_processed = scale(img_processed, float(factor))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
    elif event == "-FLIP-":
        if img_processed is not None:
            direction = sg.popup_get_text("输入翻转方向（0: 垂直, 1: 水平, -1: 垂直和水平）")
            if direction:
                img_processed = flip(img_processed, int(direction))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
    elif event == "-BLUR-":
        if img_processed is not None:
            ksize = sg.popup_get_text("输入高斯模糊核大小（奇数）")
            if ksize:
                img_processed = gaussian_blur(img_processed, int(ksize))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
    elif event == "-CONTRAST-":
        if img_processed is not None:
            alpha = sg.popup_get_text("输入对比度调整系数（推荐范围：1.0-3.0）")
            if alpha:
                img_processed = adjust_contrast_brightness(img_processed, float(alpha), 0)
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
    elif event == "-BRIGHTNESS-":
        if img_processed is not None:
            beta = sg.popup_get_text("输入亮度调整值（推荐范围：-100 - 100）")
            if beta: img_processed = adjust_contrast_brightness(img_processed, 1, int(beta))
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
    elif event == "-CANNY-":
        if img_processed is not None:
            low_threshold = sg.popup_get_text("输入Canny边缘检测低阈值")
            high_threshold = sg.popup_get_text("输入Canny边缘检测高阈值")
            if low_threshold and high_threshold:
                img_processed = canny_edge_detection(img_processed, int(low_threshold), int(high_threshold))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
    elif event == "-THRESHOLD-":
        if img_processed is not None:
            thresh_value = sg.popup_get_text("输入阈值处理阈值")
            if thresh_value: img_processed = threshold(img_processed, int(thresh_value))
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))

window.close()