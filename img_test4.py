'''
Xử lý cắt và vẽ lên ảnh 
'''
import cv2 
import numpy as np 

path = 'tiger.jpg'
img = cv2.imread(path)

# hàm shape sẽ trả về 3 giá trị: height, width với số kênh màu 
h, w, c = img.shape 

# onefourth_img = img[0 : h//2, 0 : w//2] # dùng // để lấy số nguyên và cột trước hàng sau 
# cv2.imshow("First Quarter", onefourth_img)

center_img = img[h//4 : 3*h//4, w//4 : 3*w//4]
cv2.imshow("Center", center_img)

# vẽ 1 đường từ điểm x,y = w//4,0 đến x,y = w//4,h -> line dọc 
cv2.line(img, (w//4,0), (w//4,h), (128, 0, 255), 2)
cv2.imshow("Input", img)

cv2.waitKey(0)
cv2.destroyAllWindows()