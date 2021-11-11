import requests
import json

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

import requests

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
