import dlib
from skimage import io, transform
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import openface
import pickle 
import os
import sys
import argparse
import time

from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder

# dlib 얼굴인식 모델 불러오기 
face_detector = dlib.get_frontal_face_detector()
face_encoder = dlib.face_recognition_model_v1('./model/dlib_face_recognition_resnet_model_v1.dat')
face_pose_predictor = dlib.shape_predictor('./model/shape_predictor_68_face_landmarks.dat')

def get_detected_faces(filename):
    """
    HOG(방향성 그래디언트 히스토그램)를 이용하여 사진에서 얼굴을 인식 
    :입력(filename): 사진 파일의 이름 
    :출력: numpy 배열, face_detector 함수 동작
    """
    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image, face_detector(image, 1)

def get_face_encoding(image, detected_face):
    """
    신경망을 사용하여 얼굴을 암호화
    :입력 1(image): numpy 배열
    :입력 2(detected_face): 사진에서 포착된 얼굴 하나
    :출력: measurement, numpy 배열
    """
    pose_landmarks = face_pose_predictor(image, detected_face)
    face_encoding = face_encoder.compute_face_descriptor(image, pose_landmarks, 1)
    return np.array(face_encoding)

def training(people):
    """
    Linear SVC를 사용해 훈련하는 과정. Pickle을 사용해 만들어진 모델을 저장. 
    사진 하나 당 한 명(개)의 사람(얼굴)을 포착할 수 있도록 함. 
    :입력(people): 분류하고 탐지할 사람 개체
    """
    # 주어진 라벨 분석
    df = pd.DataFrame()
    for p in people:
        l = []
        for filename in glob.glob('./data/%s/*' % p):
            image, face_detect = get_detected_faces(filename)
            face_encoding = get_face_encoding(image, face_detect[0])
            l.append(np.append(face_encoding, [p]))
        temp = pd.DataFrame(np.array(l))
        df = pd.concat([df, temp])
    df.reset_index(drop=True, inplace=True)

    # 라벨을 int 값으로 변환하는 과정
    le = LabelEncoder()
    y = le.fit_transform(df[128])
    print("Training for {} classes.".format(len(le.classes_)))
    X = df.drop(128, axis=1)
    print("Training with {} pictures.".format(len(X)))

    # 모델 훈련
    clf = SVC(C=1, kernel='linear', probability=True)
    clf.fit(X, y)

    # 만들어진 모델 내보내기
    fName = "./classifier.pkl"
    print("Saving classifier to '{}'".format(fName))
    with open(fName, 'wb') as f:
        pickle.dump((le, clf), f)

def predict(filename, le=None, clf=None, verbose=False):
    """
    주어진 모델을 통해 사진에서 사람 얼굴을 탐지하는 기능
    :입력(filename): 얼굴을 탐지할 사진
    :입력(le):
    :입력(clf):
    :입력(verbose):
    :출력: 얼굴을 탐지하여 박스로 표기한 사진 
    """
    if not le and not clf:
        with open("./classifier.pkl", 'rb') as f:
            (le, clf) = pickle.load(f)
    image, detected_faces = get_detected_faces(filename)
    prediction = []

    # 디버깅용 장황성 설정
    if verbose:
        print('{} faces detected.'.format(len(detected_faces)))
    img = np.copy(image)
    font = cv2.FONT_HERSHEY_SIMPLEX

    for face_detect in detected_faces:
        # 얼굴 표시용 박스 설정 
        cv2.rectangle(img, (face_detect.left(), face_detect.top()), 
                          (face_detect.right(), face_detect.bottom()), (255, 0, 0), 2)
        start_time = time.time()

        # 얼굴별 탐지 
        p = clf.predict_proba(get_face_encoding(image, face_detect).reshape(1, 128))

        # "자신감"이 상대적으로 떨어지는 탐지 결과는 출력하지 않는다
        a = np.sort(p[0])[::-1]
        if a[0]-a[1] > 0.5:
            y_pred = le.inverse_transform(np.argmax(p))
            prediction.append([y_pred, (face_detect.left(), face_detect.top()), 
                          (face_detect.right(), face_detect.bottom())])
        else:
            y_pred = 'unknown'

        # 디버깅용 장황성 설정
        if verbose:
            print('\n'.join(['%s : %.3f' % (k[0], k[1]) for k in list(zip(map(le.inverse_transform, 
                                                                              np.argsort(p[0])), 
                                                                          np.sort(p[0])))[::-1]]))
            print('Prediction took {:.2f}s'.format(time.time()-start_time))
        
        cv2.putText(img, y_pred, (face_detect.left(), face_detect.top()-5), font, np.max(img.shape[:2])/1800, (255, 0, 0))
    return img, prediction

# 메인 함수
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser 호출 때 사용할 수 있는 인자값 추가
    parser.add_argument('mode', type=str, help='훈련인지 탐지인지 결정합니다.')
    parser.add_argument('--training_data',
                        type=str,
                        help="훈련 데이터 경로를 나타냅니다.",
                        default='./data/')
    parser.add_argument('--testing_data',
                        type=str,
                        help="테스트 데이터 경로를 나타냅니다.",
                        default='./test/')

    args = parser.parse_args()
    people = os.listdir(args.training_data)
    # 탐지될 사람의 수 출력
    print('{}명의 사람이 탐지됩니다.'.format(len(people)))

    # 함수 모드에 따라 동작을 다르게 수행
    if args.mode == 'train':
        training(people)
    elif args.mode == 'test':
        with open("./classifier.pkl", 'rb') as f:
            (le, clf) = pickle.load(f)
        for i, f in enumerate(glob.glob(args.testing_data)):
            img, _ = predict(f, le, clf)
            cv2.imwrite(args.testing_data + 'test_{}.jpg'.format(i), img)

