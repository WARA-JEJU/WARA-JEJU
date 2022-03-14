#!/usr/bin/env python
# coding: utf-8

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

# In[ ]:


jeju_range['법정동_리'][0].split(',')[:5]

# #### 2. 데이터 획득 테스트

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

# #### 3. 셀레니움, 뷰티풀수프 데이터 추가 테스트

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

# #### 4. 데이터 획득

# - 카카오 API(키워드 검색) JSON 형식
#   - 'documents' : ['address_name', 'category_group_code', 'category_group_name', 'category_name', 'distance', 'id', 'phone', 'place_name', 'place_url', 'road_address_name', 'x', 'y']
#   - 'meta' : ['is_end', 'pageable_count', 'same_name', 'total_count']

# ---
# **중복을 제거한 후 관광지 등의 데이터가 너무 부족하여 키워드를 재설정하여 크롤링 시행**  
# - 아래 코드는 결과가 부족하게 나왔지만 진행상황을 보기위해 남겨두었음.
# ---
# 

# ##### ◽카테고리, 키워드, 지역 변수

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

# ##### ◽카카오 API 활용 함수

# - (키워드, 카테고리, 법정동_리) 검색 함수

# In[ ]:


import json
import requests

def search_result(keyword, category, jeju_name):
    result = []

    # REST 키
    rest_api_key = '63d0926cf9b14de298157081ba8a8d02'
    # 헤더
    headers = {"Authorization" : "KakaoAK {}".format(rest_api_key)}
    # 파라미터
    params = {"query" : f"{jeju_name} {keyword}", "page" : 1, "category_group_code" : f"{category}"}
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    while True:
        # GET을 이용하여 획득
        res = requests.get(url, headers=headers, params=params)
        if res.status_code == 200:
            # Json을 이용하여 해제
            doc = json.loads(res.text)
            result.extend(doc['documents'])
            if doc['meta']['is_end'] == True:
                break
            else:
                params['page'] += 1
    return result

# - 전체 결과 데이터 프레임 반환 함수

# In[ ]:


import pandas as pd
from tqdm.notebook import tqdm

def search_df():
    results = []
    for idx, row in tqdm(jeju_range.iterrows()):
        for jeju in row['법정동_리'].split(','):
            for category in categorys:
                for key in keywords:
                    r = pd.DataFrame(search_result(key, category, jeju))
                    r['keyword'] = key
                    results.append(r.copy())
    return pd.concat(results).reset_index(drop=True)

# ##### ◽카카오 API 활용 데이터 획득

# In[ ]:


jeju_poi = search_df()

# In[ ]:


# jeju_poi.to_excel('./data/220114/제주도_POI(API).xlsx',index=False)

# In[ ]:


jeju_poi.head(2)

# ##### ◽데이터 확인(제주도_POI(API))

# - 기본 정보 확인
#   - NaN 데이터는 존재하지 않는다.

# - distance 컬럼은 값이 존재하지 않음

# In[ ]:


jeju_poi.info()

# - 검색한 키워드 중 존재하지않는 키워드 확인

# In[ ]:


for key in keywords:
    if key not in jeju_poi['keyword'].unique():
        print(key, end = ' | ')

# - keyword별 불균형이 존재

# In[ ]:


pd.DataFrame(jeju_poi['keyword'].value_counts())

# In[ ]:


jeju_poi['id'].unique().shape

# ##### ◽데이터 확인(제주도_POI(API)2)

# - 주소가 제주도가 아닌 경우를 삭제한 버전

# In[ ]:


import pandas as pd

api_poi = pd.read_excel('./data/220114/제주도_POI(API)2.xlsx', index_col=False)

# - distance 컬럼은 값이 존재하지 않음

# In[ ]:


api_poi.info()

# - keyword별 불균형이 존재

# In[ ]:


pd.DataFrame(api_poi['keyword'].value_counts())

# In[ ]:


pd.DataFrame(api_poi['category_group_name'].value_counts())

# In[ ]:


jeju_poi['id'].unique().shape

# ### - 카카오 API(키워드 검색) : 데이터 획득 (재시도)

# - 키워드 검색
#   - 질의어를 통해 장소 검색 결과 반환
#   - category_group_name, category_name, place_url
# - 키워드 장소 검색 : 일간 100,000건
# - 검색 키워드 선정 : **위 결과를 바탕으로 검색되지 않는 경우 삭제, 새로운 키워드 추가**
#   - '맛집', '분위기 좋은', '테마파크' ,'오션뷰', '감성', '가족여행', '체험', '휴식', '레포츠', '가볼만한 곳'
# - 검색할 카테고리 선정 : 숙박을 제외하고 검색 진행
#   - CT1(문화시설), AT4(관광명소), FD6(음식점), CE7(카페), AD5(숙박)
# - 법정동·리 별로 검색 : <a href = 'https://ko.wikipedia.org/wiki/%EC%A0%9C%EC%A3%BC%EC%8B%9C%EC%9D%98_%ED%96%89%EC%A0%95_%EA%B5%AC%EC%97%AD' target='_blink'>위키백과</a>

# #### 1. 데이터 획득

# ##### ◽카테고리, 키워드, 지역 변수

# In[ ]:


keywords = ['맛집', '분위기 좋은', '테마파크' ,'오션뷰', '감성', '가족여행', '체험', '휴식', '레포츠', '가볼만한 곳']
categorys = ['CT1', 'AT4', 'FD6', 'CE7']
categorys_info = {'CT1' : '문화시설', 'AT4' : '관광명소', 'FD6' : '음식점', 'CE7' : '카페'}

# In[ ]:


import pandas as pd

jeju_range = pd.read_excel('./data/220113/제주도_법정동_리.xlsx')
jeju_range.head()

# ##### ◽카카오 API 활용 함수

# - (키워드, 카테고리, 법정동_리) 검색 함수

# In[ ]:


import json
import requests

def search_result(keyword, category, jeju_name):
    result = []

    # REST 키
    rest_api_key = ''
    # 헤더
    headers = {"Authorization" : "KakaoAK {}".format(rest_api_key)}
    # 파라미터
    params = {"query" : f"제주특별자치도 {jeju_name} {keyword}", "page" : 1, "category_group_code" : f"{category}"}
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    while True:
        # GET을 이용하여 획득
        res = requests.get(url, headers=headers, params=params)
        if res.status_code == 200:
            # Json을 이용하여 해제
            doc = json.loads(res.text)
            result.extend(doc['documents'])
            if doc['meta']['is_end'] == True:
                break
            else:
                params['page'] += 1
    return result

# - 전체 결과 데이터 프레임 반환 함수

# In[ ]:


import pandas as pd
from tqdm.notebook import tqdm

def search_df():
    results = []
    for idx, row in tqdm(jeju_range.iterrows()):
        for jeju in row['법정동_리'].split(','):
            for category in categorys:
                for key in keywords:
                    r = pd.DataFrame(search_result(key, category, jeju))
                    r['keyword'] = key
                    results.append(r.copy())
    return pd.concat(results).reset_index(drop=True)

# ##### ◽카카오 API 활용 데이터 획득

# In[ ]:


jeju_poi = search_df()

# In[ ]:


# jeju_poi.to_excel('./data/220114/제주도_POI(API)3.xlsx',index=False)

# In[ ]:


jeju_poi.head(2)

# ##### ◽데이터 확인(제주도_POI(API)3)

# - 엑셀을 통해 중복(id) 제거

# In[ ]:


import pandas as pd

api_poi = pd.read_excel('./data/220114/제주도_POI(API)3.xlsx', index_col=False)

# In[ ]:


api_poi.info()

# In[ ]:


pd.DataFrame(api_poi['keyword'].value_counts())

# In[ ]:


pd.DataFrame(api_poi['category_group_name'].value_counts())

# #### 2. id 중복 처리 : 키워드 합치기

# ##### ◽id 중복 확인

# In[ ]:


import pandas as pd

api_poi = pd.read_excel('./data/220114/제주도_POI(API)3.xlsx', index_col=False)

# - id 값으로 조회하여 값이 2개이상인 경우
#   - 각 데이터의 키워드를 합치고 1개의 행만 남긴다.
#   - included : 중복된 id일 경우를 식별하기 위해 dict형으로 확인한 경우 추가
#   - del_index : 중복된 id의 인덱스 중 1개만 사용할 것이기에 삭제할 인덱스 추가

# In[ ]:


included = {}
del_index = []
for idx, row in api_poi.iterrows():
    id = row['id']
    temp = api_poi[api_poi['id'] == id].copy()
    cnt = len(temp)
    if id not in included and cnt > 1:
        included[id] = True
        for i, r in temp.iterrows():
            if idx == i:
                continue
            else:
                api_poi.loc[idx, 'keyword'] = api_poi.loc[idx, 'keyword'] + ',' + r['keyword']
                del_index.append(i)

# In[ ]:


# 중복 id의 수, 삭제할 인덱스의 수
len(included.keys()), len(del_index)

# In[ ]:


# 중복 id의 인덱스 삭제
api_poi_del = api_poi.drop(del_index, axis=0)

# In[ ]:


api_poi_del.info()

# In[ ]:


# api_poi_del.to_excel('./data/220114/제주도_POI(API)4.xlsx', index=False)

# ##### ◽id 중복 제거 데이터 확인(제주도_POI(API)4)

# In[ ]:


import pandas as pd

api_poi_del = pd.read_excel('./data/220114/제주도_POI(API)4.xlsx', index_col=False)

# In[ ]:


api_poi_del.info()

# - 행의 수와 id의 수가 일치하므로 중복된 id가 없음을 확인할 수 있다.

# In[ ]:


len(api_poi_del['id'].unique())

# In[ ]:


pd.DataFrame(api_poi_del['category_group_name'].value_counts())
