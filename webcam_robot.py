# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time

# --- CẤU HÌNH LOAD XML ---
try:
    path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
except AttributeError:
    path = 'haarcascade_frontalface_default.xml'

face_cascade = cv2.CascadeClassifier(path)

def open_cam_on_jetson(sensor_id=0):
    # Thử pipeline YUYV (Raw) trước vì nó tương thích với mọi loại cam rẻ tiền
    # MJPEG nhanh hơn nhưng nhiều cam không hỗ trợ sẽ gây lỗi "Internal data stream"
    gst_str = (
        "v4l2src device=/dev/video{} ! "
        "video/x-raw, width=640, height=480, framerate=30/1 ! " 
        "videoconvert ! "
        "appsink"
    ).format(sensor_id)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

def main():
    cap = open_cam_on_jetson(0)
    
    if not cap.isOpened():
        print("Loi: Khong mo duoc Camera! Kiem tra lai day cam.")
        return

    deadzone = 50 
    print("------------------------------------------------")
    print("Robot Logic Started... (Chay ngam, khong hien cua so)")
    print("Bam Ctrl + C de thoat.")
    print("------------------------------------------------")

    # Biến đếm để không lưu ảnh liên tục (hại thẻ nhớ)
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret: 
            print("Khong doc duoc hinh tu Camera!")
            break

        # Lật ảnh
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        center_x = width // 2

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Vẽ vạch vùng an toàn
        cv2.line(frame, (center_x - deadzone, 0), (center_x - deadzone, height), (0, 255, 255), 2)
        cv2.line(frame, (center_x + deadzone, 0), (center_x + deadzone, height), (0, 255, 255), 2)

        cmd = "DUNG YEN"
        
        if len(faces) > 0:
            faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
            (x, y, w, h) = faces[0]
            
            face_center_x = x + w // 2
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            error = face_center_x - center_x
            
            if abs(error) < deadzone:
                cmd = "DI THANG"
            elif error < 0:
                cmd = "<<< RE TRAI"
            else:
                cmd = "RE PHAI >>>"
                
            # In ra màn hình Terminal (Đây là giao diện chính khi SSH)
            print("Phat hien mat! Lenh: " + cmd + " | Error: " + str(error))
        else:
            # print("Dang tim kiem...") # Bỏ comment nếu muốn spam màn hình
            pass

        # --- QUAN TRỌNG: Lưu ảnh thay vì hiện ảnh ---
        # Cứ mỗi 10 khung hình (tầm 0.3 giây) thì lưu file 1 lần để xem
        count += 1
        if count % 10 == 0:
            cv2.putText(frame, "CMD: " + cmd, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.imwrite("camera_view.jpg", frame)
            # Reset biến đếm để tránh tràn số (dù rất lâu mới tràn)
            if count > 1000: count = 0

    cap.release()

if __name__ == "__main__":
    main()