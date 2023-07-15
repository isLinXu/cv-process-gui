import cv2
import json
import PySimpleGUI as sg
from cvlibs.process_fun import *

# GUI布局
layout = [
    [sg.Image(filename="", key="-IMAGE-ORIGINAL-"), sg.Image(filename="", key="-IMAGE-PROCESSED-")],
    [sg.Text("图像处理工具")],
    [sg.Button("打开图片", key="-OPEN-"), sg.Button("保存图片", key="-SAVE-"),
     sg.Button("打开JSON", key="-OPENJSON-"),
     sg.Button("复原", key="-RESET-"),
     sg.Button("灰度", key="-GRAYSCALE-"),
     sg.Button("旋转", key="-ROTATE-"),
     sg.Button("缩小", key="-SCALE-"),
     sg.Button("翻转", key="-FLIP-"),
     sg.Button("高斯模糊", key="-BLUR-"),
     sg.Button("对比度调整", key="-CONTRAST-"),
     sg.Button("亮度调整", key="-BRIGHTNESS-"),],
    [sg.Button("Canny边缘检测", key="-CANNY-"),
     sg.Button("阈值处理", key="-THRESHOLD-"),
     sg.Button("平滑", key="-SMOOTH-"),
     sg.Button("形态学操作", key="-MORPHOLOGY-"),
     sg.Button("直方图均衡化", key="-EQUALIZEHIST-"),
     sg.Button("Sobel边缘检测", key="-SOBEL-"),
     sg.Button("Laplacian边缘检测", key="-LAPLACIAN-"),
     sg.Button("Scharr边缘检测", key="-SCHARR-"),
     sg.Button("图像金字塔", key="-PYRAMID-"),],
    [sg.Button("轮廓检测", key="-CONTOURS-"),
     sg.Button("模板匹配", key="-TEMPLATE-"),
     sg.Button("Hough线变换", key="-HOUGHLINES-"),
     sg.Button("Hough圆变换", key="-HOUGHCIRCLES-"),
     sg.Button("图像缝合", key="-STITCH-"),
     sg.Button("均值模糊", key="-AVERAGEBLUR-"),
     sg.Button("双边滤波", key="-BILATERALFILTER-"),
     sg.Button("仿射变换", key="-WARP-"),
     sg.Button("计算直方图", key="-HISTOGRAM-"),
     sg.Button("全局阈值二值化", key="-GLOBALTHRESH-"), ],
    [sg.Button("自适应阈值二值化", key="-ADAPTIVETHRESH-"),
     sg.Button("通道分离", key="-SPLIT-"),
     sg.Button("通道合并", key="-MERGE-"),
     sg.Button("色彩空间转换", key="-CONVERTCOLOR-"),
     sg.Button("Otsu阈值法", key="-OTSU-"),
     sg.Button("图像形状检测", key="-SHAPES-"),
     sg.Button("退出", key="-EXIT-")],
]

