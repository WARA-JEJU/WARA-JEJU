#!/usr/bin/env python
# coding: utf-8

# # 컬럼명 변경 및 데이터 불러오기

# In[62]:


import pandas as pd
jeju = pd.read_csv("제주관광지_필터링.csv",encoding="utf-8")
jeju.tail()

# In[63]:


jeju.info()

# In[64]:


jeju.columns

# In[65]:


jeju.rename(columns = {'위치좌표 X축값 ' : 'x','위치좌표 Y축값 ' : "y"}, inplace = True)


# In[66]:


jeju.head()

# # 전처리

# ## 1. 좌표 값이 같고 이름이 다른 경우(중복 장소 제거)

# In[27]:




# ## 2. 관광/숙박 시설 나누기

# In[87]:


jeju_split = pd.read_excel("POI_관광_숙박.xlsx")
jeju_split

# In[88]:


jeju_accom = jeju_split.query('장소명.str.contains("호텔|민박|모텔|여관|리조트|펜션|여인숙|별장|콘도|팬션|호스텔|무인텔|하우스") or 장소명.str.endswith("텔")', engine='python')
jeju_accom


# In[89]:


for i in jeju_accom.index:
    jeju_split.drop(index = i,inplace=True)

# In[90]:


jeju_split.info()

# In[92]:


jeju_tour = jeju_split
jeju_tour

# # 크롤링

# ## 1.지역 크롤링 확인

# In[6]:


import requests
from urllib.parse import quote    
import pandas as pd

# In[7]:


client_id = ""
client_secret = ""

# In[8]:


