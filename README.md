# "Smart Summary"


산학캡스톤디자인1(04분반,5팀) : **비비빅**(Be-Vision-Big)



-------


## 주제 소개
최근 많은 사람들이 온라인에서 물건을 구입하지만 아마존과 같은 해외 웹사이트의 리뷰는 대부분 외국인들로부터 온 것이다. <br>그렇기에 해외 제품을 구매하는 입장에서는 상품의 다양한 정보를 얻기 힘들다.<br>그래서 우리는 영문 리뷰 요약을 통해 핵심 정보만 도출, 사람들이 보다 쉽게 해외 웹사이트에서 쇼핑을 즐길 수 있게 할 것이다.
 

## 선정 배경

나날이 직구를 찾는 사람들이 늘어나고 그들 중 다수의 사람들이 미국(아마존, 아이허브, 이베이)등을 이용해오고 있음을 확인할 수 있다.<br>그래서 우리는 소비자가 해외 웹사이트에서 직접 구매할 때 맞닥뜨리는 언어장벽의 어려움을 낮춰주고자 영문리뷰요약 모델을 개발하기로 결정했다.

![G3](https://user-images.githubusercontent.com/30707885/121585106-2a9b5100-ca6d-11eb-863e-0234b7122aa7.jpg) ![G2](https://user-images.githubusercontent.com/30707885/121585140-3424b900-ca6d-11eb-96dc-72ebebd738a4.jpg) ![G1](https://user-images.githubusercontent.com/30707885/121585158-39820380-ca6d-11eb-9438-63355aa51092.jpg)


## 기대효과

해외 구매 사이트의 리뷰를 영어로 요약하면 제품에 대한 다양한 정보를 얻기 수월해지고 구매에 있어서 더 좋은 판단이 가능해질 것이다.<br>그래서 소비자들의 구매 실패와 해외 제품 구매에 대한 불안감도 줄일 수 있다고 기대된다.


-------



## 팀원 소개


|마서연<br>(팀장)|안재명|윤영준|엽옥영|
|------|------|------|------|
|웹 페이지 제작<br>전처리<br>개발 보조<br>README|메인 개발<br>모델 제작<br>발표|문서 작성 및 정리<br>발표 자료 제작<br>전처리<br>개발 보조|개발 보조|

-------

## 개발 일정(요약)


| 기간 | 작업 | 설명 |
|-------|------|---------|
| 1주 | 아이디어 회의 | 시각 장애인을 위한 서비스를 개발하기로 결정 |
| 2주 | 아이디어 변경 | 점자번역 > 손톱을 통한 건강체크 > 텍스트 요약 |
| 3주 | 데이터 수집, 기존 서비스 분석 | Amazon review data, BBC data 등을 수집 |
| 4~8주 | 기술 공부, 구현 | 데이터 전처리, 모델링 등 전반적인 요약 기능 구현 |
| 9~10주 | 테스트 | 사용자로부터 직접입력 받아 요약문 생성 |
| 10주 | 유지보수, 웹 페이지 개발 | Django 사용했다가 Flask로 뼈대,스타일 구성 |
| 11주 | 유지보수, 연동시키기 | Flask로 모델 배포, 요약문 생성 |





-------

## 개발 환경

### AI
- Google Colaboratory
- Jupiter Notebook


### Web
- VS Code
- Flask

-------

## 주요 기능


- **요약 기능**


요약할 리뷰를 복사해와서 왼쪽 노트에 붙여넣고 "Click!"(요약 버튼)을 누르면 오른쪽 노트에 요약 결과를 보여준다.
"restart" 버튼을 눌러 첫 페이지로 돌아갈 수 있다.


- **번역 기능**


"Papago" 버튼을 누르면 url 쿼리에 요약결과가 함께 전달되어 요약문에 대한 번역을 바로 확인할 수 있다.


![Screenshot 2021-06-10 at 23 38 21](https://user-images.githubusercontent.com/30707885/121567920-1437ca00-ca5a-11eb-8356-ba035c54a41b.jpg)


![Screenshot 2021-06-10 at 23 50 32](https://user-images.githubusercontent.com/30707885/121567940-18fc7e00-ca5a-11eb-8840-0d08e0331746.jpg)



-------

## 사용한 기반 기술

- **자연어 처리(문서 요약)**


전체 문서에 포함된 글자와 문장들을 분석해서 요약문과 같이 글의 특징을 뽑아낸다.


|추출요약|추상요약|
|------|------|
|입력으로 들어온 텍스트에서 요약문에 해당하는 문장, 단어를 추출하는 방식|글의 내용을 파악해서 요약문에 해당하는 문장을 직접 생성하는 방식|



- **Modeling(Seq2seq + Attention)**

![md](https://user-images.githubusercontent.com/30707885/121567904-0eda7f80-ca5a-11eb-8bbe-ec1bc2734984.PNG)


**인코더** : 입력 문장의 단어 토큰화를 통해 쪼갠 후 각각 RNN 셀에 입력


**Embedding** : 텍스트를 벡터로 바꿈


**Context**  : 인코더 RNN 셀의 마지막 시점의 은닉 상태를 디코더 RNN 셀로 넘겨줌


각각의 셀이 다음 올 단어를 예측해서 입력을 받음. 


**Softmax 함수** : 출력 시퀀스의 각 단어별 확률값을 반환하고 이를 통해 다음에 올 수 있는 수많은 단어 중에 하나를 결정한다.


값이 Softmax 를 거치면 Attention weight ( 각 입력 단어들과 디코더가 예측할 단어의 유사도 ) 

-------


## 전체적인 흐름



![p](https://user-images.githubusercontent.com/30707885/121567864-02eebd80-ca5a-11eb-86e0-8a76a953610b.PNG)

-------

## 구현


### 1. preprocessing


**전체 데이터의 개수 : 568454**


> 데이터 중복 제거<br>
  결측치 제거<br>
  단어 정규화 및 불용어 제거<br>
  텍스트 소문자화<br>
  Html 태그 제거<br>
  괄호로 닫힌 문자열 제거<br>
  쌍따옴표 제거<br>
  약어 정규화<br>
  소유격 제거 (‘s)<br>
  영어 외 문자 공백으로 변환<br>


**전처리를 거친 후 데이터의 개수 : 393224**

![pre](https://user-images.githubusercontent.com/30707885/121585061-1eaf8f00-ca6d-11eb-9978-c97c8265c202.jpg)


### 2. EDA

**- 요약된 문장의 분포도 / 리뷰 텍스트의 분포도**


![그림1](https://user-images.githubusercontent.com/30707885/121568047-34678900-ca5a-11eb-87ae-44ecb36acd51.png)  ![그림2](https://user-images.githubusercontent.com/30707885/121568026-30d40200-ca5a-11eb-92be-d367dadd2345.png)

![그림3](https://user-images.githubusercontent.com/30707885/121568010-2c0f4e00-ca5a-11eb-8476-f90d059cafb6.png)


|-|최대 길이|평균 길이|
|---|------|------|
|원문|1919| 38|
|요약문|28|3|


>원문 텍스트에서 길이가 60 이하인 샘플의 비율 : 84%<br>
 요약된 문장에서 길이가 6 이하인 샘플의 비율 : 86%<br>
 >각각 정해준 길이보다 큰 샘플을 제거



### 3. Split Data & Additional Processing

![그림4](https://user-images.githubusercontent.com/30707885/121568078-3df0f100-ca5a-11eb-91d0-3c7a4668d4c8.jpg) ![pr](https://user-images.githubusercontent.com/30707885/121585086-240cd980-ca6d-11eb-95bf-1b5f0ddf7b39.jpg)


**8 : 2 비율로 훈련 데이터와 테스트 데이터 분리** 


>전체 등장 빈도에서 희귀 단어 등장 빈도 비율 : 1.56%
 > 해당 단어들은 정수 인코딩 과정에서 배제<br>
   몇 단어들이 제거되면서 해당 단어로 구성된 샘플이 빈 샘플이 됨<br>
   빈 샘플들도 제거


### 4. Modeling

![model](https://user-images.githubusercontent.com/30707885/121569569-e489c180-ca5b-11eb-935a-110e4f52cd91.PNG)

**Batch_size = 256, Epochs = 30**

---------


### 5. Train&Vaild

- 최종결과

|loss|acc|val_loss|val_acc|Embedding_dim|
|------|------|------|------|-----------|
|2.2606|62%|2.5024|60%|50|



### 6. Test



#### - 사용자로부터 입력을 받아 테스트해 본 결과

|-|테스트 문장|결과|
|------|-----------|------|
|원문|I have a brushed dewalt torque wrench and i didn't have a driver so i bought this. This is an amazing driver but what you don't know that this unscrewed my car lug nuts without issues! Further more it's brush less so there were no sparks going off while doing it!|love this stuff|
|번역|필요로 했던 물건이 없어서 대신 이 물건을 샀는데 이게 문제없이 내가 하고자 하는 일을 해냈다는 건 여러분이 모를 거예요! 게다가 브러쉬가 적어서 일을 하는 동안 불꽃이 튀지도 않았다구요!|이 물건이 좋아요|

---------

### 7. Web

- html, css를 사용해 기본 틀을 마련(base, result.html)
- Flask로 요약 Model을 웹에 배포(app.py), 이를 통해 사용자의 입력에 따른 요약문을 생성할 예정

![w그림1](https://user-images.githubusercontent.com/30707885/121587922-46ecbd00-ca70-11eb-93d3-090ef7563b90.png)


---------

## Good Case / Bad Case

![case](https://user-images.githubusercontent.com/30707885/121567884-0a15cb80-ca5a-11eb-8ff5-213ab95ec665.PNG)



