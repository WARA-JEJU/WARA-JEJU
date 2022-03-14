#!/usr/bin/env python
# coding: utf-8

# ### - 카카오 API(키워드 검색) : 숙박 시설 데이터

# - 키워드 검색
#   - 질의어를 통해 장소 검색 결과 반환
#   - category_group_name, category_name, place_url
# - 키워드 장소 검색 : 일간 100,000건
# - 검색할 카테고리 선정 : 숙박
#   - AD5(숙박)
# - 법정동·리 별로 검색 : <a href = 'https://ko.wikipedia.org/wiki/%EC%A0%9C%EC%A3%BC%EC%8B%9C%EC%9D%98_%ED%96%89%EC%A0%95_%EA%B5%AC%EC%97%AD' target='_blink'>위키백과</a>

# #### 1. 데이터 획득

# ##### ◽카테고리, 키워드, 지역 변수

# In[ ]:


keywords = ['호텔', '리조트', '콘도', '게스트하우스', '민박', '펜션']
categorys = ['AD5']
categorys_info = {'AD5' : '숙박'}

# In[ ]:


import pandas as pd

jeju_range = pd.read_excel('./data/220113/제주도_법정동_리.xlsx')
jeju_range.head()

# ##### ◽카카오 API 활용 함수 : 함수 재활용

# - search_result(keyword, category, jeju_name)
#   - (카테고리, 법정동_리) 검색 함수

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


accommodation_poi = search_df()

# In[ ]:


# accommodation_poi.to_excel('./data/220114/숙박_POI(API).xlsx',index=False)

# In[ ]:


accommodation_poi.head(2)

# ##### ◽데이터 확인(숙박_POI(API))

# - 엑셀을 통해 중복(keyword, id) 제거

# In[ ]:


import pandas as pd

accommodation_poi = pd.read_excel('./data/220114/숙박_POI(API).xlsx', index_col=False)

# In[ ]:


accommodation_poi.info()

# In[ ]:


pd.DataFrame(accommodation_poi['keyword'].value_counts())

# #### 2. id 중복 처리 : 키워드 합치기

# ##### ◽id 중복 확인

# In[ ]:


import pandas as pd

accommodation_poi = pd.read_excel('./data/220114/숙박_POI(API).xlsx', index_col=False)

# - id 값으로 조회
#   - keyword와 category를 비교하여 맞지않는 경우 삭제

# In[ ]:


del_index = []
for idx, row in accommodation_poi.iterrows():
    if row['keyword'] not in row['category_name']:
            del_index.append(idx)

# In[ ]:


# 삭제할 인덱스의 수
len(del_index)

# In[ ]:


# 중복 id의 인덱스 삭제
accommodation_poi_del = accommodation_poi.drop(del_index, axis=0)

# In[ ]:


accommodation_poi_del.info()

# In[ ]:


# accommodation_poi_del.to_excel('./data/220114/숙박_POI(API)2.xlsx', index=False)

# ##### ◽id 중복 제거 데이터 확인

# In[ ]:


import pandas as pd

accommodation_poi_del = pd.read_excel('./data/220114/숙박_POI(API)2.xlsx', index_col=False)

# In[ ]:


accommodation_poi_del.info()

# - 행의 수와 id의 수가 일치하므로 중복된 id가 없음을 확인할 수 있다.

# In[ ]:


len(accommodation_poi_del['id'].unique())

# - '리조트', '콘도'는 리조트/콘도로 변경

# In[ ]:


index = list(accommodation_poi_del[accommodation_poi_del['keyword'] == '리조트'].index)
accommodation_poi_del.loc[index, 'keyword'] = '리조트/콘도'

# In[ ]:


pd.DataFrame(accommodation_poi_del['keyword'].value_counts())

# In[ ]:


# accommodation_poi_del.to_excel('./data/220114/숙박_POI(API)3.xlsx', index=False)

# #### 3. 셀레니움 : 이미지, 평점, 호텔 등급 데이터 확보

# ##### ◽데이터 확인

# In[ ]:


import pandas as pd

accommodation = pd.read_excel('./data/220114/_숙박_POI(API)_keyword정리.xlsx', index_col=False)

# In[ ]:


accommodation.columns

# In[ ]:


accommodation.shape

# In[ ]:


accommodation.head(2)

# ##### ◽셀레니움 함수

# - 평점 : #mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b
# - 호텔등급 : span.txt_location
# - 이미지 : #mArticle > div.cont_photo.no_category > div.photo_area > ul > li.size_l > a

# In[ ]:


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


from tqdm.notebook import tqdm

accommodation['rating'] = 0
accommodation['grade'] = accommodation['keyword']
accommodation['image'] = 'Not Image'

