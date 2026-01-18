''' 
Dung filter len webcam
'''

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while True:
    ret, fr = cap.read()
    gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    cv2.imshow ("Gray", gray)
    
    custom_kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ], dtype=np.float32) # kernel này là sharpen kernel 
    custom_sharp = cv2.filter2D(gray, -1, custom_kernel, anchor=(-1, -1), delta=0, borderType=cv2.BORDER_DEFAULT)
    # cv2.imshow ("Sharpen", custom_sharp)

    gaussian = cv2.GaussianBlur(gray, (7, 7), 0)
    # cv2.imshow ("Gblur", gaussian)

    edge_input = gaussian 
    sobelx = cv2.Sobel(edge_input,ddepth=cv2.CV_64F,dx=1,dy=0,ksize=3)
    sobely = cv2.Sobel(edge_input,cv2.CV_64F,dx=0,dy=1,ksize=3)
    abs_sobelx = cv2.convertScaleAbs(sobelx)
    abs_sobely = cv2.convertScaleAbs(sobely)
    sobel_image = cv2.addWeighted(abs_sobelx, 0.5, abs_sobely, 0.5, 0)
    cv2.imshow("Edge Sobel", sobel_image)
    
    canny_image = cv2.Canny(edge_input, 50, 150)
    cv2.imshow("Edge Canny", canny_image)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()