window = sg.Window("Image Processing GUI(©️islinxu)", layout)

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
        else:
            sg.popup("请先打开图片")
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
        else:
            sg.popup("请先打开图片")
    elif event == "-ROTATE-":
        if img_processed is not None:
            angle = sg.popup_get_text("输入旋转角度")
            if angle:
                img_processed = rotate(img_processed, float(angle))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-SCALE-":
        if img_processed is not None:
            factor = sg.popup_get_text("输入缩放因子（0-1）")
            if factor:
                img_processed = scale(img_processed, float(factor))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-FLIP-":
        if img_processed is not None:
            direction = sg.popup_get_text("输入翻转方向（0: 垂直, 1: 水平, -1: 垂直和水平）")
            if direction:
                img_processed = flip(img_processed, int(direction))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-BLUR-":
        if img_processed is not None:
            ksize = sg.popup_get_text("输入高斯模糊核大小（奇数）")
            if ksize:
                img_processed = gaussian_blur(img_processed, int(ksize))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-CONTRAST-":
        if img_processed is not None:
            alpha = sg.popup_get_text("输入对比度调整系数（推荐范围：1.0-3.0）")
            if alpha:
                img_processed = adjust_contrast_brightness(img_processed, float(alpha), 0)
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-BRIGHTNESS-":
        if img_processed is not None:
            beta = sg.popup_get_text("输入亮度调整值（推荐范围：-100 - 100）")
            if beta: img_processed = adjust_contrast_brightness(img_processed, 1, int(beta))
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-CANNY-":
        if img_processed is not None:
            low_threshold = sg.popup_get_text("输入Canny边缘检测低阈值")
            high_threshold = sg.popup_get_text("输入Canny边缘检测高阈值")
            if low_threshold and high_threshold:
                img_processed = canny_edge_detection(img_processed, int(low_threshold), int(high_threshold))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-THRESHOLD-":
        if img_processed is not None:
            thresh_value = sg.popup_get_text("输入阈值处理阈值")
            if thresh_value: img_processed = threshold(img_processed, int(thresh_value))
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-SMOOTH-":
        if img_processed is not None:
            ksize = sg.popup_get_text("输入平滑核大小（奇数）")
            if ksize:
                img_processed = smooth(img_processed, int(ksize))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-MORPHOLOGY-":
        if img_processed is not None:
            operation = sg.popup_get_listbox("选择形态学操作", ["膨胀", "腐蚀"])
            ksize = sg.popup_get_text("输入形态学操作核大小")
            if operation and ksize:
                operation_map = {"膨胀": cv2.MORPH_DILATE, "腐蚀": cv2.MORPH_ERODE}
                img_processed = morphology(img_processed, operation_map[operation[0]], int(ksize))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-EQUALIZEHIST-":
        if img_processed is not None:
            img_processed = equalize_histogram(img_processed)
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-SOBEL-":
        if img_processed is not None:
            dx = sg.popup_get_text("输入Sobel边缘检测dx值")
            dy = sg.popup_get_text("输入Sobel边缘检测dy值")
            ksize = sg.popup_get_text("输入Sobel边缘检测核大小（奇数）")
            if dx and dy and ksize:
                img_processed = sobel_edge_detection(img_processed, int(dx), int(dy), int(ksize))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-LAPLACIAN-":
        if img_processed is not None:
            ksize = sg.popup_get_text("输入Laplacian边缘检测核大小（奇数）")
            if ksize:
                img_processed = laplacian_edge_detection(img_processed, int(ksize))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-SCHARR-":
        if img_processed is not None:
            dx = sg.popup_get_text("输入Scharr边缘检测dx值")
            dy = sg.popup_get_text("输入Scharr边缘检测dy值")
            if dx and dy:
                img_processed = scharr_edge_detection(img_processed, int(dx), int(dy))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-PYRAMID-":
        if img_processed is not None:
            # operation = sg.popup_get_listbox("选择图像金字塔操作", ["上采样", "下采样"])
            level = sg.popup_get_text("输入图像金字塔层数")
            if operation and level:
                img_processed = pyramid(img_processed, operation[0], int(level))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")

    elif event == "-CONTOURS-":
        if img_processed is not None:
            img_processed = find_contours(img_processed)
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-TEMPLATE-":
        if img_processed is not None:
            template_path = sg.popup_get_file("选择模板图片")
            if template_path:
                img_processed = template_matching(img_processed, template_path)
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-HOUGHLINES-":
        if img_processed is not None:
            img_processed = hough_lines(img_processed)
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")
    elif event == "-HOUGHCIRCLES-":
        if img_processed is not None:
            img_processed = hough_circles(img_processed)
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")


    elif event == "-BLEND-":
        if img_processed is not None:
            img2_path = sg.popup_get_file("选择第二张图片")
            if img2_path:
                img2 = open_image(img2_path)
                alpha = sg.popup_get_text("输入图像融合系数（推荐范围：0-1）")
                if alpha:
                    img_processed = blend_images(img_processed, img2, float(alpha))
                    window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))

    elif event == "-STITCH-":
        if img_processed is not None:
            img2_path = sg.popup_get_file("选择第二张图片")
            if img2_path:
                img2 = open_image(img2_path)
                img_processed = stitch_images(img_processed, img2)
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))
        else:
            sg.popup("请先打开图片")

    elif event == "-AVERAGEBLUR-":
        if img_processed is not None:
            ksize = sg.popup_get_text("输入均值模糊核大小（奇数）")
            if ksize:
                img_processed = average_blur(img_processed, int(ksize))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))


    elif event == "-BILATERALFILTER-":
        if img_processed is not None:
            d = sg.popup_get_text("输入双边滤波直径")
            sigma_color = sg.popup_get_text("输入双边滤波颜色标准差")
            sigma_space = sg.popup_get_text("输入双边滤波空间标准差")
            if d and sigma_color and sigma_space:
                img_processed = bilateral_filter(img_processed, int(d), int(sigma_color),int(sigma_space))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))

    elif event == "-WARP-":
        if img_processed is not None:
            M = np.float32([[1, 0, 100], [0, 1, 50]])
            img_processed = warp_affine_transform(img_processed, M)
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))

    elif event == "-HISTOGRAM-":
        if img_processed is not None:
            compute_histogram(img_processed)

    elif event == "-GLOBALTHRESH-":
        if img_processed is not None:
            thresh_value = sg.popup_get_text("输入全局阈值")
            if thresh_value:
                img_processed = global_threshold(img_processed, int(thresh_value))
                window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))

    elif event == "-ADAPTIVETHRESH-":
        if img_processed is not None:
            img_processed = adaptive_threshold(img_processed)
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))

    elif event == "-SHAPES-":
        if img_processed is not None:
            img_processed = detect_shapes(img_processed)
            window["-IMAGE-PROCESSED-"].update(data=convert_image_to_bytes(img_processed))

window.close()
