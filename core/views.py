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
from itertools import permutations
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from tqdm.notebook import tqdm
import urllib


# Create your views here.
def home(request):
    if request.method == 'GET':
        context = {
            "name" : request.GET.get("name"),
            "select" : request.GET.get("select")
        }
        try:
            select = request.GET.get("select")
            name = request.GET.get("name")
            if select is not None or name is not None:
                # 제주도 POI(장소) 데이터
                jeju_poi_path = '제주특별자치도_최종_병합2.csv'

                jeju_poi = pd.read_csv(jeju_poi_path, index_col=False)
                jeju_poi['기타'] = jeju_poi['상호명'] + ' ' + jeju_poi['category_name']
                jeju_poi = jeju_poi[jeju_poi['기타'].notnull()]
                jeju_poi = jeju_poi[jeju_poi['thumbnail'].notnull()]

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
                    # input_result를 이용해 count_vector 생성
                    input_mat = count_vect.transform([' '.join(input_result)])
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
                    # 코사인 유사도 컬럼 추가
                    original['input_sim'] = [round(x[0], 1) for x in input_sim]

                    # 유사도 결과 Top 5 반환
                    return original[original['input_sim'] > 0.2].sort_values(['input_sim', 'kakao_grade', 'kakao_review'],
                                                                             ascending=False).iloc[:5, :]

                # 코사인 유사도 확인
                cosine_poi = get_cosine_top5(jeju_poi.copy(), name).reset_index(drop=True)
                # row['thumbnail'],o row['kakao_grade'], row['kakao_review'], row['기타'], row['상호명'], row['input_sim']

                context = {
                    "cosine_pois": cosine_poi.to_dict('list'),
                }

        except AttributeError:
            print('AttributeError')
        finally:
            print(context)
            return render(request, 'index.html', context)


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
