''' 
Dung filter len webcam
'''

import cv2

cap = cv2.VideoCapture(0)
while True:
    ret, fr = cap.read()
    gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)

    cv2.imshow ("Output", gray)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()