import cv2
import os
import datetime

# 컴퓨터 내장 카메라를 사용한다
cap = cv2.VideoCapture(0)

# 저장된 영상을 담을 폴더를 지정한다
output_dir = "recorded_videos"
os.makedirs(output_dir, exist_ok=True)

# 폴더 관리를 위한 변수들을 초기화
current_hour = None
current_folder = None

# 폴더의 최대 용량을 정의 (폴더 용량이 더 커지면 가장 옛날 서브폴더를 삭제)
max_folder_size_mb = 500

# 새로운 폴더를 만드는 함수
def create_new_folder():
    now = datetime.datetime.now()
    folder_name = now.strftime("%Y-%m-%d_%H")
    folder_path = os.path.join(output_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

# 폴더 사이즈를 체크하는 함수
def check_folder_size(folder_path):
    folder_size = sum(os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path))
    return folder_size / (1024 * 1024)  # Convert to megabytes

# 용량 한계가 넘으면 가장 옛날 서브폴더를 삭제하는 함수
def delete_oldest_folder():
    folders = sorted(os.listdir(output_dir))
    if len(folders) > 0:
        oldest_folder = os.path.join(output_dir, folders[0])
        os.rmdir(oldest_folder)

while True:
    ret, frame = cap.read()

    # 현재 시간을 체크 
    now = datetime.datetime.now()

    # 시(단위)가 달라지면 새로운 폴더 생성
    if current_hour != now.hour:
        current_hour = now.hour
        current_folder = create_new_folder()

    # 저장할 파일 이름 정의 
    video_filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".avi"
    video_path = os.path.join(current_folder, video_filename)

    # 출력할 프레임 정의 
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"XVID"), 30, (frame.shape[1], frame.shape[0]))
    out.write(frame)

    # 폴더 사이즈 체크 
    if check_folder_size(current_folder) > max_folder_size_mb:
        txt_filename = "folder_size_exceeded.txt"
        txt_path = os.path.join(current_folder, txt_filename)
        with open(txt_path, "w") as txt_file:
            txt_file.write("Folder size exceeded 500 MB.")

        # 서브폴더 삭제
        delete_oldest_folder()

    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 카메라 사용을 끝내고 창을 닫는 함수
cap.release()
cv2.destroyAllWindows()
