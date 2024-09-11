import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# 데이터셋 불러오기
dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

## -----데이터셋 청소 단계 
# 첫 번째 기록에 한정해서 단어 청소 실행
import re  
review = re.sub('[^a-zA-Z]',' ',dataset['Review'][0]) # 알파벳 (A부터 Z까지) 제외한 단어를 모두 소거 
review = review.lower()  # 남은 모든 단어를 소문자로 일괄 변환

# 리뷰에서 중요하지 않은 단어를 제거
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
review = review.split()  # 분석할 문장을 쪼개 단어들의 리스트로 변환
review = [word for word in review if not word in set(stopwords.words('english'))]

# 과거형이나 미래형 등 시제나 용법이 다른 단어들을 원형으로 변환
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
ml = []
for word in review:
    st = ps.stem(word)
    ml.append(st)
review = ml

# '다듬어잔' 단어들을 결합하여 String으로 합친다 
review = ' '.join(review) 
corpus = []
corpus.append(review)
# 디버깅 시 "print(len(corpus))" 구문을 사용 가능 

# 이상의 과정을 보유 중인 리뷰 세트 전체에 적용할 필요가 있다
for i in range(1,1000):
    review1 = re.sub('[^a-zA-Z]',' ',dataset['Review'][i])
    review1 = review1.lower()
    review1 = review1.split()
    review1 = [word for word in review1 if not word in set(stopwords.words('english'))]
    ml1 = []
    for word in review1:
        st1 = ps.stem(word)
        ml1.append(st1)
        review1 = ml1
    review1 = ' '.join(review1)
    corpus.append(review1)

## -----------------------------------
#  "단어 가방" 모델 생성 
# 토큰화 과정을 통해 희소 행렬을 생성하
# 각 단어별 등장 빈도를 체크, 계산한다

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500)
X10 = cv.fit_transform(corpus)
X1 = X10.toarray()
y = dataset.iloc[:, 1].values

##-----------------------------------
# 데이터 세트를 훈련용과 시험용으로 분리
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X1, y, test_size = 0.20, random_state = 0)

# 훈련용 세트는 나이브-베이즈 분류 적용 
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)
plt.hist(X_train)
plt.hist(y_train, label='positive (1) and negative (0)')
plt.legend()
plt.show()

# 시험용 세트를 예상
y_pred = classifier.predict(X_test)

# 혼동 행렬 생성 
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)

# 정확도 계산
print('혼동 행렬 출력: \n', cm)
acc_cm =(cm[0,0]+cm[1,1])/(cm[0,0]+cm[0,1]+cm[1,0]+cm[1,1])
print('혼동 행렬 기반 정확도: ', acc_cm)
acc_score1 = accuracy_score(y_test, y_pred)
print('모델 정확도: ', acc_score1)

#- ------------------------------------------------------------
# 만들어진 모델에 입각하여 유저로부터 새로 입력을 받는다 (과정은 동일함)

userinput = input("Enter your input :     ")
# userinput = st.text_area("Enter your input :     ")

review2 = re.sub('[^a-zA-Z]',' ',userinput) # 알파벳 이외의 글자를 소거
review2 = review2.lower()

review2 = review2.split()
review2 = [word for word in review2 if not word in set(stopwords.words('english'))]

ml13 = []
for word in review2:
    st13 = ps.stem(word)
    ml13.append(st13)
    review2 = ml13
review2 = ' '.join(review2)

import copy
corpus_copy = copy.deepcopy(corpus)
corpus_copy.append(review2)

# 유저 입력을 분석한 기록을 기존의 기록 아래에 덧붙인다

cv = CountVectorizer(max_features = 1500)
X111 = cv.fit_transform(corpus_copy).toarray()

y_pred1 = classifier.predict(X111[-1:][:])
print(y_pred1)

if y_pred1 == 1:
    print("긍정적인 피드백입니다.")
else:
    print("부정적인 피드백입니다.")

corpus_copy = []
