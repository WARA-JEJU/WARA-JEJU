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

# In[10]:


import requests
from urllib.parse import quote    
import pandas as pd

# In[11]:


client_id = ""
client_secret = ""

# In[13]:


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

# In[130]:


jeju_accom.to_excel("숙박_장소처리.xlsx")


# In[131]:


jeju_tour.to_excel("관광지_장소처리.xlsx")

# In[134]:


park.to_excel("공원_장소처리.xlsx")

# In[135]:


leisure.to_excel("레저_스포츠_장소처리.xlsx")

# In[136]:


culture.to_excel("문화예술_장소처리.xlsx")

# ## 3. 이미지 크롤링

# In[44]:


url_base="https://openapi.naver.com/v1/search/image?query="
keyword = quote("서귀포호텔	")
url_middle="&display=5&start=1&sort=sim"

url = url_base + keyword + url_middle

result = requests.get(url,headers = headers).json()
result

# In[ ]:




# In[ ]:




# In[ ]:



