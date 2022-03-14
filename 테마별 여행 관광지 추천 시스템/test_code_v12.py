#!/usr/bin/env python
# coding: utf-8

# ### - 서귀포 숙소 데이터

# - 숙소 데이터도 서귀포 쪽의 데이터가 없으므로 추가로 동일한 방법으로 추가한다.
# - 키워드 검색
#   - 질의어를 통해 장소 검색 결과 반환
#   - category_group_name, category_name, place_url
# - 키워드 장소 검색 : 일간 100,000건
# - 검색할 카테고리 선정 : 숙박
#   - AD5(숙박)
# - 법정동·리 별로 검색 : <a href = 'https://ko.wikipedia.org/wiki/%EC%84%9C%EA%B7%80%ED%8F%AC%EC%8B%9C%EC%9D%98_%ED%96%89%EC%A0%95_%EA%B5%AC%EC%97%AD' target='_blink'>위키백과</a>

# #### 1. 데이터 획득

# ##### ◽카테고리, 키워드, 지역 변수

# In[3]:


keywords = ['호텔', '리조트', '콘도', '게스트하우스', '민박', '펜션']
categorys = ['AD5']
categorys_info = {'AD5' : '숙박'}

# In[4]:


jeju_range = ['법환동', '서호동', '호근동', '강정동', '도순동', '영남동', '월평동', '동홍동', '서홍동', '보목동','서귀동','토평동', '상효동', '상예동', '색달동', '하예동', '대포동', '중문동', '하원동', '회수동', '신효동', '하효동']

# ##### ◽카카오 API 활용 함수 : 함수 재활용

# - search_result(keyword, category, jeju_name)
#   - (카테고리, 법정동_리) 검색 함수

# In[5]:


import json
import requests

def search_result(keyword, category, jeju_name):
    result = []

    # REST 키
    rest_api_key = '63d0926cf9b14de298157081ba8a8d02'
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

# - search_df()
#   - 전체 숙박 데이터 프레임 반환 함수

# In[6]:


import pandas as pd
from tqdm.notebook import tqdm

def search_df():
    results = []
    for idx, jeju in tqdm(enumerate(jeju_range)):
        for category in categorys:
            for key in keywords:
                r = pd.DataFrame(search_result(key, category, jeju))
                r['keyword'] = key
                results.append(r.copy())
    return pd.concat(results).reset_index(drop=True)

# ##### ◽카카오 API 활용 데이터 획득

# In[7]:


accommodation_poi_add = search_df()

# In[9]:


# accommodation_poi_add.to_excel('./data/220121/서귀포_숙박_POI.xlsx',index=False)

# In[10]:


accommodation_poi_add.head(2)

# ##### ◽데이터 확인(숙박_POI(API))

# - 엑셀을 통해 중복(keyword, id) 제거

# In[23]:


import pandas as pd

accommodation_poi_add = pd.read_excel('./data/220121/서귀포_숙박_POI.xlsx', index_col=False)

# In[24]:


accommodation_poi_add.info()

# In[25]:


pd.DataFrame(accommodation_poi_add['keyword'].value_counts())

# #### 2. id 중복 처리 : 키워드 정리

# ##### ◽id 중복 확인

# In[27]:


import pandas as pd

accommodation_poi_add = pd.read_excel('./data/220121/서귀포_숙박_POI.xlsx', index_col=False)

# - id 값으로 조회
#   - keyword와 category를 비교하여 맞지않는 경우 삭제

# In[28]:


del_index = []
for idx, row in accommodation_poi_add.iterrows():
    key = row['keyword']
    if '리조트' in key:
        key = '리조트'
    if key not in row['category_name']:
            del_index.append(idx)

# In[29]:


# 삭제할 인덱스의 수
len(del_index)

# In[30]:


# 중복 id의 인덱스 삭제
accommodation_poi_del = accommodation_poi_add.drop(del_index, axis=0)

# In[31]:


accommodation_poi_del.info()

# In[32]:


len(accommodation_poi_del['id'].unique())

# In[33]:


# accommodation_poi_del.to_excel('./data/220121/서귀포_숙박_POI_최종RAW.xlsx', index=False)

# #### 3. 셀레니움 : 이미지, 평점, 호텔 등급 데이터 확보

# ##### ◽데이터 확인

# In[34]:


import pandas as pd

accommodation = pd.read_excel('./data/220121/서귀포_숙박_POI_최종RAW.xlsx', index_col=False)

# In[35]:


accommodation.columns

# In[36]:


accommodation.shape

# In[37]:


accommodation.head(2)

# ##### ◽셀레니움 함수

# - 평점 : #mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b
# - 호텔등급 : span.txt_location
# - 이미지 : #mArticle > div.cont_photo.no_category > div.photo_area > ul > li.size_l > a

# In[38]:


import json
import requests
import time
from tqdm.notebook import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

def selenium_result(url):    
    rate = 0
    grade = False
    image = False
    ua = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'user-agent={ua.ie}')
    # options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome('./driver/chromedriver.exe', options=options)
    time.sleep(0.5)
    driver.implicitly_wait(8)
    driver.get(url)
    try:
        rate = driver.find_element_by_css_selector('''#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b''').text
    except:
        pass
    try:
        grade = driver.find_element_by_css_selector('''span.txt_location''').text
    except:
        pass
    try :
        image = driver.find_element_by_css_selector('''#mArticle > div.cont_photo.no_category > div.photo_area > ul > li.size_l > a''')
    except:
        pass
    else:
        image = 'https:'+image.get_attribute('style')[23:-3]
    driver.quit()

    return rate, grade, image

# - 각 행의 place_url을 통해 해당 정보 추출

# In[ ]:


accommodation['rating'] = 0
accommodation['grade'] = accommodation['keyword']
accommodation['image'] = 'Not Image'

# In[45]:


from tqdm.notebook import tqdm

for idx in tqdm(range(757, len(accommodation))):
    url = accommodation.loc[idx, 'place_url']
    rate, grade, image = selenium_result(url)
    accommodation.loc[idx, 'rating'] = rate
    if grade != False:
        accommodation.loc[idx, 'grade'] = grade
    if image != False:
        accommodation.loc[idx, 'image'] = image

# - 오류가 발생하므로 각각의 데이터를 저장 후 합쳐주었다.

# In[46]:


# accommodation.to_excel('./data/220121/서귀포_숙박_selenium.xlsx', index=False)

# ##### ◽셀레니움 데이터 확인

# - 최종 합본 데이터 확인

# In[53]:


import pandas as pd

accommodation_all = pd.read_excel('./data/220121/_서귀포_숙박_selenium_final.xlsx', index_col=False)

# In[54]:


accommodation_all.info()

# In[55]:


accommodation_all[['id', 'rating', 'grade', 'image']].head(3)

# - 1000개 정도의 숙박 시설은 이미지가 없는 것 확인

# In[56]:


(accommodation_all['image'] != 'Not Image').value_counts()

# In[57]:


accommodation_all['keyword'].value_counts()

# In[58]:


accommodation_all['grade'].value_counts()

# ##### ◽이미지 데이터 다운로드

# - 이미지 다운로드 함수 작성
#   - image_download(place_name, place_id, place_image_url):

# In[59]:


import requests

def image_download(place_name, place_id, place_image_url):    
    response = requests.get(place_image_url)
    name = f'{place_name}_{place_id}'
    # 이름 내에 슬래시('/')가 있으면 디렉터리로 인식하므로
    # replace를 통해 변경해준다.
    if '/' in name:
        name = name.replace('/', '-')
    with open("./data/220121/서귀포_숙박_이미지/{}.png".format(name), "wb") as f:
        f.write(response.content)

# - 데이터 불러오기

# In[60]:


import pandas as pd

accommodation_all = pd.read_excel('./data/220121/_서귀포_숙박_selenium_final.xlsx', index_col=False)

# In[61]:


accommodation_all.head(2)

# - 이미지 저장

# In[62]:


import pandas as pd
import time
from tqdm.notebook import tqdm

