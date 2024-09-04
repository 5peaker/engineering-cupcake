import cv2
import time
import os
from datetime import datetime

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Use MJPG codec

def get_folder_size(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def delete_oldest_folder(root_folder):
    folders = [os.path.join(root_folder, d) for d in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, d))]
    if folders:
        oldest_folder = min(folders, key=os.path.getctime)
        for root, dirs, files in os.walk(oldest_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(oldest_folder)

def start_new_recording():
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    current_hour = datetime.now().strftime('%Y-%m-%d_%H')
    root_folder = "BB"
    os.makedirs(root_folder, exist_ok=True)
    video_folder = os.path.join(root_folder, current_hour)
    os.makedirs(video_folder, exist_ok=True)
    video_name = os.path.join(video_folder, f"{current_time}.avi")
    return cv2.VideoWriter(video_name, fourcc, 30.0, (1280, 720)), time.time(), current_hour, root_folder

out, start_time, current_hour, root_folder = start_new_recording()

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
            out, start_time, current_hour, root_folder = start_new_recording()
        
        # Check if the hour has changed
        new_hour = datetime.now().strftime('%Y-%m-%d_%H')
        if new_hour != current_hour:
            current_hour = new_hour
            out.release()
            out, start_time, current_hour, root_folder = start_new_recording()
        
        # Check if the root folder size exceeds 500MB
        if get_folder_size(root_folder) > 500 * 1024 * 1024:
            delete_oldest_folder(root_folder)
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
