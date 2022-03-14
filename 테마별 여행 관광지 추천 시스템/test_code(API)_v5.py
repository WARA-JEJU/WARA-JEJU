#!/usr/bin/env python
# coding: utf-8

# ### - 카카오 API : 네비게이션 검색

# - 카카오 API 테스트
#   - 앱 ID : 
#   - 네이티브 앱 키 : 
#   - REST API 키 : 
#   - JavaScript 키 : 
#   - Admin 키 : 
# - 키워드 검색
#   - 질의어를 통해 장소 검색 결과 반환
#   - 네비게이션 길안내 결과 반환

# - origin : 33.248678, 126.56734
# - destiantion : 33.291055, 126.461936
# - 한라산 : 33.361204769954284, 126.53111502985787
# ---
# - 경로 탐색 실패하는 경우 발생 : **출발지, 도착지 주변에 도로가 없는 경우**

# #### 1. 경로 검색

# In[ ]:


import json
import requests
# REST 키
rest_api_key = ''
# 헤더
headers = {"Authorization" : "KakaoAK {}".format(rest_api_key)}
# 파라미터
url1 = "https://apis-navi.kakaomobility.com/v1/directions?origin=126.56734,33.248678&destination=126.461936,33.291055&waypoints=&priority=RECOMMEND&car_fuel=GASOLINE&car_hipass=false&alternatives=false&road_details=false"
url2 = "https://apis-navi.kakaomobility.com/v1/directions?origin=126.56734,33.248678&destination=126.53111502985787,33.361204769954284&waypoints=&priority=RECOMMEND&car_fuel=GASOLINE&car_hipass=false&alternatives=false&road_details=false"

# GET을 이용하여 획득
res1 = requests.get(url1, headers=headers)
# Json을 이용하여 해제
doc1 = json.loads(res1.text)

res2 = requests.get(url2, headers=headers)
doc2 = json.loads(res2.text)

# 200일 경우 정상
res1.status_code, res2.status_code

# In[72]:


# 결과(Dict형으로 표현)
print(doc1['routes'][0]['result_code'], doc1['routes'][0]['result_msg'],)
doc1['routes'][0]['summary']

# In[70]:


doc2

# In[57]:


vertexes = []
for road in doc1['routes'][0]['sections'][0]['roads']:
    test_v = road['vertexes']
    for i in range(0, len(test_v), 2):
        vertexes.append((test_v[i+1], test_v[i]))

# In[58]:


vertexes[:10]

# #### 2. 경로 표현

# In[59]:


import folium
import pandas as pd

origin = doc1['routes'][0]['summary']['origin']
destination = doc1['routes'][0]['summary']['destination']

map = folium.Map(location=[origin['y'], origin['x']], zoom_start=9)
folium.Marker(location=[origin['y'], origin['x']], popup='origin').add_to(map)
folium.Marker(location=[destination['y'], destination['x']], popup='destination').add_to(map)
folium.PolyLine(vertexes, color='red').add_to(map)
map

# ### - 데이터 확인

# #### 1. POI 정보

# In[1]:


import pandas as pd

poi_df = pd.read_excel('./data/220112/POI_장소처리_del.xlsx')

# In[2]:


poi_df.head()

# In[3]:


poi_df.info()

# In[4]:


poi_df['구분'].value_counts()

# In[5]:


(poi_df['구분'] == '숙박').value_counts()

# #### 2. 식당 데이터

# - 식당 정보

# In[ ]:


restaurant_df = pd.read_excel('./data/식당/제주도 식당 정보_전체.xlsx')
restaurant_df.shape

# In[ ]:


restaurant_df.columns
