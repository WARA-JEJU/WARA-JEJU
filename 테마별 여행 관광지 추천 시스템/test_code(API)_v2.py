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

# In[ ]:


import json
import requests
# REST 키
rest_api_key = ''
# 헤더
headers = {"Authorization" : "KakaoAK {}".format(rest_api_key)}
# 파라미터
params = {"query" : "제주도 추자도"}
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

# ### - 네이버 API : 지역 검색

# - 네이버 API 테스트
#   - Client ID : 
#   - Client Secret : 
# - 지역 검색
#   - 질의어를 통해 장소 검색 결과 반환
#   - category, description 사용 가능

# In[ ]:


import json
import urllib
import requests
# REST 키
client_key = ''
client_secret = ''
# 헤더
headers = {"X-Naver-Client-Id" : client_key, 
           "X-Naver-Client-Secret" : client_secret}
# 파라미터
encText = urllib.parse.quote("제주도 신례토종닭식당")
url = "https://openapi.naver.com/v1/search/local.json?query="+encText

# GET을 이용하여 획득
res = requests.get(url, headers=headers)
# Json을 이용하여 해제
doc = json.loads(res.text)
# 200일 경우 정상
res.status_code

# In[ ]:


# 결과(Dict형으로 표현)
# items : 각 검색 결과 정보
#  - title(String) : 업체, 기관명
#  - link(String) : 기관의 상세 정보가 제공되는 네이버 페이지의 하이퍼텍스트 link
#  - category(String) : 중요 카테고리만 그룹핑한 카테고리 그룹명
#  - description(String) : 기관명에 대한 설명을 제공
#  - telephone(String) : 하위 호환성을 위해 존재
#  - address(String) : 기관명의 주소를 제공
#  - roadAddress(String) : 기관명의 도로명 주소를 제공
#  - mapx(String) : x좌표를 제공한다. 제공값은 카텍좌표계 값으로 제공
#  - mapy(String) : y좌표를 제공한다. 제공값은 카텍 좌표계 값으로 제공
doc

# ### - 관광 / 숙박 분리

# - 관광 / 숙박은 카테고리상 차이가 나기 때문에 분리해주도록 한다.

# #### 1. 데이터 확인

# - 필터링1 버전으로 실행
# - 필터링2는 레저/스포츠 부분만 전처리를 진행하였기 때문에 관광/숙박 시설은 필터링1과 동일

# In[ ]:


import pandas as pd

df = pd.read_excel('./data/제주도 장소(POI) - 필터링1.xlsx')
df.head()

# In[ ]:


df.info()

# - 구분 컬럼으로 카운트 확인

# In[ ]:


df['구분'].unique()

# In[ ]:


df['구분'].value_counts()

# #### 2. 관광 / 숙박 : 숙박 시설 확인

# - 관광/숙박 컬럼 선택

# In[ ]:


# all = df.query('구분 == "관광/숙박"')
all = df[df['구분'] == '관광/숙박']
all.head()

# In[ ]:


all.info()

# - 숙박 시설 확인
#   - '호텔', '민박', '모텔', '여관', '리조트', '펜션', '여인숙', '별장', '팬션', '콘도', '호스텔', '하우스'
#   - '--텔'로 끝나는 경우
#   - 2480개

# In[ ]:


accommodations = ['호텔', '민박', '모텔', '여관', '리조트', '펜션', '여인숙', '별장', '팬션', '콘도', '호스텔', '하우스']

accommodation_df = all.query(f'장소명.str.contains("{"|".join(accommodations)}") or 장소명.str.endswith("텔")', engine='python').copy()

# - 숙박 시설 DataFrame

# In[ ]:


accommodation_df.info()

# In[ ]:


len(accommodation_df['장소명'].unique())

# In[ ]:


# accommodation_df.to_excel('./accomodation.xlsx')

# #### 3. 관광 / 숙박 : 관광 시설 확인

# - 숙박 시설의 인덱스를 제거하여 관광 시설 판별

# In[ ]:


tourism_df = all.drop(accommodation_df.index, axis=0).copy()
tourism_df.info()

# In[ ]:


len(tourism_df['장소명'].unique())

# In[ ]:


# tourism_df.to_excel('tourism.xlsx')

# #### 4. 관광 / 숙박 : 관광 시설 추가 관찰

# - 엑셀을 이용해 직접 확인

# ### - 중복 좌표 처리

# #### 1. 데이터 확인

# - 필터링2 버전으로 실행
# - 같은 좌표가 2개 이상인 경우만 추가하여 확인

# In[1]:


import pandas as pd

df = pd.read_excel('./data/제주도 장소(POI) - 필터링2.xlsx')
df.head()

# In[2]:


df.info()

# In[3]:


df.columns

# In[4]:


include_index = []      # 탐색한 좌표
duplicate_index = []    # 중복 좌표

for idx, row in df.iterrows():
    # 중복 좌표가 아닌 경우 탐색
    if idx not in include_index:
        # 중복 좌표의 인덱스 확인
        temp = list(df[((df['위치좌표 X축값 '] == row['위치좌표 X축값 ']) & (df['위치좌표 Y축값 '] == row['위치좌표 Y축값 ']))].index)
        # 길이가 2 이상인 경우 : 중복 좌표가 존재함을 의미
        if len(temp) >=2 :
            include_index.extend(temp)
            duplicate_index.append(temp)
        # 길이가 1인 경우 : 중복 좌표가 존재하지 않음을 의미
        else:
            include_index.append(idx)

# - 전체 인덱스 개수

# In[5]:


len(include_index)

# - 중복 좌표 개수

# In[6]:


len(duplicate_index)

# #### 2. 중복 좌표 삭제

# In[7]:


total = 0
names = {}
for idx, index_list in enumerate(duplicate_index, start=1):
    total += len(index_list)    # 중복 좌표의 개수 확인
    names[index_list[0]] = []   # 중복 좌표의 다른 이름 추가
    for idx2, index in enumerate(index_list):
        if idx2 != 0:
            # 다른 이름 추가
            names[index_list[0]].append(df.loc[index, '장소명'])
            # 행 삭제
            df.drop(index, axis=0, inplace=True)

# - 전체 중복 좌표 수

# In[8]:


total

# - 삭제한 행의 수

# In[9]:


total - len(duplicate_index)

# - 중복 컬럼 삭제 후 정보

# In[10]:


df.info()

# In[11]:


df['구분'].value_counts()

# In[12]:


# 추가 이름 컬럼 생성
# 중복 좌표의 '이름' 추가, 없을 경우 '.'으로 표현
df['Additional_Name'] = '.'
for idx, value in names.items():
    df.loc[idx, 'Additional_Name'] = ','.join(value)

# In[13]:


df.head()

# - 중복 좌표 삭제

# In[ ]:


# df.to_excel('./data/제주도 장소(POI) - 필터링3.xlsx')
