from django.contrib.auth import login
from django.shortcuts import render, redirect
from . import forms
import json
import requests
import folium
import pandas as pd
import numpy as np
import matplotlib.font_manager as fm
import matplotlib as mpl
import matplotlib.pyplot as plt
# from itertools import permutations
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from tqdm.notebook import tqdm
import urllib


# Create your views here.
def home(request):
    if request.method == 'GET':
        print(request)
        try:
            print(request.name)
            # 제주도 POI(장소) 데이터
            jeju_poi_path = '제주특별자치도_최종_병합.csv'

            # 제주도 중심 좌표 (x, y)
            # jeju_pos = [126.54536611348854, 33.38394921171469]

            # 시작 좌표 (x, y) : 제주국제공항
            # default_pos = [126.49411256317285, 33.50589515795999]

            # 기본 컬럼
            columns = ['업종', '상호명', '행정시', 'address_name', 'road_address_name', 'phone', 'y',
                       'x', 'place_url', 'thumbnail', 'image_link', 'kakao_grade',
                       'kakao_review', 'category_group_code', 'category_group_name',
                       'category_name', '기타']

            # past_poi = None
            # past_pos = default_pos
            jeju_poi = pd.read_csv(jeju_poi_path, index_col=False)
            jeju_poi['기타'] = jeju_poi['상호명'] + ' ' + jeju_poi['category_name']
            jeju_poi = jeju_poi[jeju_poi['기타'].notnull()]
            jeju_poi = jeju_poi[jeju_poi['thumbnail'].notnull()]
            recommand_poi = pd.DataFrame(columns=columns)

            # 좌표간의 직선 거리 계산 함수
            # pos1 : (x좌표, y좌표)
            # pos2 : (x좌표, y좌표)
            def cal_dist(pos1, pos2):
                return (((pos1[1] - pos2[1]) * 88.8) ** 2 + ((pos1[0] - pos2[0]) * 88.8) ** 2) ** (1 / 2)

            # (content, 입력값)의 count_vector matrix 반환 함수
            # category : 입력받은 카테고리 리스트
            # content : 장소 정보의 'content' 컬럼
            #           - content : keyword + category_group_name
            def get_count_mat(category, content):
                # content를 이용해 count_vector 학습
                count_vect = CountVectorizer(min_df=0, ngram_range=(1, 2))
                content_mat = count_vect.fit_transform(content)
                input_result = [category]
                # count vecter를 위해 각 단어의 공백(space) 삭제
                input_result = [input_str.replace(' ', '') for input_str in input_result]
                print(input_result)
                # input_result를 이용해 count_vector 생성
                input_mat = count_vect.transform([' '.join(input_result)])
                print(input_mat)
                print(content_mat)
                return input_mat, content_mat

            # input_mat 기준 sim_mat의 유사도 결과 반환
            # DataFrame의 컬럼으로 추가하기 위해 reshape하여 반환
            def get_cosine_sim(input_mat, sim_mat):
                input_sim = cosine_similarity(input_mat, sim_mat)
                return input_sim.reshape(-1, 1)

            # content(keyword + category_group_name) 기준 코사인 상위 Top5 반환
            # original : 코사인 유사도를 구할 원본 Dataframe
            # category : 코사인 유사도를 구할 카테고리명
            def get_cosine_top5(original, category):
                # 코사인 유사도 획득
                input_mat, content_mat = get_count_mat(category, original['기타'])
                input_sim = get_cosine_sim(input_mat, content_mat)
                print(input_sim)
                # 코사인 유사도 컬럼 추가
                original['input_sim'] = [round(x[0], 1) for x in input_sim]

                # 유사도 결과 Top 5 반환
                return original[original['input_sim'] > 0.2].sort_values(['input_sim', 'kakao_grade', 'kakao_review'],
                                                                         ascending=False).iloc[:5, :]

            # 관광명소를 추천하는 함수
            # 유클리드 거리와 평점을 기준으로 선정
            # poi_df : 전체 장소 DataFrame
            # select_id : 대표로 선정된 장소의 id
            # past_pos : 이전 장소(좌표)
            def recommand_tourism(poi_df, select_id, past_pos):
                tour_df = poi_df.query('category_group_name == "관광명소"').reset_index(drop=True)
                img_euclidean_dist = np.load(img_euclidean_path)

                idx = tour_df[tour_df['id'] == select_id].index[0]
                tour_df['img_euclidean_dist'] = img_euclidean_dist[idx]
                # 이전 장소와의 거리가 15km 이하인 경우에서만 선택
                tour_df['dist'] = cal_dist(past_pos, (tour_df['x'], tour_df['y']))
                top20 = tour_df[tour_df['dist'] <= 15].sort_values('img_euclidean_dist', ascending=True).iloc[:20, :]

                return top20[columns].sort_values('rating', ascending=False)

            # 음식점을 추천하는 함수
            # poi_df : 전체 장소 DataFrame
            # select_id : 대표로 선정된 장소의 id
            # past_pos : 이전 장소(좌표)
            def recommand_rest(poi_df, select_id, past_pos):
                rest_df = poi_df.query('category_group_name == "음식점"').reset_index(drop=True)
                food_label = pd.read_excel(rest_clip_label, index_col=False)
                rest_df.loc[:, 'food_label'] = food_label['food_label'].copy()
                food = rest_df[rest_df['id'] == select_id]['food_label'].iloc[0]
                # 이전 장소와의 거리가 15km 이하인 경우에서만 선택
                rest_df['dist'] = cal_dist(past_pos, (rest_df['x'], rest_df['y']))
                top20 = rest_df.query(f'dist <= 15 and food_label == "{food}"').iloc[:20, :]

                return top20[columns].sort_values('rating', ascending=False)

            # 카페를 추천하는 함수
            # poi_df : 전체 장소 DataFrame
            # select_id : 대표로 선정된 장소의 id(다른 함수와 동일한 형태를 유지하기 위해 사용)
            # past_pos : 이전 장소(좌표)
            def recommand_cafe(poi_df, select_id, past_pos):
                cafe_df = poi_df.query('category_group_name == "카페"').reset_index(drop=True)

                # 이전 장소와의 거리가 15km 이하인 경우에서만 선택
                cafe_df['dist'] = cal_dist(past_pos, (cafe_df['x'], cafe_df['y']))
                top20 = cafe_df[cafe_df['dist'] <= 15].sort_values('', ascending=True).iloc[:20, :]

                return top20[columns].sort_values('rating', ascending=False)

            # 매개변수 category에 따라 추천 함수 실행 후 결과 반환
            # poi_df : 전체 장소 DataFrame
            # select_id : 대표로 선정된 장소의 id
            # category : 대표로 선정된 장소의 category_group_name
            def recommand_site(poi_df, select_id, category, past_pos, included):
                if category == "관광명소":
                    temp = recommand_tourism(poi_df, select_id, past_pos)

                elif category == "음식점":
                    temp = recommand_rest(poi_df, select_id, past_pos)
                elif category == "카페":
                    temp = recommand_cafe(poi_df, select_id, past_pos)
                else:
                    print('오류 발생. 유효하지 않은 카테고리 입니다.')
                    return None
                # 추천된 관광지 삭제
                included_idx = []
                for p_id in included:
                    idx = list(temp[temp['id'] == p_id].index)
                    included_idx.extend(idx)
                # 가장 순위가 높은 관광지 추천
                if included_idx:
                    return temp.drop(included_idx, axis=0).iloc[0, :]
                else:
                    return temp.iloc[0, :]

            # 장소 좌표를 이용해 경로 탐색
            # routes : 출발지, 경로, 도착지 좌표
            # 첫 인덱스 좌표 : 출발지
            # 마지막 인덱스 좌표 : 도착지
            # 사이의 인덱스 좌표 : 경로
            def search_navi_route(routes):
                # REST 키
                rest_api_key = ''
                # 헤더
                headers = {"Authorization": "KakaoAK {}".format(rest_api_key)}
                origin = routes[0][1]
                destination = routes[-1][1]
                waypoints = [r for p_id, r in routes[1:-1]]
                waypoints = '|'.join(waypoints)
                # 파라미터
                # origin, destination : x, y
                # waypoints : x, y| x, y|...
                url = "https://apis-navi.kakaomobility.com/v1/directions?origin={}&destination={}&waypoints={}".format(
                    origin, destination, waypoints)

                # GET을 이용하여 획득
                res = requests.get(url, headers=headers)
                # Json을 이용하여 해제
                doc = json.loads(res.text)

                # 200일 경우 정상
                return res.status_code, doc

            # 경로의 좌표, 거리, 시간 반환 함수
            # routes : 출발지, 경로, 도착지 좌표
            def get_navi_vertexes(routes):
                if len(routes) <= 1:
                    print('장소를 추가하시기 바랍니다.(최소 장소 개수 : 2개)')
                    return None, None, None
                status, doc = search_navi_route(routes)
                # 경로 탐색이 된 경우 (경로, 거리, 시간) 반환
                if status == 200 and doc['routes'][0]['result_code'] == 0:
                    vertexes = []
                    for section in doc['routes'][0]['sections']:
                        for road in section['roads']:
                            test_v = road['vertexes']
                            for i in range(0, len(test_v), 2):
                                vertexes.append((test_v[i + 1], test_v[i]))
                    # 경로, 거리, 시간
                    return vertexes, doc['routes'][0]['summary']['distance'], doc['routes'][0]['summary']['duration']
                else:
                    return None, None, None

            # 경로의 직선 거리 계산 함수
            # routes : 전체 경로의 좌표((x, y)로 구성된 리스트 형태)
            def get_straight_dist(routes):
                if len(routes) <= 1:
                    print('장소를 추가하시기 바랍니다.(최소 장소 개수 : 2개)')
                    return None
                straight_dist = 0
                for i in range(len(routes) - 1):
                    straight_dist += cal_dist(routes[i][1:], routes[i + 1][1:])

                # 거리
                return straight_dist

            while True:
                # 키워드 입력
                print('카테고리 입력(입력, 종료시 0) : ', end='')
                category_result = str(input())
                if category_result == '0':
                    print('종료')  # 종료 문구
                    break
                else:
                    print(category_result)

                # 카페가 아닌 경우 코사인 유사도 확인
                if category_result != '카페':
                    print('-' * 60)
                    cosine_poi = get_cosine_top5(jeju_poi.copy(), category_result)
                    print(cosine_poi['기타'].count() > 0)
                    if cosine_poi['기타'].count() == 0:
                        continue
                    else:
                        cosine_poi = cosine_poi.reset_index(drop=True)
                        # 대표 장소 선택
                        img_info = {}
                        plt.figure(figsize=(20, 25))
                        cnt = 1
                        for idx, row in cosine_poi.iterrows():
                            plt.subplot(5, 4, cnt)
                            img_path = urllib.request.urlretrieve(str(row['thumbnail']))[0]
                            img = plt.imread(img_path)
                            plt.imshow(img)
                            title = str(cnt) + '. ' + row['기타'] + ':' + str(round(row['input_sim'], 3)) + str(
                                row['kakao_grade']) + ':' + str(row['kakao_review'])
                            plt.gca().set_title(title)
                            plt.axis(False)
                            img_info[str(cnt)] = [row['상호명'], round(row['input_sim'], 3)]
                            cnt += 1
                        plt.show()
                        print('-' * 60)
                        print('대표 장소를 선택해주시기 바랍니다. 1개만 선택')
                        print('-' * 60)
                        for key, value in img_info.items():
                            print('\t{}. {}'.format(key, value))
                        print('-' * 60)
                        print('입력(번호 선택) : ', end='')
                        cosine_num = input()
                        cosine_result = cosine_poi.iloc[int(cosine_num) - 1, :]
                        print(cosine_num, '-', cosine_result['상호명'])
                        print()

                # 관광지 추천
                included = list(recommand_poi['id'])
                if category_result == '카페':
                    recommand_poi = recommand_poi.append(
                        recommand_site(jeju_poi, None, category_result, past_pos, included))
                else:
                    recommand_poi = recommand_poi.append(
                        recommand_site(jeju_poi, cosine_result['id'], category_result, past_pos, included))
                past_pos = [recommand_poi.iloc[-1]['x'], recommand_poi.iloc[-1]['y']]
        except AttributeError:
            print('AttributeError')
        finally:
            return render(request, 'index.html')


def sign_up(request):
    form = forms.SignUpForm

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        print(request)

        if form.is_valid():
            email = form.cleaned_data.get('email').lower()

            user = form.save(commit=False)
            user.username = email
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')

    return render(request, 'sign_up.html', {'form': form})


def recommendation(request):
    form = forms.SignUpForm

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        print(request)

        if form.is_valid():
            email = form.cleaned_data.get('email').lower()

            user = form.save(commit=False)
            user.username = email
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')

    return render(request, 'sign_up.html', {'form': form})