not_image = pd.DataFrame({'place_name' : [], 'id' : [], 'idx' : []})
cnt = 0
for idx in tqdm(range(len(accommodation_all))):
    p_name, p_id, p_image = accommodation_all.loc[idx, ['place_name', 'id', 'image']]
    if p_image != 'Not Image':
        image_download(p_name, p_id, p_image)
        time.sleep(0.5)
    else:
        not_image.loc[cnt] = {'place_name' : p_image, 'id' : str(p_id), 'idx' : idx}
        cnt += 1

not_image.loc[:, 'idx'] = not_image.loc[:, 'idx'].astype('int')

# In[63]:


not_image.info()

# In[64]:


# not_image.to_excel('./data/220121/서귀포_숙박_not_image.xlsx', index=False)

# #### 4. 이미지 삭제 : 로고, 음식 사진인 경우 삭제

# - 각 이미지를 확인하여 잘못된 경우 삭제한다.

# ##### ◽이미지 ID 확인

# - 데이터 확인

# In[97]:


import pandas as pd

seogipo_accom = pd.read_excel('./data/220121/_서귀포_숙박_selenium_del.xlsx', index_col=False)
jeju_accom = pd.read_excel('./data/220117/_숙박_selenium_del.xlsx', index_col=False)

# In[98]:


seogipo_accom.head(1)

# In[100]:


jeju_accom.head(1)

# In[101]:


del_index = []
del_names = []
for idx, row in seogipo_accom.iterrows():
    s_id = row['id']
    s_name = row['place_name']
    if int(s_id) in list(map(int, jeju_accom['id'])):
        del_index.append(idx)
        del_names.append((s_id, s_name))

# In[102]:


del_index[:5], len(del_index), del_names[:2]

# ##### ◽중복 행 삭제

# - jeju_accom에 존재하는 데이터는 삭제한다.

# In[105]:


seogipo_accom_del = seogipo_accom.drop(del_index, axis=0)

# In[106]:


seogipo_accom_del.head(1)

# In[107]:


# seogipo_accom_del.to_excel('./data/220121/_서귀포_숙박_final.xlsx', index=False)

# ##### ◽이미지 삭제

# - 삭제할 이미지 id 확인

# In[ ]:


import os

del_id = []
for file in os.listdir('./data/220121/서귀포_숙박_삭제'):
    p_id = file.split('_')[1][:-4]
    del_id.append(p_id)

# In[ ]:


del_id[:5]

# - 해당 데이터 삭제

# In[ ]:


import pandas as pd

accommodation_all = pd.read_excel('./data/220121/_서귀포_숙박_final.xlsx', index_col=False)

# In[ ]:


accommodation_all.head(1)

# In[ ]:


del_idx = []

for idx, row in accommodation_all.iterrows():
    if str(row['id']) in del_id:
        del_idx.append(idx)

# In[ ]:


len(del_idx), del_idx[:4]

# In[ ]:


accom_del = accommodation_all.drop(del_idx, axis=0)

# In[ ]:


# accom_del.to_excel('./data/220121/_서귀포_숙박_최종.xlsx', index=False)

# ##### ◽이미지 데이터 재다운로드

# - 이미지 다운로드 함수 작성
#   - image_download(place_name, place_id, place_image_url):

# In[ ]:


import requests

def image_download(place_name, place_id, place_image_url):    
    response = requests.get(place_image_url)
    name = f'{place_name}_{place_id}'
    # 이름 내에 슬래시('/')가 있으면 디렉터리로 인식하므로
    # replace를 통해 변경해준다.
    if '/' in name:
        name = name.replace('/', '-')
    with open("./data/220121/서귀포_숙박_이미지/{}.png".format(name), "wb") as f:
        f.write(response.content)

# - 데이터 불러오기

# In[ ]:


import pandas as pd

accommodation_all = pd.read_excel('./data/220121/_서귀포_숙박_최종.xlsx', index_col=False)

# In[ ]:


accommodation_all.head(2)

# - 이미지 저장

# In[ ]:


import pandas as pd
import time
from tqdm.notebook import tqdm

for idx in tqdm(range(len(accommodation_all))):
    p_name, p_id, p_image = accommodation_all.loc[idx, ['place_name', 'id', 'image']]
    
    image_download(p_name, p_id, p_image)
    time.sleep(0.5)