for idx in tqdm(range(len(accommodation))):
    url = accommodation.loc[idx, 'place_url']
    rate, grade, image = selenium_result(url)
    accommodation.loc[idx, 'rating'] = rate
    if grade != False:
        accommodation.loc[idx, 'grade'] = grade
    if image != False:
        accommodation.loc[idx, 'image'] = image

# - 오류가 발생하므로 각각의 데이터를 저장 후 합쳐주었다.

# In[ ]:


accommodation.to_excel('./data/220115/숙박_selenium.xlsx', index=False)

# ##### ◽셀레니움 데이터 확인

# - 최종 합본 데이터 확인

# In[ ]:


import pandas as pd

accommodation_all = pd.read_excel('./data/220115/숙박_selenium_합본.xlsx', index_col=False)

# In[ ]:


accommodation_all.info()

# In[ ]:


accommodation_all[['id', 'rating', 'grade', 'image']].head(3)

# - 1000개 정도의 숙박 시설은 이미지가 없는 것 확인

# In[ ]:


(accommodation_all['image'] != 'Not Image').value_counts()

# In[ ]:


accommodation_all['keyword'].value_counts()

# In[ ]:


accommodation_all['grade'].value_counts()

# ##### ◽이미지 데이터 다운로드

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
    with open("./data/220116/숙박 시설 이미지/{}.png".format(name), "wb") as f:
        f.write(response.content)

# - 데이터 불러오기

# In[ ]:


import pandas as pd

accommodation_all = pd.read_excel('./data/220115/숙박_selenium_합본.xlsx', index_col=False)

# In[ ]:


accommodation_all.head(2)

# - 이미지 저장

# In[ ]:


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

# In[ ]:


not_image.info()

# In[ ]:


# not_image.to_excel('./data/220116/not_image.xlsx', index=False)

# #### 4. 셀레니움 : 이미지없는 경우 재확인

# - 이미지의 경우 태그가 2개로 나뉘어진 것을 확인
#   - 이미지1 : #mArticle > div.cont_photo.no_category > div.photo_area > ul > li.size_l > a
#   - 이미지2 : #mArticle > div.cont_photo > div.photo_area > ul > li.size_l > a

# ##### ◽데이터 읽기

# In[ ]:


import pandas as pd

# In[ ]:


accom_all = pd.read_excel('./data/220115/숙박_selenium_합본.xlsx', index_col=False)
not_image = pd.read_excel('./data/220116/not_image.xlsx', index_col=False)

# - 숙박 셀레니움 합본 데이터

# In[ ]:


accom_all.head(1)

# - 숙박 데이터 중 image가 없는 경우의 데이터

# In[ ]:


not_image.head(1)

# - not_image의 ['idx'] 컬럼 검증
#    - 각 컬럼의 연결이 잘 되어있음을 확인할 수 있다!!

# In[ ]:


for idx, row in not_image.iterrows():
    if accom_all[accom_all['id'] == row['id']].index != row['idx']:
        print('Fail!!!!!')

# ##### ◽셀레니움 함수 : 이미지만 추가로 확인

# - 이미지(기존) : #mArticle > div.cont_photo.no_category > div.photo_area > ul > li.size_l > a
# - 이미지(변경) : #mArticle > div.cont_photo > div.photo_area > ul > li.size_l > a

# In[ ]:


import json
import requests
import time
from tqdm.notebook import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

def selenium_only_image(url):    
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
    driver.implicitly_wait(8)
    driver.get(url)
    try :
        image = driver.find_element_by_css_selector('''#mArticle > div.cont_photo > div.photo_area > ul > li.size_l > a''')
    except:
        pass
    else:
        image = 'https:'+image.get_attribute('style')[23:-3]
    driver.quit()
    time.sleep(0.5)

    return image

# In[ ]:


len(not_image)

# In[ ]:


#mArticle > div.cont_photo.no_category > div.photo_area > ul > li > a

# - 각 행의 place_url을 통해 해당 정보 추출

# In[ ]:


from tqdm.notebook import tqdm
# len(not_image) == 1117
for idx in tqdm(range(1005, len(not_image), 1)):
    target_idx = not_image.loc[idx, 'idx']
    url = accom_all.loc[target_idx, 'place_url']
    image = selenium_only_image(url)
    if image != False:
        accom_all.loc[target_idx, 'image'] = image
        not_image.loc[idx, 'image'] = image

# - 오류가 발생하므로 각각의 데이터를 저장 후 합쳐주었다.

# In[ ]:


# accom_all.to_excel('./data/220117/숙박_selenium.xlsx', index=False)
# not_image.to_excel('./data/220116/not_image.xlsx', index=False)

# ##### ◽이미지 데이터 다운로드

# - 이미지 다운로드 함수 : 위에서 사용한 함수 그대로 사용

# In[ ]:


import requests

