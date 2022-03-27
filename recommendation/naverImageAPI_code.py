import json

import pandas as pd
import requests
from pandas import read_csv

jeju_range = read_csv("./제주특별자치도_업체_병합_case2_네이버.csv", encoding="UTF-8")


# 네이버 이미지 조회 API Start
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
        if doc['total'] > 0:
            result.extend(doc['items'])
    return result


def naver_image_df():
    category = ['link', 'thumbnail']
    results = []
    for idx, row in jeju_range.iterrows():
        if row['x'] != '' or not pd.isna(row['x']):
            if row['image_link'] == '' or row['thumbnail'] == '' or pd.isna(row['image_link']) or pd.isna(row['thumbnail']):
                print("제주도 %s (%d건 진행중)" % (row['상호명'], idx))
                r = pd.DataFrame(naver_image_result('제주도' + row['상호명']))
                for bowl in category:
                    try:
                        if bowl == 'link':
                            print('기존 = %s, 새로운 = %s (%s)' % (row['image_link'], r[bowl][0], bowl))
                            row['image_link'] = r[bowl][0]
                        else:
                            print('기존 = %s, 새로운 = %s (%s)' % (row[bowl], r[bowl][0], bowl))
                            row[bowl] = r[bowl][0]
                    except:
                        break
        results.append(row.copy())
    return pd.DataFrame(results).reset_index(drop=True)


jeju_range = naver_image_df()
jeju_range.to_csv('./제주특별자치도_업체_병합_case2_네이버_이미지.csv', index=False)  # 구분자를 탭으로 하여 저장. 인덱스칼럼은 저장 안함.
