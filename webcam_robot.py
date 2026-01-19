# -*- coding: utf-8 -*-
import cv2
import sys

def open_cam_auto(dev_id=0):
    # --- CÁCH 1: GStreamer RAW (Chuẩn nhất cho Jetson) ---
    print("Dang thu Cach 1: GStreamer RAW...")
    gst_raw = (
        "v4l2src device=/dev/video{} ! "
        "video/x-raw, width=640, height=480, framerate=30/1 ! "
        "videoconvert ! appsink"
    ).format(dev_id)
    cap = cv2.VideoCapture(gst_raw, cv2.CAP_GSTREAMER)
    if cap.isOpened(): return cap

    # --- CÁCH 2: GStreamer MJPEG (Cho cam khong ho tro RAW) ---
    print("Cach 1 that bai. Dang thu Cach 2: GStreamer MJPEG...")
    gst_mjpg = (
        "v4l2src device=/dev/video{} ! "
        "image/jpeg, width=640, height=480, framerate=30/1 ! "
        "jpegdec ! videoconvert ! appsink"
    ).format(dev_id)
    cap = cv2.VideoCapture(gst_mjpg, cv2.CAP_GSTREAMER)
    if cap.isOpened(): return cap

    # --- CÁCH 3: V4L2 Thường (Cổ điển) ---
    print("Cach 2 that bai. Dang thu Cach 3: V4L2 thuong...")
    # Thử các backend khác nhau
    cap = cv2.VideoCapture(dev_id) 
    if cap.isOpened(): return cap

    return None

def main():
    cap = open_cam_auto(0)
    
    if cap is None or not cap.isOpened():
        print("\nCHOT LAI: Khong mo duoc Camera bang moi cach!")
        print("Hay thu rut Camera ra cam lai hoac check lenh v4l2-ctl.")
        return

    print("\n>>> DA KET NOI CAMERA THANH CONG! <<<")
    print("Nhan Ctrl+C de thoat...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Loi: Mat ket noi hinh anh!")
            break
            
        # Code xử lý của bạn ở đây...
        # ...
        
        # Test lưu ảnh
        cv2.imwrite("test_success.jpg", frame)

if __name__ == "__main__":
    main()