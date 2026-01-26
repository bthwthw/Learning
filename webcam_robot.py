import cv2
import numpy as np

# Load bộ nhận diện khuôn mặt có sẵn của OpenCV (nhẹ, không cần cài thêm)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def main():
    # Mở Webcam laptop (số 0)
    cap = cv2.VideoCapture(0)
    
    # Giả lập thông số Robot
    # Giả sử khung hình là 640 pixel. Tâm là 320.
    # Vùng an toàn (Deadzone) là +- 50 pixel ở giữa.
    deadzone = 50 

    print("Robot Logic Started... Nhấn 'q' để thoát.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Lật ngược ảnh cho giống gương (để bạn dễ điều khiển trái phải)
        frame = cv2.flip(frame, 1)
        
        height, width, _ = frame.shape
        center_x = width // 2

        # Chuyển ảnh xám để nhận diện
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Phát hiện khuôn mặt
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Vẽ 2 vạch kẻ phân chia vùng Trái - Giữa - Phải
        cv2.line(frame, (center_x - deadzone, 0), (center_x - deadzone, height), (0, 255, 255), 2)
        cv2.line(frame, (center_x + deadzone, 0), (center_x + deadzone, height), (0, 255, 255), 2)

        cmd = "DUNG YEN (Searching...)"
        color = (100, 100, 100)

        if len(faces) > 0:
            # Lấy khuôn mặt to nhất (gần nhất)
            (x, y, w, h) = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[0]
            
            # Tính tâm khuôn mặt
            face_center_x = x + w // 2
            face_center_y = y + h // 2
            
            # Vẽ hình vuông quanh mặt
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.circle(frame, (face_center_x, face_center_y), 5, (0, 0, 255), -1)

            # --- LOGIC ĐIỀU KHIỂN ROBOT ---
            error = face_center_x - center_x
            
            if abs(error) < deadzone:
                cmd = "DI THANG (Forward)"
                color = (0, 255, 0) # Xanh lá
            elif error < 0:
                cmd = "<<< RE TRAI (Turn Left)"
                color = (0, 0, 255) # Đỏ
            else:
                cmd = "RE PHAI (Turn Right) >>>"
                color = (0, 0, 255) # Đỏ
                
            # Hiện thông số sai số (Error)
            cv2.putText(frame, f"Error: {error} px", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Hiện lệnh điều khiển lên màn hình
        cv2.putText(frame, f"CMD: {cmd}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

        cv2.imshow('Robot Vision Simulator', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()