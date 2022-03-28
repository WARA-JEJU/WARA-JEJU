import json

import pandas as pd
import requests
from urllib.request import urlopen
from pandas import read_csv

jeju_range = read_csv("./제주특별자치도_지리_병합_네이버.csv", encoding="UTF-8")


# 카카오 KTM to WGS84 조회 API Start
def kakao_WGS84_result(x, y):
    result = []
    # REST 키
    rest_api_key = '45d7de218a156d51a78cc450e4a32c6b'
    # 헤더
    headers = {"Authorization": "KakaoAK {}".format(rest_api_key)}  # KakaoAK 45d7de218a156d51a78cc450e4a32c6b
    # 파라미터
    params = {"x": x, "y": y, "input_coord": 'KTM', "output_coord": 'WGS84'}
    url = "https://dapi.kakao.com/v2/local/geo/transcoord.json"

    try:
        # GET을 이용하여 획득
        res = requests.get(url, headers=headers, params=params)
    except:
        page = urlopen(url)
        # bytes to string
        doc = page.read().decode('utf-8')
        # string to dictionary
        result.extend(json.loads(doc.text)['documents'])
    else:
        if res.status_code == 200:
            # Json을 이용하여 해제
            doc = json.loads(res.text)
            result.extend(doc['documents'])
    return result


def kakao_WGS84_df():
    category = ['x', 'y']
    results = []
    for idx, row in jeju_range.iterrows():
        if row['x'] != '' and not pd.isna(row['x']):
            if str(row['x']).find('.') > 3 or str(row['x']).find('.') < 0:
                print("제주도 %s (%d건 진행중)" % (row['상호명'], idx))
                r = pd.DataFrame(kakao_WGS84_result(row['x'], row['y']))
                for bowl in category:
                    try:
                        print('기존 = %s, 새로운 = %s (%s)' % (row[bowl], r[bowl][0], bowl))
                        row[bowl] = r[bowl][0]
                    except:
                        break
        results.append(row.copy())
    return pd.DataFrame(results).reset_index(drop=True)


jeju_range = kakao_WGS84_df()
jeju_range.to_csv('./제주특별자치도_지리_병합_네이버_이미지_변환_크롤링.csv', index=False)  # 구분자를 탭으로 하여 저장. 인덱스칼럼은 저장 안함.
