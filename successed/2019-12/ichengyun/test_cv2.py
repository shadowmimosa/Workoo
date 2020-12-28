import cv2
import numpy as np


def binary(src, name, low_hsv, high_hsv):
    cv2.namedWindow(f'input-{name}', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(f'input-{name}', src)

    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)

    cv2.imshow(f'output-{name}', mask)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()


def change():
    img = cv2.imread(r'raw.png')
    new_img = cv2.resize(img, None, fx=1.2, fy=1.2)

    rows, cols, channels = new_img.shape
    print(rows, cols, channels)

    # 显示图像
    cv2.imshow('new_img', new_img)

    # 将图片转换为灰度图片
    gray_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2HSV)

    # 图片二值化处理
    low_value = np.array([90, 70, 70])
    high_value = np.array([110, 255, 255])
    binary_img = cv2.inRange(gray_img, low_value, high_value)

    # 腐蚀膨胀
    erode = cv2.erode(binary_img, None, iterations=1)
    dilate = cv2.dilate(erode, None, iterations=1)
    # cv2.imshow('dilate', dilate)

    # 遍历替换
    for i in range(rows):
        for j in range(cols):
            if dilate[i, j] == 255:
                # 此处替换颜色，为BGR通道
                new_img[i, j] = (0, 0, 255
                                 )  # (0, 0, 255)替换为红底 (255, 255, 255)替换为白底

    cv2.imshow('red_bg_img', new_img)
    # 窗口等待命令 0表示无限等待
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def replace_color():
    img = cv2.imread('raw.png')

    # 将图像转换为HSV像素空间，因为HSV空间对颜色比较敏感
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 分别设置HSV颜色空间中，红色、黄色、蓝色、绿色的阈值
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])

    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([34, 255, 255])

    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])

    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])

    lower_orange = np.array([11, 43, 46])
    upper_orange = np.array([25, 255, 255])

    lower_solid_red = np.array([0, 255, 255])
    upper_solid_red = np.array([0, 255, 255])

    # 使用inRange函数获取图像中目标颜色的索引
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_solid_red = cv2.inRange(hsv, lower_solid_red, upper_solid_red)

    img_mask = np.copy(img)

    color_1 = [128, 9, 21]
    color_2 = [50, 14, 77]
    color_3 = [61, 154, 124]
    color_4 = [59, 170, 246]
    color_5 = [59, 170, 246]

    white_color = [255, 255, 255]
    # 给目标像素赋值
    # img_mask[mask_red != 0] = color_1
    # img_mask[mask_blue != 0] = color_2
    # img_mask[mask_green != 0] = color_3
    # img_mask[mask_green != 0] = color_3
    # img_mask[mask_yellow != 0] = color_4
    img_mask[mask_orange != 0] = white_color
    img_mask[mask_solid_red != 0] = white_color

    cv2.imshow('output', img_mask)
    cv2.waitKey(0)


def rgb2hsv(r, g, b, cv2=True):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    m = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g - b) / m) * 60
        else:
            h = ((g - b) / m) * 60 + 360
    elif mx == g:
        h = ((b - r) / m) * 60 + 120
    elif mx == b:
        h = ((r - g) / m) * 60 + 240
    if mx == 0:
        s = 0
    else:
        s = m / mx
    v = mx
    if cv2:
        H = h / 2
        S = s * 255.0
        V = v * 255.0
        return H, S, V
    return h, s, v


# (95.51020408163265, 208.25, 60.0)
if __name__ == "__main__":
    # change()
    print(rgb2hsv(255, 0, 0))
    replace_color()
    src = cv2.imread("raw.png")

    # red
    low_hsv = np.array([0, 43, 46])
    high_hsv = np.array([10, 255, 255])
    binary(src, 'red', low_hsv, high_hsv)

    # # black
    # low_hsv = np.array([0, 0, 46])
    # high_hsv = np.array([180, 43, 220], )
    # binary(src, 'black', low_hsv, high_hsv)

    # black
    low_hsv = np.array([90, 200, 55])
    high_hsv = np.array([100, 210, 65])
    binary(src, 'black', low_hsv, high_hsv)

    # white
    low_hsv = np.array([0, 0, 221])
    high_hsv = np.array([180, 30, 255])
    binary(src, 'white', low_hsv, high_hsv)
