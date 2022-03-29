import json

import pandas as pd
import requests
from urllib.request import urlopen
from pandas import read_csv

jeju_range = read_csv("./제주특별자치도_숙박_병합_KAKAO.csv", encoding="UTF-8")


# 네이버 TM128 좌표 조회 API Start
def naver_search_result(jeju_name):
    result = []

    # REST 키
    client_key = 'rpUjPR07Z_lq_zcln2nX' #rpUjPR07Z_lq_zcln2nX,xzjv8j9BbPlDkjv3L4cP
    client_secret = 'n6xR0YpYs4'        #n6xR0YpYs4, qXSjpcpeln
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
        if doc['total'] > 0:
            result.extend(doc['items'])
    return result


def naver_search_df():
    category = ['roadAddress', 'mapx', 'mapy']
    results = []
    for idx, row in jeju_range.iterrows():
        if row['x'] == '' or pd.isna(row['x']):
            print("제주도 %s (%d건 진행중)" % (row['상호명'], idx))
            r = pd.DataFrame(naver_search_result('제주도' + row['상호명']))
            for bowl in category:
                try:
                    if bowl == 'mapx':
                        if row['x'] == '' or pd.isna(row['x']):
                            print('기존 = %s, 새로운 = %s (%s)' % (row['x'], r[bowl][0], bowl))
                            row['x'] = r[bowl][0]
                    elif bowl == 'mapy':
                        if row['y'] == '' or pd.isna(row['y']):
                            print('기존 = %s, 새로운 = %s (%s)' % (row['y'], r[bowl][0], bowl))
                            row['y'] = r[bowl][0]
                    elif bowl == 'roadAddress':
                        if row['address'] == '' or pd.isna(row['address']):
                            print('기존 = %s, 새로운 = %s (%s)' % (row['address'], r[bowl][0], bowl))
                            row['address'] = r[bowl][0]
                except:
                    break
        results.append(row.copy())
    return pd.DataFrame(results).reset_index(drop=True)


jeju_range = naver_search_df()
jeju_range.to_csv('./제주특별자치도_숙박_병합_네이버.csv', index=False)  # 구분자를 탭으로 하여 저장. 인덱스칼럼은 저장 안함.
