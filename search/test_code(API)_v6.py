#!/usr/bin/env python
# coding: utf-8

# ### - 카카오 API : 키워드 검색

# - 카카오 API 테스트
#   - 앱 ID : 
#   - 네이티브 앱 키 : 
#   - REST API 키 : 
#   - JavaScript 키 : 
#   - Admin 키 : 
# - 키워드 검색
#   - 질의어를 통해 장소 검색 결과 반환
#   - category_group_name, category_name, place_url
# - 키워드 장소 검색 : 일간 100,000건

# In[ ]:


import json
import requests
# REST 키
rest_api_key = ''
# 헤더
headers = {"Authorization" : "KakaoAK {}".format(rest_api_key)}
# 파라미터
params = {"query" : "도련2동", "page" : 1}
url = "https://dapi.kakao.com/v2/local/search/keyword.json"

# GET을 이용하여 획득
res = requests.get(url, headers=headers, params=params)
# Json을 이용하여 해제
doc = json.loads(res.text)
# 200일 경우 정상
res.status_code

# In[ ]:


# 결과(Dict형으로 표현)
# documets : 각 검색 결과 정보
#  - address_name(String) : 전체 지번 주소
#  - category_group_code(String) : 중요 카테고리만 그룹핑한 카테고리 그룹 코드
#  - category_group_name(String) : 중요 카테고리만 그룹핑한 카테고리 그룹명
#  - category_name(String) : 카테고리 이름
#  - distance(String) : 중심좌표까지의 거리 (단, x,y 파라미터를 준 경우에만 존재), 단위 meter
#  - id(String) : 장소 ID
#  - phone(String) : 전화번호
#  - place_name(String) : 장소명, 업체명
#  - place_url(String) : 장소 상세페이지 URL
#  - road_address_name(String) : 전체 도로명 주소
#  - x(String) : X 좌표값, 경위도인 경우 longitude (경도)
#  - y(String) : Y 좌표값, 경위도인 경우 latitude(위도)
# meta : 검색 결과 메타 정보
doc

# ### - 카카오 API(키워드 검색) : 데이터 획득

# - 키워드 검색
#   - 질의어를 통해 장소 검색 결과 반환
#   - category_group_name, category_name, place_url
# - 키워드 장소 검색 : 일간 100,000건
# - 검색 키워드 선정
#   - 분위기 좋은, 감성적인, 오션뷰, 가족여행, 조용한, 맛집, 핫플레이스, 휴식/힐링, 화려한, 커플여행, 경치, 재미있는, 친구여행, 레포츠, 체험, 관람, 테마파크
# - 검색할 카테고리 선정
#   - CT1(문화시설), AT4(관광명소), FD6(음식점), CE7(카페), AD5(숙박)
# - 법정동·리 별로 검색 : <a href = 'https://ko.wikipedia.org/wiki/%EC%A0%9C%EC%A3%BC%EC%8B%9C%EC%9D%98_%ED%96%89%EC%A0%95_%EA%B5%AC%EC%97%AD' target='_blink'>위키백과</a>

# #### 1. 키워드, 카테고리 선정

# In[ ]:


keywords = ['분위기 좋은', '감성', '오션뷰', '가족여행', '조용한', '맛집', '핫플레이스', 
            '휴식', '화려한', '커플여행', '경치', '재미있는', '친구여행', '레포츠', 
            '체험', '관람', '테마파크']
categorys = ['CT1', 'AT4', 'FD6', 'CE7']
categorys_info = {'CT1' : '문화시설', 'AT4' : '관광명소', 'FD6' : '음식점', 'CE7' : '카페'}

# In[ ]:


import pandas as pd

jeju_range = pd.read_excel('./data/220113/제주도_법정동_리.xlsx')
jeju_range.head()

# #### 2. 데이터 획득

# - 카테고리, 키워드, 법정동_리를 이용해 기본 데이터 획득

# In[ ]:


import json
import requests
# REST 키
rest_api_key = ''
# 헤더
headers = {"Authorization" : "KakaoAK {}".format(rest_api_key)}
# 파라미터
params = {"query" : "도련2동", "page" : 1}
url = "https://dapi.kakao.com/v2/local/search/keyword.json"

# GET을 이용하여 획득
res = requests.get(url, headers=headers, params=params)
# Json을 이용하여 해제
doc = json.loads(res.text)
# 200일 경우 정상
res.status_code

# In[ ]:


# 결과(Dict형으로 표현)
doc

# #### 3. 셀레니움, 뷰티풀수프 데이터 추가

# - 평점, 이미지, 호텔등급 등 데이터 추가

# In[ ]:


import json
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('./driver/chromedriver.exe')
driver.get("https://place.map.kakao.com/7862728")

# - 평점 : #mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b
# - 호텔등급 : span.txt_location
# - 이미지는 태그가 다른 경우가 있어 2가지로 생각
#   - 더 많을 수도 있으므로 확인 필요
#   - 이미지1 : #mArticle > div.cont_photo.no_category > div.photo_area > ul > li.size_l > a
#   - 이미지2 : #mArticle > div.cont_photo > div.photo_area > ul > li.size_l > a

# In[ ]:


try:
    rate = driver.find_element_by_css_selector('''#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b''')
except:
    rate = False
try:
    hotel = driver.find_element_by_css_selector('''span.txt_location''')
except:
    hotel = False
try :
    image = driver.find_element_by_css_selector('''#mArticle > div.cont_photo.no_category > div.photo_area > ul > li.size_l > a''')
except:
    try:
        image = driver.find_element_by_css_selector('''#mArticle > div.cont_photo > div.photo_area > ul > li.size_l > a''')
    except:
        image = False

# In[ ]:


print(rate.text)
print(hotel.text)
if image:
    image = 'https:'+image.get_attribute('style')[23:-3]
print(image)

# In[ ]:


response = requests.get(image)
name = '_test'
# 이름 내에 슬래시('/')가 있으면 디렉터리로 인식하므로
# replace를 통해 변경해준다.
if '/' in name:
    name = name.replace('/', '-')
with open("{}.png".format(name), "wb") as f:
    f.write(response.content)

# In[ ]:


driver.quit()
