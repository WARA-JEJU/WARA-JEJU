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


# 카카오 경도, 경도, 리뷰 링크 조회 API Start
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
                if doc['meta']['is_end']:
                    break
                else:
                    params['page'] += 1
    return result


def kakao_search_df():
    category = ['address_name', 'x', 'y', 'place_url']
    results = []
    for idx, row in jeju_range.iterrows():
        if row['place_url'] == '' or pd.isna(row['place_url']):
            print("제주도 %s (%d건 진행중)" % (row['상호명'], idx))
            r = pd.DataFrame(kakao_search_result('제주도' + row['상호명']))
            for bowl in category:
                try:
                    if bowl == 'address_name':
                        if row['address'] == '' or pd.isna(row['address']):
                            print('기존 = %s, 새로운 = %s (%s)' % (row[bowl], r[bowl][0], bowl))
                            row['address'] = r[bowl][0]
                    else:
                        if row[bowl] == '' or pd.isna(row[bowl]):
                            print('기존 = %s, 새로운 = %s (%s)' % (row[bowl], r[bowl][0], bowl))
                            row[bowl] = r[bowl][0]
                except:
                    break
        results.append(row.copy())
    return pd.DataFrame(results).reset_index(drop=True)


jeju_range = kakao_search_df()
jeju_range.to_csv('./제주특별자치도_음식_병합_KAKAO.csv', index=False)  # 구분자를 탭으로 하여 저장. 인덱스칼럼은 저장 안함.