def image_download(place_name, place_id, place_image_url):    
    response = requests.get(place_image_url)
    name = f'{place_name}_{place_id}'
    # 이름 내에 슬래시('/')가 있으면 디렉터리로 인식하므로
    # replace를 통해 변경해준다.
    if '/' in name:
        name = name.replace('/', '-')
    # with open("./data/220116/숙박 시설 이미지/{}.png".format(name), "wb") as f:
    with open("./data/220116/숙박 시설 없던 것들/{}.png".format(name), "wb") as f:
        f.write(response.content)

# - 데이터 불러오기

# In[ ]:


import pandas as pd

not_image_down = pd.read_excel('./data/220116/not_image_all.xlsx', index_col=False)
accom_all = pd.read_excel('./data/220117/숙박_selenium_all.xlsx', index_col = False)

# In[ ]:


accom_all.head(1)

# In[ ]:


not_image_down.head(1)

# In[ ]:


(not_image_down['image'] != 'Not Image').value_counts()

# - 이미지 저장

# In[ ]:


import pandas as pd
import time
from tqdm.notebook import tqdm

for idx in tqdm(range(len(not_image_down))):
    target_idx, p_id, p_image = not_image_down.loc[idx, ['idx', 'id', 'image']]
    p_name = accom_all.loc[target_idx, 'place_name']
    if p_image == 'Not Image':
        continue
    image_download(p_name, p_id, p_image)
    time.sleep(0.5)

# #### 5. 이미지 변경 : 로고, 음식 사진인 경우 변경

# ##### ◽이미지 변경할 경우 id 확인

# - 이미지가 로고, 음식 등 해당 장소를 특정하기 힘든 경우 다른 이미지로 변경한다.
# - 장소명과 id를 통해 변경할 이미지를 직접 찾는다.
#    - `https://place.map.kakao.com/[id]` : 카카오맵 장소 정보 URL
#    - 해당 페이지에 접속하여 직접 이미지를 찾고 이미지 주소를 추가한다.

# In[ ]:


import os
import pandas as pd

id_list = []
name_list = []
for file in os.listdir('./data/220116/숙박 시설 확인할 것들'):
    split_file = file.split('_')
    id_list.append(split_file[-1][:-4])
    name_list.append(split_file[0])

# In[ ]:


change_id = pd.DataFrame({'id' : id_list, 'place_name' : name_list})
change_id['image'] = ''

# In[ ]:


change_id.to_excel('./data/220116/chage_id_all.xlsx',index = False)

# ##### ◽이미지 다운로드

# - 데이터 확인

# In[ ]:


import pandas as pd

change_image = pd.read_excel('./data/220116/chage_id_all.xlsx', index_col=False)

# In[ ]:


change_image.head(1)

# - 이미지 다운로드 함수

# In[ ]:


import requests

def image_download(place_name, place_id, place_image_url):    
    response = requests.get(place_image_url)
    name = f'{place_name}_{place_id}'
    # 이름 내에 슬래시('/')가 있으면 디렉터리로 인식하므로
    # replace를 통해 변경해준다.
    if '/' in name:
        name = name.replace('/', '-')
    with open("./data/220116/숙박 시설 확인_추가/{}.png".format(name), "wb") as f:
        f.write(response.content)

# - 이미지 다운로드

# In[ ]:


import pandas as pd
import time
from tqdm.notebook import tqdm

not_image = pd.DataFrame({'place_name' : [], 'id' : [], 'idx' : []})
cnt = 0
for idx in tqdm(range(len(change_image))):
    p_name, p_id, p_image = change_image.loc[idx, ['place_name', 'id', 'image']]

    image_download(p_name, p_id, p_image)
    time.sleep(0.5)

# ##### ◽URL 업데이트

# - 최종 데이터에 URL을 변경 버전으로 업데이트한다.

# In[ ]:


import pandas as pd

change_image = pd.read_excel('./data/220116/chage_id_all.xlsx', index_col=False)
accom_all = pd.read_excel('./data/220117/숙박_selenium_all.xlsx', index_col = False)

# In[ ]:


change_image.head(1)

# In[ ]:


accom_all.head(1)

# In[ ]:


len(change_image), len(change_image['id'].unique())

# - 이미지 URL 업데이트

# In[ ]:


from tqdm.notebook import tqdm

for idx in tqdm(range(len(change_image))):
    accom_id = change_image.loc[idx, 'id']
    accom_idx = accom_all[accom_all['id'] == accom_id].index
    accom_all.loc[accom_idx, 'image'] = change_image.loc[idx, 'image']

# In[ ]:


# accom_all.to_excel('./data/220117/숙박_selenium_최종.xlsx', index=False)

# - 총 이미지 2569개 확보

# In[ ]:


(accom_all['image'] != 'Not Image').value_counts()
