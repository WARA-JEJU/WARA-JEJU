import json

import pandas as pd
import requests
from urllib.request import urlopen
from pandas import read_csv

jeju_range = read_csv("./제주특별자치도_음식_병합.csv", encoding="CP949")
jeju_range = jeju_range.rename(columns={'도로명주소': 'address', '위도': 'y', '경도': 'x', '업소명': '상호명'})
jeju_range['place_url'] = ''  # 카카오 Map URL Data
jeju_range['thumbnail'] = ''  # 썸네일 Image Url Data
jeju_range['image_link'] = ''  # Image Url Data


# 네이버 TM128 좌표 조회 API Start
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

    while True:
        try:
            # GET을 이용하여 획득
            res = requests.get(url, headers=headers)
        except:
            page = urlopen(url)
            # bytes to string
            doc = page.read().decode('utf-8')
            # string to dictionary
            result.extend(json.loads(doc.text)['items'])
        else:
            if res.status_code == 200:
                # Json을 이용하여 해제
                doc = json.loads(res.text)
                result.extend(doc['items'])
    return result


def naver_search_df():
    category = ['address', 'mapx', 'mapy']
    results = []
    for idx, row in jeju_range.iterrows():
        if row['x'] == '' or pd.isna(row['x']):
            print("제주도 %s (%d건 진행중)" % (row['상호명'], idx))
            r = pd.DataFrame(naver_search_result('제주도' + row['상호명']))
            for bowl in category:
                try:
                    if bowl == 'mapx':
                        if row['x'] == '' or pd.isna(row['x']):
                            print('기존 = %s, 새로운 = %s (%s)' % (row[bowl], r[bowl][0], bowl))
                            row['x'] = r[bowl][0]
                    elif bowl == 'mapy':
                        if row['y'] == '' or pd.isna(row['y']):
                            print('기존 = %s, 새로운 = %s (%s)' % (row[bowl], r[bowl][0], bowl))
                            row['y'] = r[bowl][0]
                    else:
                        if row[bowl] == '' or pd.isna(row[bowl]):
                            print('기존 = %s, 새로운 = %s (%s)' % (row[bowl], r[bowl][0], bowl))
                            row[bowl] = r[bowl][0]
                except:
                    break
        results.append(row.copy())
    return pd.DataFrame(results).reset_index(drop=True)


jeju_range = naver_search_df()
jeju_range.to_csv('./제주특별자치도_음식_병합_NAVER.csv', index=False)  # 구분자를 탭으로 하여 저장. 인덱스칼럼은 저장 안함.
