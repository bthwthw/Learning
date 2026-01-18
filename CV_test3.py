'''
Áp dụng bộ lọc kernel vào ảnh dùng hàm của cv2 
+ filter2D() dùng cho kernel mình tự chế 
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = r"C:\Users\Thu\OneDrive\Fablab\Project_Reception_Robot\Vision\Learning\xuong.png"

img_color = cv2.imread(image_path)
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

kernel = np.array([
    [0, 1, 0],
    [0, 0, 0],
    [0,-1, 0]
], dtype=np.float32)

image_output=cv2.filter2D(img_gray, -1, kernel, anchor=(-1, -1), delta=0, borderType=cv2.BORDER_DEFAULT)
