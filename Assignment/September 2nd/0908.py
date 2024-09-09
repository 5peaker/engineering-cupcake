import cv2
import numpy as np

# 전역 변수 설정
points = []

# 마우스 콜백 함수
def draw_shape(event, x, y, flags, param):
    global points

    # 왼쪽 마우스 버튼 클릭하면 좌표를 저장하고, 네 번째 좌표 입력 후 선으로 그어 사각형 출력
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        if len(points) == 4:
            cv2.polylines(img, [np.array(points)], isClosed=True, color=(255, 0, 0), thickness=2)
            points = []

    # 오른쪽 마우스 입력하면 반지름 10을 가지는 원 출력
    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(img, (x, y), 10, (0, 255, 0), -1)

# 빈 이미지 생성
img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_shape)

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    # ESC 키를 누르면 종료
    if k == 27:
        break

# 이미지 리사이징 및 필터링
resized_img = cv2.resize(img, (256, 256), interpolation=cv2.INTER_AREA)
resized_img_linear = cv2.resize(img, (256, 256), interpolation=cv2.INTER_LINEAR)

# 결과 이미지 표시
cv2.imshow('Resized Image (INTER_AREA)', resized_img)
cv2.imshow('Resized Image (INTER_LINEAR)', resized_img_linear)
cv2.waitKey(0)
cv2.destroyAllWindows()
