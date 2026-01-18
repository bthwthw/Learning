'''
Xử lý từng pixel trên ảnh qua các hàm negative, thresholding, log, power 
'''
import cv2
import numpy as np

image_path = r"C:\Users\Thu\OneDrive\Fablab\Project_Reception_Robot\Vision\Learning\tiger.jpg"

img_color = cv2.imread(image_path) # image read -> chuyển ảnh thành ma trận 

img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY) # chuyển màu sang gray (nếu là gray ròi thì nó sẽ giữ nguyên)

#NEGATIVE IMAGE
negative_img = 255 - img_gray

#THRESHOLDING
T = 120
threshold_img = np.zeros_like(img_gray)
for i in range(img_gray.shape[0]): # shape[0] là chiều dọc, height
    for j in range(img_gray.shape[1]): # shape[1] là chiều ngang, width
        if img_gray[i, j] >= T:
            threshold_img[i, j] = 255
        else:
            threshold_img[i, j] = 0
# _, threshold_img_cv = cv2.threshold(img_gray,120,255,cv2.THRESH_BINARY)

#BASIC GRAY LEVEL TRANSFORMATIONS

#Log transformation s = c * log(1 + r)
c = 255 / np.log(1 + np.max(img_gray))  # c là 1 hệ số để đảm báo khi r input lớn nhất thì s cũng cao nhất là 255 
log_img = c * np.log(1 + img_gray)      # áp hàm log lên 
log_img = np.clip(log_img, 0, 255).astype(np.uint8) # đưa về int8 để hiển thị, tại vì c xài phép chia ra thập phân, 
                                                    # nếu hiển thị thì nó ra thập phân sẽ bị lỗi 

#Power law transformation s = c * r^gamma
gamma = 0.6   # gamma < 1: làm sáng vùng tối
c = 1           # này hệ số độ lợi hoi 
gamma_img = c * np.power(img_gray / 255.0, gamma)   # khúc này cái input r phải chia 255 (tại hàm mũ nên nó ra giá trị lớn)
                                                    # không chuẩn hóa về 0 tới 1 thì nó quá lớn, tính toán lâu 
gamma_img = np.clip(gamma_img * 255, 0, 255).astype(np.uint8)   # oke ròi thì mình nhân 255 lại 

cv2.imshow("Original Gray Image", img_gray)
cv2.imshow("Negative Image", negative_img)
cv2.imshow("Threshold Image", threshold_img)
cv2.imshow("Log Transformation", log_img)
cv2.imshow("Gamma Transformation", gamma_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
