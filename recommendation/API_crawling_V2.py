#!pip install selenium
#!pip install pandas
#!pip install matplotlib
#!pip install pyproj

import pandas as pd

jeju_range = pd.read_csv("/제주특별자치도_숙박업현황_01_02_2020.csv", encoding="CP949")
jeju_range['address'] = ''  # 도로명 Data
jeju_range['x'] = ''  # 경도 Data
jeju_range['y'] = ''  # 위도 Data
jeju_range['place_url'] = ''  # 카카오 Map URL Data
jeju_range['thumbnail'] = ''  # 썸네일 Image Url Data
jeju_range['image_link'] = ''  # Image Url Data
jeju_range.tail()

## 카카오 경도, 경도, 리뷰 링크 조회 API Start

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


import pandas as pd
from tqdm.notebook import tqdm  # python 진행률 프로세스바


def kakao_search_df():
    category = ['address_name', 'x', 'y', 'place_url']
    for idx, row in tqdm(jeju_range.iterrows()):
        print('업소명 = 제주도 ' + row['업소명'])
        r = pd.DataFrame(kakao_search_result('제주도' + row['업소명']))
        for bowl in category:
            try:
                print(bowl + ' = ' + r[bowl][0])
                if bowl == 'address_name':
                    jeju_range['address'][idx] = r[bowl][0]
                else:
                    jeju_range[bowl][idx] = r[bowl][0]
            except:
                break
    return pd.DataFrame(jeju_range)


kakao_search_df()

jeju_range.tail()

jeju_range["kakao_grade"] = ''
jeju_range["kakao_review"] = ''
jeju_range["kakao_img"] = ''

jeju_range[jeju_range['place_url'] != '']

## 카카오 경도, 위도, 리뷰 링크 조회 API End

## 크롬드라이버 크롤링 Start

from selenium import webdriver
import matplotlib.pyplot as plt
import time


def kakao_crawling():
    for idx, i in tqdm(jeju_range.iterrows()):
        time.sleep(0.7)
        driver = webdriver.Chrome("driver/chromedriver")  # 크롬 드라이버 경로 지정
        url = i["place_url"]
        driver.implicitly_wait(8)
        driver.get(url)
        # grade = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div > div.place_details > div.location_evaluation > a.link_score > span.color_b2 > span:nth-child(1)")
        grade = driver.find_element_by_css_selector(
            "#mArticle > div.cont_essential > div > div.place_details > div.location_evaluation > a.link_score > span:nth-child(1) > span:nth-child(1)")
        kakao_grade = grade.text
        jeju_range["kakao_grade"][idx] = kakao_grade

        review = driver.find_element_by_css_selector(
            "#mArticle > div.cont_essential > div > div.place_details > div.location_evaluation > a.link_review > span > span:nth-child(1)")
        kakao_review = review.text
        jeju_range["kakao_review"][idx] = kakao_review

        try:
            image = driver.find_element_by_css_selector("#mArticle > div.cont_photo > ul > li:nth-child(1) > a > span")

        except:
            name = str(idx) + "_" + i["place_name"]
            plt.savefig(f"Final_pro/error/idx_{name}.png")
            driver.quit()

        else:
            image = image.get_attribute("style")[23:-3]
            kakao_img = "https:" + image
            jeju_range["kakao_img"][idx] = kakao_img

            # with open("Final_pro/img/{}.jpg".format(name), "wb") as f:
            #    f.write(response.content)

            driver.quit()


kakao_crawling()
jeju_range.tall()

## 크롬드라이버 크롤링 End

## 네이버 TM128 좌표 조회 API Start

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
    url = "https://openapi.naver.com/v1/search/local.json?query=" + jeju_name

    # GET을 이용하여 획득
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        # Json을 이용하여 해제
        doc = json.loads(res.text)
        result.extend(doc['items'])

    return result


import pandas as pd
from tqdm.notebook import tqdm  # python 진행률 프로세스바


