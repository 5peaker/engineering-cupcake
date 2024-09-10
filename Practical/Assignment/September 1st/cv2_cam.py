import cv2
import os
import datetime

# Set up video capture from the webcam
cap = cv2.VideoCapture(0)

# Create a directory to store video files
output_dir = "recorded_videos"
os.makedirs(output_dir, exist_ok=True)

# Initialize variables for time-based folder management
current_hour = None
current_folder = None
max_folder_size_mb = 500

def create_new_folder():
    now = datetime.datetime.now()
    folder_name = now.strftime("%Y-%m-%d_%H")
    folder_path = os.path.join(output_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def check_folder_size(folder_path):
    folder_size = sum(os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path))
    return folder_size / (1024 * 1024)  # Convert to megabytes

def delete_oldest_folder():
    folders = sorted(os.listdir(output_dir))
    if len(folders) > 0:
        oldest_folder = os.path.join(output_dir, folders[0])
        os.rmdir(oldest_folder)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Get the current timestamp
    now = datetime.datetime.now()

    # Check if a new hour has started
    if current_hour != now.hour:
        current_hour = now.hour
        current_folder = create_new_folder()

    # Define the video file name
    video_filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".avi"
    video_path = os.path.join(current_folder, video_filename)

    # Write the frame to the video file
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"XVID"), 30, (frame.shape[1], frame.shape[0]))
    out.write(frame)

    # Check folder size and create a TXT file if necessary
    if check_folder_size(current_folder) > max_folder_size_mb:
        txt_filename = "folder_size_exceeded.txt"
        txt_path = os.path.join(current_folder, txt_filename)
        with open(txt_path, "w") as txt_file:
            txt_file.write("Folder size exceeded 500 MB.")

        # Delete the oldest folder
        delete_oldest_folder()

    # Display the frame (optional)
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
