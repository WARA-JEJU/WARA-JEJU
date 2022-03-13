#!/usr/bin/env python
# coding: utf-8

# # 데이터 수집

# ## 1. 카카오맵 api를 통해 키워드별 장소 크롤링

# In[30]:


import json
import requests
# REST 키
headers = {"Authorization": "KakaoAK 7d323e26f84156c6194a9d77f33e1e6a"}
# 파라미터
params = {"query" : "제주도 일도1동 가볼만한 곳", "page" : 1, "size" : 15,"category_group_code" : "AT4"}
url = "https://dapi.kakao.com/v2/local/search/keyword.json"

# GET을 이용하여 획득
res = requests.get(url, headers=headers, params=params)
# Json을 이용하여 해제
doc = json.loads(res.text)
# 200일 경우 정상
res.status_code

# In[31]:


doc

# In[15]:


doc["documents"]

# In[ ]:


# 반복문을 통해 크롤링 데이터 => 데이터프레임화
import pandas as pd

test_df = pd.DataFrame(doc["documents"][0],index = [0])

for i in range(len(doc["documents"])):
    merge_df = pd.DataFrame(doc["documents"][i],index = [i])
    test_df = pd.concat([test_df,merge_df])


test_df


# ## 2. 평점과 이미지 크롤링

# In[34]:


from selenium import webdriver

driver = webdriver.Chrome("driver/chromedriver") # 크롬 드라이버 경로 지정 
driver.get("http://place.map.kakao.com/12710968") # get 명령으로 접근하고 싶은 주소 지정  

# In[78]:


import pandas as pd
img_df = pd.read_excel("Final_pro/JEJU_POIAPI4.xlsx")
img_df.head()

# In[80]:


img_df["rating"] = ""
img_df["img_link"] = ""

# In[81]:


import matplotlib.pyplot as plt

# In[77]:


import time
for idx,i in img_df.iterrows():
    time.sleep(0.7)
    driver = webdriver.Chrome("driver/chromedriver") # 크롬 드라이버 경로 지정 
    url = i["place_url"]
    driver.implicitly_wait(8)
    driver.get(url)
    contents = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b")
    rating = contents.text
    img_df["rating"][idx] = rating

    try:
        image = driver.find_element_by_css_selector("#mArticle > div.cont_photo > div.photo_area > ul > li.size_l > a")
        
    except:
        name = str(idx) + "_" + i["place_name"]
        plt.savefig(f"Final_pro/error/idx_{name}.png")
        driver.quit()

    else:
        img_link = image.get_attribute("style")[23:-3]
        img_link = "https:" + img_link
        img_df["img_link"][idx] = img_link

        response = requests.get(img_df["img_link"][idx])
        name = str(idx) + "_" + i["place_name"]
        with open("Final_pro/img/{}.jpg".format(name), "wb") as f:
            f.write(response.content)
        driver.quit()
        

# # 카카오 네비를 이용한 경로 탐색

# In[ ]:


URL_base = "https://apis-navi.kakaomobility.com/v1/directions?"
origin = "origin=127.11015314141542,37.39472714688412&"
destination = "destination=127.10824367964793,37.401937080111644&"
waypoints = "waypoints=127.11341936045922,37.39639094915999&"
priority = "priority=RECOMMEND&"
car_type = "car_fuel=GASOLINE&car_hipass=True&summary=True"

URL = URL_base + origin + destination + waypoints + priority + car_type


headers = {"Authorization": "KakaoAK 7d323e26f84156c6194a9d77f33e1e6a"}

# In[ ]:


test = requests.get(URL,headers=headers).json()
test

# In[ ]:


test["routes"][0]["summary"]["duration"]

# In[ ]:


url2 = "https://apis-navi.kakaomobility.com/v1/directions?origin=127.11015314141542,37.39472714688412&destination=127.10824367964793,37.401937080111644&waypoints=&priority=RECOMMEND&car_fuel=GASOLINE&car_hipass=false&alternatives=false&road_details=false"

# In[ ]:


all_re = requests.get(url2,headers=headers).json()
all_re

# In[ ]:


#경로내 좌표
vertexes = []
for road in all_re['routes'][0]['sections'][0]['roads']:
    test_v = road['vertexes']
    for i in range(0, len(test_v), 2):
        vertexes.append((test_v[i+1], test_v[i]))

# In[ ]:


import folium
import pandas as pd

origin = all_re['routes'][0]['summary']['origin']
destination = all_re['routes'][0]['summary']['destination']

map = folium.Map(location=[origin['y'], origin['x']], zoom_start=9)
folium.Marker(location=[origin['y'], origin['x']], popup='origin').add_to(map)
folium.Marker(location=[destination['y'], destination['x']], popup='destination').add_to(map)
folium.PolyLine(vertexes, color='red').add_to(map)
map