def navar_search_df():
    category = ['address', 'mapx', 'mapy', 'link']
    for idx, row in tqdm(jeju_range.iterrows()):
        if row['x'] == '':
            print('업소명 = 제주도 ' + row['업소명'])
            r = pd.DataFrame(naver_search_result('제주도' + row['업소명']))
            for bowl in category:
                try:
                    print(bowl + ' = ' + r[bowl][0])
                    if bowl == 'mapx':
                        jeju_range['x'][idx] = r[bowl][0]
                    elif bowl == 'mapy':
                        jeju_range['y'][idx] = r[bowl][0]
                    # elif  bowl == 'link':
                    #  jeju_range['place_url'][idx] = r[bowl][0]
                    else:
                        jeju_range[bowl][idx] = r[bowl][0]
                except:
                    break
                # finally:
                #  if jeju_range['x'][idx] != '' and jeju_range['y'][idx] != '':
                #    x,y = tm128_to_wgs84(jeju_range['x'][idx], jeju_range['y'][idx])
                #    jeju_range['x'][idx] = x
                #    jeju_range['y'][idx] = y
    return pd.DataFrame(jeju_range)


# from pyproj import Proj
# from pyproj import transform

# WGS84 = { 'proj':'latlong', 'datum':'WGS84', 'ellps':'WGS84', }

# TM128 = { 'proj':'tmerc', 'lat_0':'38N', 'lon_0':'128E', 'ellps':'bessel',
#        'x_0':'400000', 'y_0':'600000', 'k':'0.9999',
#        'towgs84':'-146.43,507.89,681.46'}

# def tm128_to_wgs84(x, y):
#   return transform( Proj(**TM128), Proj(**WGS84), x, y )

navar_search_df()
jeju_range.tail()

## 네이버 TM128 좌표 조회 API End

## 네이버 이미지 조회 API Start

import json
import requests


def naver_image_result(jeju_name):
    result = []

    # REST 키
    client_key = 'xzjv8j9BbPlDkjv3L4cP'
    client_secret = 'qXSjpcpeln'
    # 헤더
    headers = {"X-Naver-Client-Id": client_key,
               "X-Naver-Client-Secret": client_secret}
    # 파라미터
    url = "https://openapi.naver.com/v1/search/image?query=" + jeju_name

    # GET을 이용하여 획득
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        # Json을 이용하여 해제
        doc = json.loads(res.text)
        result.extend(doc['items'])

    return result


import pandas as pd
from tqdm.notebook import tqdm  # python 진행률 프로세스바


def navar_image_df():
    category = ['link', 'thumbnail']
    for idx, row in tqdm(jeju_range.iterrows()):
        if row['x'] == '':
            print('업소명 = 제주도 ' + row['업소명'])
            r = pd.DataFrame(naver_image_result('제주도' + row['업소명']))
            for bowl in category:
                try:
                    print(bowl + ' = ' + r[bowl][0])
                    if bowl == 'link':
                        jeju_range['image_link'][idx] = r[bowl][0]
                    else:
                        jeju_range[bowl][idx] = r[bowl][0]
                except:
                    break
    return pd.DataFrame(jeju_range)


navar_image_df()
jeju_range.tail()

## 네이버 이미지 조회 API End

## 카카오 KTM to WGS84 조회 API Start

import json
import requests


def kakao_WGS84_result(x, y):
    result = []
    # REST 키
    rest_api_key = '45d7de218a156d51a78cc450e4a32c6b'
    # 헤더
    headers = {"Authorization": "KakaoAK {}".format(rest_api_key)}  # KakaoAK 45d7de218a156d51a78cc450e4a32c6b
    # 파라미터
    params = {"x": x, "y": y, "input_coord": 'KTM', "output_coord": 'WGS84'}
    url = "https://dapi.kakao.com/v2/local/geo/transcoord.json"

    # GET을 이용하여 획득
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        # Json을 이용하여 해제
        doc = json.loads(res.text)
        result.extend(doc['documents'])

    return result


import pandas as pd
from tqdm.notebook import tqdm  # python 진행률 프로세스바


def kakao_WGS84_df():
    category = ['x', 'y']
    for idx, row in tqdm(jeju_range.iterrows()):
        if (row['x'].find('.') > 3 or row['x'].find('.') < 0) and row['x'] != '':
            print('업소명 = 제주도 ' + row['업소명'])
            r = pd.DataFrame(kakao_WGS84_result(row['x'], row['y']))
            print(row['x'].find('.'))
            print(r['x'][0])
            for bowl in category:
                try:
                    print(r[bowl][0])
                    jeju_range[bowl][idx] = r[bowl][0]
                except:
                    break
    return pd.DataFrame(jeju_range)


kakao_WGS84_df()
jeju_range.tail()

## 카카오 KTM to WGS84 조회 API End
