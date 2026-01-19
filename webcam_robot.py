# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time

# Load XML
try:
    path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
except AttributeError:
    path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(path)

def open_cam_csi():
    # Đây là chuỗi lệnh "Thần thánh" dành riêng cho Cam BG10 trên Jetson
    gst_str = (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! "
        "nvvidconv ! "
        "video/x-raw, width=640, height=360, format=BGRx ! " # Resize xuống nhỏ để detect cho nhanh
        "videoconvert ! "
        "video/x-raw, format=BGR ! "
        "appsink"
    )
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

def main():
    print(">>> DANG KET NOI CAMERA CSI (IMX219) <<<")
    cap = open_cam_csi()
    
    if not cap.isOpened():
        print("Loi: Van khong mo duoc! Kiem tra lai day cap CSI.")
        return

    print(">>> KET NOI THANH CONG! <<<")
    print("Nhan Ctrl+C de thoat...")

    count = 0
    cmd = "DUNG YEN"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Mat tin hieu camera!")
            break

        # Code xử lý cũ của bạn
        # Lật ảnh (Vì cam CSI thường bị ngược)
        frame = cv2.flip(frame, 0) # Thử 0 hoặc 1 hoặc -1 nếu bị ngược đầu
        frame = cv2.flip(frame, 1) # Lật tiếp gương
        
        height, width = frame.shape[:2]
        center_x = width // 2
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Logic điều khiển
        deadzone = 50
        if len(faces) > 0:
            faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
            (x, y, w, h) = faces[0]
            face_center_x = x + w // 2
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            error = face_center_x - center_x
            if abs(error) < deadzone: cmd = "DI THANG"
            elif error < 0: cmd = "<<< RE TRAI"
            else: cmd = "RE PHAI >>>"
            
            print("Lenh: " + cmd + " | Error: " + str(error))

        # Lưu ảnh check
        count += 1
        if count % 10 == 0:
            cv2.putText(frame, "CMD: " + cmd, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imwrite("csi_cam_view.jpg", frame)
            if count > 1000: count = 0

    cap.release()

if __name__ == "__main__":
    main()