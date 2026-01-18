# -*- coding: utf-8 -*-
import cv2
import numpy as np

# --- CẤU HÌNH ---
# Nếu máy báo lỗi không tìm thấy file xml, hãy tải file xml về để cùng thư mục
# và sửa dòng dưới thành: face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
try:
    path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
except AttributeError:
    # Dự phòng cho OpenCV đời cũ trên Python 2
    path = 'haarcascade_frontalface_default.xml'

face_cascade = cv2.CascadeClassifier(path)

def main():
    # Mở Webcam (số 0 hoặc 1 tùy máy Jetson)
    cap = cv2.VideoCapture(0, 200)
    
    if not cap.isOpened():
        print("Loi: Khong mo duoc Camera!")
        return

    deadzone = 50 
    print("Robot Logic Started... Nhan 'q' de thoat.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Lật ảnh
        frame = cv2.flip(frame, 1)
        
        # Python 2 trả về tuple (h, w, c)
        height, width = frame.shape[:2]
        center_x = width // 2

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Vẽ vạch
        cv2.line(frame, (center_x - deadzone, 0), (center_x - deadzone, height), (0, 255, 255), 2)
        cv2.line(frame, (center_x + deadzone, 0), (center_x + deadzone, height), (0, 255, 255), 2)

        cmd = "DUNG YEN"
        color = (100, 100, 100)

        if len(faces) > 0:
            # Python 2 vẫn chạy tốt logic này
            faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
            (x, y, w, h) = faces[0]
            
            face_center_x = x + w // 2
            face_center_y = y + h // 2
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.circle(frame, (face_center_x, face_center_y), 5, (0, 0, 255), -1)

            error = face_center_x - center_x
            
            if abs(error) < deadzone:
                cmd = "DI THANG"
                color = (0, 255, 0)
            elif error < 0:
                cmd = "<<< RE TRAI"
                color = (0, 0, 255)
            else:
                cmd = "RE PHAI >>>"
                color = (0, 0, 255)
                
            # Python 2 kén f-string, dùng format kiểu cũ cho chắc
            cv2.putText(frame, "Error: " + str(error) + " px", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.putText(frame, "CMD: " + cmd, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

        cv2.imshow('Robot Vision Simulator', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()