headers = {"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}

# In[17]:


url_base="https://openapi.naver.com/v1/search/local.json?query="
keyword = quote(input("검색 키워드를 입력하세요. : "))
url_middle="&display=10&start=1&sort=random"

url = url_base + keyword + url_middle

result = requests.get(url,headers = headers).json()                  #결과값을 변수로 지정
result                                                           #결과값 출력

# In[18]:


result["total"]

# ## 2. 없어진 장소 처리

# ### 1. 숙박 업소

# In[93]:


import copy
jeju_accom.info()

# In[94]:


jeju_accom["검색결과"] = ""
jeju_accom

# In[95]:


for idx,i in jeju_accom.iterrows():
    print(idx,i["장소명"][:2])

# In[96]:


import time 
for idx,i in jeju_accom.iterrows():
    time.sleep(1.3)
    if len(i["장소명"]) > 2: 
        if i["장소명"][:2] == "제주":
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote(i["장소명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                jeju_accom.loc[idx, "검색결과"] = "없는 장소"
        else:
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote("제주" + i["장소명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                jeju_accom.loc[idx, "검색결과"] = "없는 장소"
    else:
        url_base="https://openapi.naver.com/v1/search/local.json?query="
        keyword = quote("제주" + i["장소명"])
        url_middle="&display=5 & start=1"
        url = url_base + keyword + url_middle
        result = requests.get(url,headers = headers).json()
        if result["total"] == 0:
                jeju_accom.loc[idx, "검색결과"] = "없는 장소"

# In[97]:


len(jeju_accom[jeju_accom["검색결과"] =="없는 장소"])

# In[98]:


jeju_accom

# In[104]:


jeju_accom = jeju_accom.drop(jeju_accom[jeju_accom["검색결과"]=="없는 장소"].index)

# In[105]:


jeju_accom

# ### 2. 관광지

# In[106]:


jeju_tour["검색결과"] = ""
jeju_tour

# In[107]:


import time 
for idx,i in jeju_tour.iterrows():
    time.sleep(1.5)
    if len(i["장소명"]) > 2: 
        if i["장소명"][:2] == "제주":
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote(i["장소명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                jeju_tour.loc[idx, "검색결과"] = "없는 장소"
        else:
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote("제주" + i["장소명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                jeju_tour.loc[idx, "검색결과"] = "없는 장소"
    else:
        url_base="https://openapi.naver.com/v1/search/local.json?query="
        keyword = quote("제주" + i["장소명"])
        url_middle="&display=5 & start=1"
        url = url_base + keyword + url_middle
        result = requests.get(url,headers = headers).json()
        if result["total"] == 0:
                jeju_tour.loc[idx, "검색결과"] = "없는 장소"

# In[108]:


len(jeju_tour[jeju_tour["검색결과"] =="없는 장소"])

# In[109]:


jeju_tour = jeju_tour.drop(jeju_tour[jeju_tour["검색결과"]=="없는 장소"].index)

# In[110]:


jeju_tour

# ### 3.동식물원

# In[111]:


park = pd.read_excel("POI_공원_산_동.식물원.xlsx")
park.head()

# In[112]:


park["검색결과"] = ""
park.head()

# In[113]:


import time 
for idx,i in park.iterrows():
    time.sleep(1.5)
    if len(i["장소명"]) > 2: 
        if i["장소명"][:2] == "제주":
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote(i["장소명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                park.loc[idx, "검색결과"] = "없는 장소"
        else:
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote("제주" + i["장소명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                park.loc[idx, "검색결과"] = "없는 장소"
    else:
        url_base="https://openapi.naver.com/v1/search/local.json?query="
        keyword = quote("제주" + i["장소명"])
        url_middle="&display=5 & start=1"
        url = url_base + keyword + url_middle
        result = requests.get(url,headers = headers).json()
        if result["total"] == 0:
                park.loc[idx, "검색결과"] = "없는 장소"

# In[114]:


len(park[park["검색결과"] =="없는 장소"])

# In[127]:


park = park.drop(park[park["검색결과"]=="없는 장소"].index)
park

# ### 4.레저/스포츠

# In[116]:


leisure = pd.read_excel("POI_레져_스포츠.xlsx")
leisure.head()

# In[117]:


leisure["검색결과"] = ""
leisure.head()

# In[118]:


import time 
for idx,i in leisure.iterrows():
    time.sleep(1.5)
    if len(i["장소명"]) > 2: 
        if i["장소명"][:2] == "제주":
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote(i["장소명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                leisure.loc[idx, "검색결과"] = "없는 장소"
        else:
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote("제주" + i["장소명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                leisure.loc[idx, "검색결과"] = "없는 장소"
    else:
        url_base="https://openapi.naver.com/v1/search/local.json?query="
        keyword = quote("제주" + i["장소명"])
        url_middle="&display=5 & start=1"
        url = url_base + keyword + url_middle
        result = requests.get(url,headers = headers).json()
        if result["total"] == 0:
                leisure.loc[idx, "검색결과"] = "없는 장소"

# In[119]:


len(leisure[leisure["검색결과"] =="없는 장소"])

# In[128]:


leisure = leisure.drop(leisure[leisure["검색결과"]=="없는 장소"].index)
leisure

# ### 5. 문화/예술

# In[121]:


culture = pd.read_excel("POI_문화_종교_예술.xlsx")
culture.head()

# In[122]:


culture["검색결과"] = ""
culture.head()

# In[123]:


import time 
for idx,i in culture.iterrows():
    time.sleep(1.5)
    if len(i["장소명"]) > 2: 
        if i["장소명"][:2] == "제주":
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote(i["장소명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                culture.loc[idx, "검색결과"] = "없는 장소"
        else:
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote("제주" + i["장소명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                culture.loc[idx, "검색결과"] = "없는 장소"
    else:
        url_base="https://openapi.naver.com/v1/search/local.json?query="
        keyword = quote("제주" + i["장소명"])
        url_middle="&display=5 & start=1"
        url = url_base + keyword + url_middle
        result = requests.get(url,headers = headers).json()
        if result["total"] == 0:
                culture.loc[idx, "검색결과"] = "없는 장소"

# In[124]:


len(culture[culture["검색결과"] =="없는 장소"])

# In[129]:


culture = culture.drop(culture[culture["검색결과"]=="없는 장소"].index)
culture

# ### 6. 장소처리 엑셀화

# In[130]:


jeju_accom.to_excel("숙박_장소처리.xlsx")
jeju_tour.to_excel("관광지_장소처리.xlsx")
park.to_excel("공원_장소처리.xlsx")
leisure.to_excel("레저_스포츠_장소처리.xlsx")
culture.to_excel("문화예술_장소처리.xlsx")

# ### 7. 엑셀 병합

# In[21]:


jeju_accom = pd.read_excel("final_pro/숙박_장소처리.xlsx")
jeju_accom["구분"] = "숙박"
jeju_accom.to_excel("final_pro/숙박_장소처리.xlsx")

jeju_tour = pd.read_excel("final_pro/관광지_장소처리.xlsx")
jeju_tour["구분"] = "관광지"
jeju_tour.to_excel("final_pro/관광지_장소처리.xlsx")

# In[22]:


import numpy as np  
import glob  
import sys
import pandas as pd

#파일 Union  
all_data = pd.DataFrame()  
for f in glob.glob('final_pro/*_장소처리.xlsx'):
    df = pd.read_excel(f)  
    all_data = all_data.append(df, ignore_index=True)

#데이터갯수확인  
print(all_data.shape)

#데이터 잘 들어오는지 확인  
all_data.head()

#파일저장  
all_data.to_excel("final_pro/New_data.xlsx", header=True, index=False)

# In[24]:


all_data.columns

# In[25]:


all_data.drop(['Unnamed: 0', 'Unnamed: 0.1',"검색결과",'Unnamed: 0.1.1'],axis=1,inplace=True)

# In[26]:


all_data.to_excel("final_pro/New_data.xlsx", header=True, index=False)

# ## 3.상권정보 데이터 처리

# ### 1. 크롤링을 통해 없는 데이터 제거

# In[1]:


import pandas as pd
df = pd.read_excel("Final_pro/상권정보 데이터.xlsx")
df

# In[2]:


df["세분화분류"] = ""
df["검색결과"] = ""

# In[3]:


df.columns
df

# In[4]:


chick = df[df["상권업종중분류명"]=="닭/오리요리"]
cafe = df[df["상권업종중분류명"]=="커피점/카페"]
etc = df[df["상권업종중분류명"]!="닭/오리요리"]
etc = etc[(etc["상권업종중분류명"]!="커피점/카페")]

# In[13]:


len(chick)+len(cafe)

# In[9]:


len(chick)+len(etc)+len(cafe)

# In[ ]:




# In[10]:


import time 
for idx,i in chick.iterrows():
    time.sleep(0.5)
    if len(i["상호명"]) > 2: 
        if i["상호명"][:2] == "제주":
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote(i["상호명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                df.loc[idx, "검색결과"] = "없는 장소"
        else:
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote("제주" + i["상호명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                df.loc[idx, "검색결과"] = "없는 장소"
    else:
        url_base="https://openapi.naver.com/v1/search/local.json?query="
        keyword = quote("제주" + i["상호명"])
        url_middle="&display=5 & start=1"
        url = url_base + keyword + url_middle
        result = requests.get(url,headers = headers).json()
        if result["total"] == 0:
                df.loc[idx, "검색결과"] = "없는 장소"


# In[11]:


import time 
for idx,i in cafe.iterrows():
    time.sleep(0.5)
    if len(i["상호명"]) > 2: 
        if i["상호명"][:2] == "제주":
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote(i["상호명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                df.loc[idx, "검색결과"] = "없는 장소"
        else:
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote("제주도 카페" + i["상호명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                df.loc[idx, "검색결과"] = "없는 장소"
    else:
        url_base="https://openapi.naver.com/v1/search/local.json?query="
        keyword = quote("제주도 카페" + i["상호명"])
        url_middle="&display=5 & start=1"
        url = url_base + keyword + url_middle
        result = requests.get(url,headers = headers).json()
        if result["total"] == 0:
                df.loc[idx, "검색결과"] = "없는 장소"


# In[14]:


len(df)

# In[15]:


len(df[df["검색결과"]=="없는 장소"])

# In[16]:


df = df.drop(df[df["검색결과"]=="없는 장소"].index)
len(df)

# In[19]:


df.to_excel("final_pro/craw_상권.xlsx",index=False)

# In[55]:


etc1 = etc[:5000]
etc2 = etc[5000:]

# In[40]:


etc["상호명"][0].isnumeric()

# In[59]:


etc1= etc1.astype({"상호명" : "str"})

# In[60]:


etc1.info()

# In[62]:


import time 
for idx,i in etc1.iterrows():
    time.sleep(0.5)
    if len(i["상호명"]) > 2:
        if i["상호명"][:2] == "제주":
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote(i["상호명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                df.loc[idx, "검색결과"] = "없는 장소"
        else:
            url_base="https://openapi.naver.com/v1/search/local.json?query="
            keyword = quote("제주 " + i["상호명"])
            url_middle="&display=5 & start=1"
            url = url_base + keyword + url_middle
            result = requests.get(url,headers = headers).json()
            if result["total"] == 0:
                df.loc[idx, "검색결과"] = "없는 장소"
    else:
        url_base="https://openapi.naver.com/v1/search/local.json?query="
        keyword = quote("제주" + i["상호명"])
        url_middle="&display=5 & start=1"
        url = url_base + keyword + url_middle
        result = requests.get(url,headers = headers).json()
        if result["total"] == 0:
                df.loc[idx, "검색결과"] = "없는 장소"


# In[12]:


len(df[df["검색결과"]=="없는 장소"])

# In[ ]:


df.to_excel("final_pro/craw_상권.xlsx")

# In[ ]:


import os
def shutdown() :
    os.system("shutdown -s -t 0")

if __name__ == "__main__":
    shutdown()

# ### 1.프랜차이즈처리

# In[74]:


df["세분화분류"] = ""
df


# In[77]:


chicken = []
for idx,i in df.iterrows():
    if ("치킨" in str(i["상호명"])) or (i["표준산업분류명"] =="치킨 전문점"):
        chicken.append(idx)

# In[78]:


len(chicken)

# In[81]:


frenchise = ["BHC","와와","교촌","자담","호식이","본스","꾸바꾸바","본스","BBQ",
            "멕시칸","멕시카나","맘스","굽네","처갓집","땅땅","부어","오태식",
            "사바사바","네네","디케이","치킨플러스","60계","코코아찌","남문숯불",
            "더조은","티바","투존","페리카나","지코바","디디","순수","처가집",
            "썬더","푸라닭","후다닭","러브레터","팔일오","치킨더홈","컬투","치킨마루",
            "코리아","치킨과바람피자","치킨하우스","치킨쥼","치킨퐁","치킨의민족","치킨파티",
            "오성통닭","장군치킨","육십계","이서방양념","이서방치킨","이춘봉","오부장","와니피자치킨",
            "웰덤","꾸브라","꼴통치킨","구어스","가마솥치킨","꼴까닭치킨","네다모아피자","난피자넌치킨",
            "돈치킨","도연치킨","도연","더치킨","다사랑치킨","두리치킨","동근이숯불",
            "마미쿡","맛젤","만계","똥꼬치킨","명품치킨","범프리카","바른","베리웰",
            "바렌티나","못난감자앤치킨","스모프치킨","스머프치킨","수준이다른치킨","산들","신통치킨","또래오래","노랑통닭","가마로닭","멕시카나",
            "파닭에파무쳐"]

# 또래오래, 노랑통닭, 멕시카나, 푸라닭

for idx,i in df.iterrows():
    for j in chicken:
        if j == idx:
            for f in frenchise:
                if f in str(i["상호명"]):
                    df.loc[idx, "세분화분류"] = "프랜차이즈 치킨"
                    break
                else:
                    df.loc[idx,"세분화분류"] = "제주도만의 치킨"
        else:
            pass

# In[82]:


df[df["세분화분류"]=="제주도만의 치킨"]

# In[83]:


df[df["세분화분류"]=="프랜차이즈 치킨"]

# ### 2. ?

# In[ ]:




# ## 4. kakao map & kakao navi API

# ## 1. 카카오 맵

# In[17]:


import requests
import pandas as pd
import numpy as np
import folium
from folium.plugins import MiniMap

# In[22]:


def elec_location(region,page_num):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    params = {'query': region,'page': page_num}
    headers = {"Authorization": "KakaoAK "}

    places = requests.get(url, params=params, headers=headers).json()['documents']
    total = requests.get(url, params=params, headers=headers).json()['meta']['total_count']
    if total > 45:
        print(total,'개 중 45개 데이터밖에 가져오지 못했습니다!')
    else :
        print('모든 데이터를 가져왔습니다!')
    return places

# In[23]:


def elec_info(places):
    X = []
    Y = []
    stores = []
    road_address = []
    place_url = []
    ID = []
    for place in places:
        X.append(float(place['x']))
        Y.append(float(place['y']))
        stores.append(place['place_name'])
        road_address.append(place['road_address_name'])
        place_url.append(place['place_url'])
        ID.append(place['id'])

    ar = np.array([ID,stores, X, Y, road_address,place_url]).T
    df = pd.DataFrame(ar, columns = ['ID','stores', 'X', 'Y','road_address','place_url'])
    return df

# In[24]:


def keywords(location_name):
    df = None
    for loca in location:
        for page in range(1,4):
            local_name = elec_location(loca, page)
            local_elec_info = elec_info(local_name)

            if df is None:
                df = local_elec_info
            elif local_elec_info is None:
                continue
            else:
                df = pd.concat([df, local_elec_info],join='outer', ignore_index = True)
    return df

# In[25]:


def make_map(dfs):
    # 지도 생성하기
    m = folium.Map(location=[33.4935,126.6266],   # 기준좌표: 제주어딘가로 내가 대충 설정
                   zoom_start=12)

    # 미니맵 추가하기
    minimap = MiniMap() 
    m.add_child(minimap)

    # 마커 추가하기
    for i in range(len(dfs)):
        folium.Marker([df['Y'][i],df['X'][i]],
                  tooltip=dfs['stores'][i],
                  popup=dfs['place_url'][i],
                  ).add_to(m)
    return m

# In[26]:


location = ['성산일출봉 전기충전소']
df = keywords(location)
df = df.drop_duplicates(['ID'])
df = df.reset_index()

make_map(df)

# ## 2. 카카오 내비

# In[27]:


URL_base = "https://apis-navi.kakaomobility.com/v1/directions?"
origin = "origin=127.11015314141542,37.39472714688412&"
destination = "destination=127.10824367964793,37.401937080111644&"
waypoints = "waypoints=127.11341936045922,37.39639094915999&"
priority = "priority=RECOMMEND&"
car_type = "car_fuel=GASOLINE&car_hipass=True&summary=True"

URL = URL_base + origin + destination + waypoints + priority + car_type


headers = {"Authorization": "KakaoAK "}

# In[28]:


test = requests.get(URL,headers=headers).json()
test

# In[29]:


test["routes"][0]["summary"]["duration"]

# In[30]:


url2 = "https://apis-navi.kakaomobility.com/v1/directions?origin=127.11015314141542,37.39472714688412&destination=127.10824367964793,37.401937080111644&waypoints=&priority=RECOMMEND&car_fuel=GASOLINE&car_hipass=false&alternatives=false&road_details=false"

# In[34]:


all_re = requests.get(url2,headers=headers).json()
all_re

# In[33]:


all_re["routes"][0]["sections"][0]["roads"][1]["vertexes"]

# In[ ]:



