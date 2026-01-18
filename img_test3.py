'''
Áp dụng bộ lọc kernel vào ảnh dùng hàm của cv2 
https://opencv.org/blog/image-filtering-using-convolution-in-opencv/
+ filter2D() dùng cho kernel mình tự chế 
+ các thể loại blur như blur (trung bình cộng), GaussianBlur (Phân phối chuẩn), medianBlur(Trung vị), bilateralBlur (Lọc song phương)
+ các thể loại edge-detect như Sobel (đạo hàm), Laplacian (đạo hàm bậc 2), Canny
+ sharpen thì phải dùng custom chứ cv2 k hỗ trợ 
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = r"C:\Users\Thu\OneDrive\Fablab\Project_Reception_Robot\Vision\Learning\tiger.jpg"
img_bgr = cv2.imread(image_path)
# img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# LƯU Ý: Matplotlib hiển thị hệ màu RGB, còn OpenCV đọc là BGR
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
img_gray = img_rgb

custom_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
], dtype=np.float32) # kernel này là sharpen kernel 

custom_image=cv2.filter2D(img_gray, -1, custom_kernel, anchor=(-1, -1), delta=0, borderType=cv2.BORDER_DEFAULT)
# borderType thì default k phải là viền bằng 0 nha, constant mới bằng 0, này nó là cái gì á, mặc định 

'''blur'''
blur_image = cv2.boxFilter(img_gray, -1, (3,3), normalize=True) # or cv2.blur(img_gray,(3,3))

gaussian = cv2.GaussianBlur(img_gray, (7, 7), 0)

median = cv2.medianBlur(img_gray, 7)

bilateral = cv2.bilateralFilter(img_gray, 9, 75, 75)

'''edge detect (cần làm mờ để loại bỏ nhiễu trước khi edge-detect)'''
edge_input = gaussian

# Edge-detect thi no co am duong 
sobelx = cv2.Sobel(edge_input,ddepth=cv2.CV_64F,dx=1,dy=0,ksize=3)
sobely = cv2.Sobel(edge_input,cv2.CV_64F,dx=0,dy=1,ksize=3)
# Chuyển lại về dạng ảnh không dấu (uint8) để hiển thị
abs_sobelx = cv2.convertScaleAbs(sobelx)
abs_sobely = cv2.convertScaleAbs(sobely)
# Gộp 2 hướng lại để ra ảnh Sobel hoàn chỉnh
sobel_image = cv2.addWeighted(abs_sobelx, 0.5, abs_sobely, 0.5, 0)

laplacian = cv2.Laplacian(edge_input, cv2.CV_64F)
laplacian_image = cv2.convertScaleAbs(laplacian)

canny_image = cv2.Canny(edge_input, 50, 150)

fig, axs = plt.subplots(2, 4, figsize=(15, 8)) # fig gồm 2 hàng, 4 đồ thị (ma tran 2x4)
axs = axs.flatten() # trai thang ra thanh vector 

images = [blur_image, gaussian, median, bilateral, custom_image, sobel_image, laplacian_image, canny_image]
titles = ["Box Filter", "Gaussian Blur", "Median Blur", "Bilateral", "Custom Sharpen", "Sobel", "Laplacian", "Canny"]

for i in range(8):
    # Nếu ảnh là ảnh xám cần set cmap='gray' 
    # Nếu ảnh màu matplotlib tự hiểu
    if len(images[i].shape) == 2: # Kiểm tra xem có phải ảnh xám k
        axs[i].imshow(images[i], cmap='gray')
    else:
        axs[i].imshow(images[i])
        
    axs[i].set_title(titles[i])
    axs[i].axis('off')

plt.tight_layout()
plt.show()