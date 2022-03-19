#!pip install selenium
# !pip install pandas
# !pip install matplotlib

import pandas as pd

jeju_range = pd.read_csv("제주(POI)_필터링.csv", encoding="utf-8")
jeju_range.tail()

# CSV 파일을 한행씩 읽어서 API 함수 호출

import pandas as pd
from tqdm.notebook import tqdm  # python 진행률 프로세스바


def kakao_search_df():
    results = []
    for idx, row in tqdm(jeju_range.iterrows()):
        r = pd.DataFrame(kakao_search_result(row['업종명']))
        jeju_range['address'][idx] = r['address_name']
        jeju_range['x'][idx] = r['x']
        jeju_range['y'][idx] = r['y']
        jeju_range['plase_url'][idx] = r['plase_url']
        results.append(r.copy())
    return pd.concat(results).reset_index(drop=True)


# API 함수 호출하여
#1.keyword: 테마파크
#2.address_name: 제주특별자치도제주시연동 1320
#3.category_group_code: CT1
#4.category_group_name: 문화시설
#5.category_name: 문화, 예술 > 문화시설 > 박물관
#6.distance: null
#7.id: 26388484
#8.phone: 064 - 742 - 3700
#9.place_name: 수목원테마파크 아이스뮤지엄
#10.place_url: http: // place.map.kakao.com / 26388484
#11.road_address_name: 제주특별자치도 제주시 은수길 69
#12. x: 126.488397743899
#13.y: 33.4707773213401

import json
import requests


def kakao_search_result(jeju_name):
    result = []

    # REST 키
    rest_api_key = '45d7de218a156d51a78cc450e4a32c6b'
    # 헤더
    headers = {"Authorization": "KakaoAK {}".format(rest_api_key)}  # KakaoAK 45d7de218a156d51a78cc450e4a32c6b
    # 파라미터
    params = {"query": f"{jeju_name}", "page": 1}
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


jeju_api = kakao_search_df()

jeju_api.head(2)

jeju_api["kakao_grade"] = ""
jeju_api["kakao_review"] = ""
jeju_api["kakao_img"] = ""

# Kakao Map 크롤링

from selenium import webdriver
import matplotlib.pyplot as plt
import time


def kakao_crawling():
    for idx, i in tqdm(jeju_api.iterrows()):
        time.sleep(0.7)
        driver = webdriver.Chrome("driver/chromedriver")  # 크롬 드라이버 경로 지정
        url = i["place_url"]
        driver.implicitly_wait(8)
        driver.get(url)
        # grade = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div > div.place_details > div.location_evaluation > a.link_score > span.color_b2 > span:nth-child(1)")
        grade = driver.find_element_by_css_selector(
            "#mArticle > div.cont_essential > div > div.place_details > div.location_evaluation > a.link_score > span:nth-child(1) > span:nth-child(1)")
        kakao_grade = grade.text
        jeju_api["kakao_grade"][idx] = kakao_grade

        review = driver.find_element_by_css_selector(
            "#mArticle > div.cont_essential > div > div.place_details > div.location_evaluation > a.link_review > span > span:nth-child(1)")
        kakao_review = review.text
        jeju_api["kakao_review"][idx] = kakao_review

        try:
            image = driver.find_element_by_css_selector("#mArticle > div.cont_photo > ul > li:nth-child(1) > a > span")

        except:
            name = str(idx) + "_" + i["place_name"]
            plt.savefig(f"Final_pro/error/idx_{name}.png")
            driver.quit()

        else:
            image = image.get_attribute("style")[23:-3]
            kakao_img = "https:" + image
            jeju_api["kakao_img"][idx] = kakao_img

            # with open("Final_pro/img/{}.jpg".format(name), "wb") as f:
            #    f.write(response.content)

            driver.quit()


jeju_kakao_crawling = kakao_crawling()

jeju_kakao_crawling.head(2)

# Naver API를 통해 좌표 정보 취득

import json
import urllib
import requests

# REST 키
client_key = 'xzjv8j9BbPlDkjv3L4cP'
client_secret = 'qXSjpcpeln'
# 헤더
headers = {"X-Naver-Client-Id": client_key,
           "X-Naver-Client-Secret": client_secret}
# 파라미터
encText = urllib.parse.quote("제주 소리섬박물관")
url = "https://openapi.naver.com/v1/search/local.json?query=" + encText

# GET을 이용하여 획득
res = requests.get(url, headers=headers)
# Json을 이용하여 해제
doc = json.loads(res.text)
# 200일 경우 정상
res.status_code

import json
import requests


def naver_search_result(jeju_name):
    result = []

    # REST 키
    client_key = 'xzjv8j9BbPlDkjv3L4cP'
    client_secret = 'qXSjpcpeln'
    # 헤더
    headers = {"X-Naver-Client-Id": client_key,
               "X-Naver-Client-Secret": client_secret}
    # 파라미터
    encText = urllib.parse.quote(f"{jeju_name}")
    url = "https://openapi.naver.com/v1/search/local.json?query=" + encText

    # GET을 이용하여 획득
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        # Json을 이용하여 해제
        doc = json.loads(res.text)
        result.extend(doc['item'])

    return result


import pandas as pd
from tqdm.notebook import tqdm  # python 진행률 프로세스바


def navar_search_df():
    results = []
    for idx, row in tqdm(jeju_kakao_crawling.iterrows()):
        r = pd.DataFrame(kakao_search_result(row['업종명']))
        jeju_kakao_crawling['address'][idx] = r['address']
        jeju_kakao_crawling['x'][idx] = r['mapx']
        jeju_kakao_crawling['y'][idx] = r['mapy']
        jeju_kakao_crawling['plase_url'][idx] = r['link']
        results.append(r.copy())
    return pd.concat(results).reset_index(drop=True)


jeju_naver_api = navar_search_df()

jeju_naver_api.head(2)
