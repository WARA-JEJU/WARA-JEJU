#!/usr/bin/env python
# coding: utf-8

# # 컬럼명 변경 및 데이터 불러오기

# In[21]:


import pandas as pd
jeju = pd.read_csv("제주관광지_필터링.csv",encoding="utf-8")
jeju.tail()

# In[28]:


jeju.info()

# In[22]:


jeju.columns

# In[23]:


jeju.rename(columns = {'위치좌표 X축값 ' : 'x','위치좌표 Y축값 ' : "y"}, inplace = True)


# In[24]:


jeju.head()

# # 전처리

# ## 1. 좌표 값이 같고 이름이 다른 경우(중복 장소 제거)

# In[27]:




# ## 2. 관광/숙박 시설 나누기

# In[29]:


jeju_tour = jeju[jeju["구분"]=="관광/숙박"]
jeju_tour

# In[30]:


fileter = jeju_tour.query('장소명.str.contains("호텔|민박|모텔|여관|리조트|펜션|여인숙|별장|콘도|팬션|호스텔|무인텔|하우스") or 장소명.str.endswith("텔")', engine='python')
fileter


# In[31]:


for i in fileter.index:
    jeju_tour.drop(index = i,inplace=True)

# In[61]:


jeju_tour.info()

# # 크롤링

# ## 1.지역 크롤링 확인

# In[33]:


import requests
from urllib.parse import quote    
import pandas as pd

# In[34]:


client_id = ""
client_secret = ""

# In[35]:


headers = {"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}

# In[161]:


url_base="https://openapi.naver.com/v1/search/local.json?query="
keyword = quote(input("검색 키워드를 입력하세요. : "))
url_middle="&display=5 & start=1"

url = url_base + keyword + url_middle

result = requests.get(url,headers = headers).json()                  #결과값을 변수로 지정
result                                                           #결과값 출력

# In[162]:


result["total"]

# In[66]:


#jeju_tour_copy["검색결과"] = ""
#jeju_tour_copy.head()

# ## 2. 없어진 장소 처리

# In[68]:


import copy
test = copy.deepcopy(fileter)
test.info()

# In[148]:


test["검색결과"] = ""

# In[163]:


for idx,i in test.iterrows():

    if i["장소명"][:2] == "제주":
        url_base="https://openapi.naver.com/v1/search/local.json?query="
        keyword = quote(i["장소명"])
        url_middle="&display=5 & start=1"
        url = url_base + keyword + url_middle
        result = requests.get(url,headers = headers).json()
    else:
        url_base="https://openapi.naver.com/v1/search/local.json?query="
        keyword = quote("제주" + i["장소명"])
        url_middle="&display=5 & start=1"
        url = url_base + keyword + url_middle
        result = requests.get(url,headers = headers).json()
    try: 
        if result["total"] == 0:
            test.loc[idx, "검색결과"] = "없는 장소"
    except:
        print("Error : ", idx)

# In[157]:


test[test["검색결과"]=="없는 장소"]

# In[158]:


test[test["검색결과"]!="없는 장소"]

# In[ ]:



