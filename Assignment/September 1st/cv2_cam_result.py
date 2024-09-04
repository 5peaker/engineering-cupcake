import cv2
import time
import os
from datetime import datetime

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

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
        
        # Add this line to process window events and check for "q" key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Check if 60 seconds have passed
        if time.time() - start_time >= 60:
            out.release()
            out, start_time, current_hour = start_new_recording()
        
        # Check if the hour has changed
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