import cv2
import tensorflow.keras
import numpy as np
import requests
import json

## 이미지 전처리
def preprocessing(frame):
    # 사이즈 조정
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    
    # 이미지 정규화
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
    
    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    
    return frame_reshaped

## 메시지 전송
def send_message():
    # 커스텀 템플릿 주소 : https://kapi.kakao.com/v2/api/talk/memo/send
    talk_url = "https://kapi.kakao.com/v2/api/talk/memo/send"

    # 사용자 토큰
    token = 'b80c0df628911f66bfc491c31f514b51'
    header = {
        "Authorization": "Bearer t1jaaW6Z-7tsos7FA5JNkJgQ1ZZ6xaLiYItohQo9dZwAAAF9Da4MPg".format(
            token=token
        )
    }

    # 메시지 template id와 정의했던 ${name}을 JSON 형식으로 값으로 입력
    payload = {
        'template_id' : 65093,
        'template_args' : '{"name": "테스트 제목"}'
    }

    # 카카오톡 메시지 전송
    res = requests.post(talk_url, data=payload, headers=header)

    if res.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(res.json()))
    
    return


## main()
url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "authorization_code",
    "client_id" : "b80c0df628911f66bfc491c31f514b51",
    "redirect_uri" : "https://localhost:3000",
    "code"         : "iDyXop05L4RxWLjdFWUF1bxQ3WLRF-Y_Vkw_FjgA6aE1vH4PfDNAee664m4zb3QPqm6ZagopcSEAAAF9DcujfA"
    
}
response = requests.post(url, data=data)

tokens = response.json()

print(tokens)

## 학습된 모델 불러오기
model_filename = 'Desktop/keras_model.h5'
model = tensorflow.keras.models.load_model(model_filename)

# 카메라 캡쳐 객체, 0=내장 카메라
capture = cv2.VideoCapture(0)

# 캡쳐 프레임 사이즈 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

right_position = 1 # 바른 자세를 확인하기 위한 변수

while True:
    ret, frame = capture.read()
    if ret == True: 
        print("read success!")

    # 이미지 뒤집기
    frame_fliped = cv2.flip(frame, 1)
    
    # 이미지 출력
    cv2.imshow("VideoFrame", frame_fliped)
    
    # 1초마다 검사하며, videoframe 창으로 아무 키나 누르게 되면 종료
    if cv2.waitKey(200) > 0: 
        break
    
    # 데이터 전처리
    preprocessed = preprocessing(frame_fliped)

    # 예측
    prediction = model.predict(preprocessed)
    #print(prediction) # [[0.00533728 0.99466264]]
    
    if prediction[0,0] < prediction[0,1]:
        print("잘못된 자세")
        # 졸린 상태가 30초간 지속되면 소리 & 카카오톡 보내기
        if right_position == 1:
            right_position = 0
            send_message()
            
    else:
        print('올바른 자세')
        right_position = 1
    
# 카메라 객체 반환
capture.release() 
# 화면에 나타난 윈도우들을 종료
cv2.destroyAllWindows()
