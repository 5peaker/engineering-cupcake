import cv2
import time
import os
from datetime import datetime

cap = cv2.VideoCapture(0)

# 코덱 정의
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# 녹화를 시작하는 함수
def start_new_recording():
    current_hour = datetime.now().strftime('%Y-%m-%d_%H')
    os.makedirs(current_hour, exist_ok=True)
    video_name = f"{current_hour}/{datetime.now().strftime('%Y-%m-%d_%H-%M')}.avi"
    return cv2.VideoWriter(video_name, fourcc, 30.0, (640, 480)), time.time(), current_hour

out, start_time, current_hour = start_new_recording()

while True:
    ret, frame = cap.read()
    if ret:
        out.write(frame)
        cv2.imshow('frame', frame)
        
        # "q" 키를 누르면 화면 녹화를 중단 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # 녹화 시간으로부터 60초가 지났는지를 체크하여, 60초마다 새로운 영상으로 변경
        if time.time() - start_time >= 60:
            out.release()
            out, start_time, current_hour = start_new_recording()
        
        new_hour = datetime.now().strftime('%Y-%m-%d_%H')
        if new_hour != current_hour:
            current_hour = new_hour
            os.makedirs(current_hour, exist_ok=True)
            video_name = f"{current_hour}/{datetime.now().strftime('%Y-%m-%d_%H-%M')}.avi"
            out.release()
            out = cv2.VideoWriter(video_name, fourcc, 60.0, (640, 480))
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()