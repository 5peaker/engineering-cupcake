# OpenCV 최종과제

# 1. 배경 : 흰색 책상, 우드 테이블
# 2. 데이터 증식 조건 
#    2.1 rotate : 회전(10~30도)범위 안에서 어느 정도 각도를 넣어야 인식이 잘되는가?
#    2.2 hflip, vflip : 도움이 되는가? 넣을 것인가?
#    2.3 resize, crop : 가능하면 적용해 보자.
#    2.4 파일명을 다르게 저장 cf) jelly_wood.jpg, jelly_white.jpg
#        jelly_wood_rot_15.jpg, jelly_wood_hflip.jpg,jelly_wood_resize.jpg 
#    2.5 클래스 별로 폴더를 생성
#    2.6 데이터를 어떻게 넣느냐에 따라 어떻게 동작되는지 1~2줄로 요약

import numpy as np 
import pandas as pd

import os
import cv2

## 데이터 파일 불러오기 ---------------
# 폴더 경로 설정
folder_path = 'Chairs'
processing_path = "ResizedImg"

input_folder = "Chairs"
output_folder = "ProcessedImages"

# 폴더 내의 파일 목록 가져오기
file_list1 = os.listdir(folder_path)
file_list2 = os.listdir(processing_path)

# 출력 폴더가 없으면 생성하기
if not os.path.exists(processing_path):
    os.makedirs(processing_path)
    
if not os.path.exists(output_folder): 
    os.makedirs(output_folder)

# 이미지 로테이션 및 Hflip, Vflip 기능 추가
class Rotate_and_Flip:
    def __init__(self, image_path):
        self.img = image_path
        if self.img is None:
            raise ValueError(f"악! 이런 거 없어요!: {image_path}")
    
    # 이미지 회전 함수
    def rotate_image(self, angle=15):
        (h, w) = self.img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(self.img, M, (w, h))
        return rotated
    
    # 이미지 수평으로 뒤집기 
    def hflip_image(self):
        flipped = cv2.flip(self.img, 1)
        return flipped
    
    # 이미지 수직으로 뒤집기 
    def vflip_image(self):
        flipped = cv2.flip(self.img, 0)
        return flipped
    
    # 이미지를 수직, 수평 둘 다 뒤집기
    def twoflip_image(self):
        flipped = cv2.flip(self.img, -1)
        return flipped
    
    def save_new_image(self, image, output_file_path):
        cv2.imwrite(output_file_path, image)
        
class ImageProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def crop_into_quadrants(self, image):
        (h, w) = image.shape[:2]
        center_x, center_y = w // 2, h // 2

        # 네 등분으로 자르기
        top_left = image[0:center_y, 0:center_x]
        top_right = image[0:center_y, center_x:w]
        bottom_left = image[center_y:h, 0:center_x]
        bottom_right = image[center_y:h, center_x:w]

        return top_left, top_right, bottom_left, bottom_right
    
    def process_image(self):     
        for filename in os.listdir(self.input_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(self.input_folder, filename)
                image = cv2.imread(image_path)
                quadrants = self.crop_into_quadrants(image)
                
                # 각 사분면을 저장
                for i, quadrant in enumerate(quadrants):
                    output_path = os.path.join(self.output_folder, f"{filename}_quadrant_{i+1}.jpg")
                    cv2.imwrite(output_path, quadrant)
                
def save_image(image, output_folder, file_name, options):
    output_file_path = os.path.join(output_folder, f"{file_name}_{options}.jpg")
    cv2.imwrite(output_file_path, image)

# 파일 목록을 순회하며 이미지 읽기
for file_name in file_list1:
    # 파일 경로 생성
    file_path = os.path.join(folder_path, file_name)
    print(file_path)
    # 이미지 읽기
    image = cv2.imread(file_path)
    
    # 이미지가 제대로 읽혔는지 확인
    if image is not None:
        # 이미지를 224x224 크기로 리사이즈
        image = cv2.resize(image, (224, 224))
        output_file_path = os.path.join(processing_path, file_name)
        # 리사이즈된 이미지 저장
        cv2.imwrite(output_file_path, image)
        processor = ImageProcessor(input_folder, output_folder)
        processor.process_image()
    else:
        print(f"악! 못 불러왔어요!: {file_path}")
        
# 정의된 함수를 통해 이미지 전처리 작업 진행
for file_name in file_list2:
    # 파일 경로 생성
    file_path = os.path.join(processing_path, file_name)
    image = cv2.imread(file_path)
    
    if image is not None:
        # 이미지가 제대로 읽혔는지 확인
        output_file_path = os.path.join(output_folder, file_name)
        
        rf = Rotate_and_Flip(image)
        rotated_image = rf.rotate_image(30) # 30 회전
        hflip_image = rf.hflip_image() # 수평 뒤집기 
        vflip_image = rf.vflip_image() # 수직 뒤집기
        tf_image = rf.twoflip_image() # 수직, 수평 동시에 뒤집기
        
        base_file_name = os.path.splitext(file_name)[0]
        
        # 적용 옵션 별로 나누어 저장
        save_image(rotated_image, output_folder, base_file_name, 'rotated')
        save_image(hflip_image, output_folder, base_file_name, 'hflip')
        save_image(vflip_image, output_folder, base_file_name, 'vflip')
        save_image(tf_image, output_folder, base_file_name, 'twoflip')

    else:
        print(f"악! 파일을 못 찾겠어요! : {file_path}")