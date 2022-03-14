#!/usr/bin/env python
# coding: utf-8

# ### - 카카오 API : 키워드 검색

# - 카카오 API 테스트 
#   - 앱 ID : 
#   - 네이티브 앱 키 : 
#   - REST API 키 : 
#   - JavaScript 키 : 
#   - Admin 키 : 
# - 키워드 검색
#   - 질의어를 통해 장소 검색 결과 반환
#   - category_group_name, category_name, place_url

# In[ ]:


import json
import requests
# REST 키
rest_api_key = ''
# 헤더
headers = {"Authorization" : "KakaoAK {}".format(rest_api_key)}
# 파라미터
params = {"query" : "제주도 맛집", "page" : 10}
url = "https://dapi.kakao.com/v2/local/search/keyword.json"

# GET을 이용하여 획득
res = requests.get(url, headers=headers, params=params)
# Json을 이용하여 해제
doc = json.loads(res.text)
# 200일 경우 정상
res.status_code

# In[ ]:


# 결과(Dict형으로 표현)
# documets : 각 검색 결과 정보
#  - address_name(String) : 전체 지번 주소
#  - category_group_code(String) : 중요 카테고리만 그룹핑한 카테고리 그룹 코드
#  - category_group_name(String) : 중요 카테고리만 그룹핑한 카테고리 그룹명
#  - category_name(String) : 카테고리 이름
#  - distance(String) : 중심좌표까지의 거리 (단, x,y 파라미터를 준 경우에만 존재), 단위 meter
#  - id(String) : 장소 ID
#  - phone(String) : 전화번호
#  - place_name(String) : 장소명, 업체명
#  - place_url(String) : 장소 상세페이지 URL
#  - road_address_name(String) : 전체 도로명 주소
#  - x(String) : X 좌표값, 경위도인 경우 longitude (경도)
#  - y(String) : Y 좌표값, 경위도인 경우 latitude(위도)
# meta : 검색 결과 메타 정보
doc

# ### - 네이버 API : 지역 검색

# - 네이버 API 테스트
#   - Client ID : 
#   - Client Secret : 
# - 지역 검색
#   - 질의어를 통해 장소 검색 결과 반환
#   - category, description 사용 가능

# In[44]:


import json
import urllib
import requests
# REST 키
client_key = 'xzjv8j9BbPlDkjv3L4cP'
client_secret = 'qXSjpcpeln'
# 헤더
headers = {"X-Naver-Client-Id" : client_key, 
           "X-Naver-Client-Secret" : client_secret}
# 파라미터
encText = urllib.parse.quote("제주 소리섬박물관")
url = "https://openapi.naver.com/v1/search/local.json?query="+encText

# GET을 이용하여 획득
res = requests.get(url, headers=headers)
# Json을 이용하여 해제
doc = json.loads(res.text)
# 200일 경우 정상
res.status_code

# In[45]:


# 결과(Dict형으로 표현)
# items : 각 검색 결과 정보
#  - title(String) : 업체, 기관명
#  - link(String) : 기관의 상세 정보가 제공되는 네이버 페이지의 하이퍼텍스트 link
#  - category(String) : 중요 카테고리만 그룹핑한 카테고리 그룹명
#  - description(String) : 기관명에 대한 설명을 제공
#  - telephone(String) : 하위 호환성을 위해 존재
#  - address(String) : 기관명의 주소를 제공
#  - roadAddress(String) : 기관명의 도로명 주소를 제공
#  - mapx(String) : x좌표를 제공한다. 제공값은 카텍좌표계 값으로 제공
#  - mapy(String) : y좌표를 제공한다. 제공값은 카텍 좌표계 값으로 제공
doc

# ### - 네이버 API : 이미지 검색

# - 네이버 API 테스트
#   - Client ID : 
#   - Client Secret : 
# - 지역 검색
#   - 질의어를 통해 이미지 검색 결과 반환
#   - image 링크 반환

# In[14]:


import json
import urllib
import requests
# REST 키
client_key = 'xzjv8j9BbPlDkjv3L4cP'
client_secret = 'qXSjpcpeln'
# 헤더
headers = {"X-Naver-Client-Id" : client_key, 
           "X-Naver-Client-Secret" : client_secret}
# 파라미터
encText = urllib.parse.quote("성산일출봉")
url = "https://openapi.naver.com/v1/search/image?query="+encText

# GET을 이용하여 획득
res = requests.get(url, headers=headers)
# Json을 이용하여 해제
doc = json.loads(res.text)
# 200일 경우 정상
res.status_code

# In[19]:


# 결과(Dict형으로 표현)
doc['items'][0]

# ### - 한국관광공사 LOD

# - Python에서 SPARQL을 사용하기 위해 `pip install sparqlwrapper`

# - 기본 정보

# #### 1. 한국관광공사 LOD 테스트

# In[91]:


from SPARQLWrapper import SPARQLWrapper, JSON

def getInfo():
    sparql = SPARQLWrapper("http://data.visitkorea.or.kr/sparql")
    prefix = """
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc: <http://purl.org/dc/elements/1.1/>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX vi: <http://www.saltlux.com/transformer/views#>
                PREFIX kto: <http://data.visitkorea.or.kr/ontology/>
                PREFIX ktop: <http://data.visitkorea.or.kr/property/>
                PREFIX ids: <http://data.visitkorea.or.kr/resource/>
                PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX geo: <http://www.saltlux.com/geo/property#>
                PREFIX pf: <http://www.saltlux.com/DARQ/property#> 
             """

    select_state = """
                    SELECT * 
                    WHERE {
                        ?resource a kto:Place ;
                            rdfs:label ?name ;
                            ktop:category ?category . 
                        ?category skos:prefLabel ?category_name . 
                        FILTER langMatches( lang(?category_name), "KO" ) 
                    } limit 10
                   """
    sparql.setQuery(prefix + select_state)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    for r in result['results']['bindings']:
        print(r['name']['value'], ':', r['category_name']['value'])
    # return result

# In[92]:


getInfo()

# #### 2. 한국관광공사 LOD : 이미지

# - 이미지 정보 : 대표 이미지(가장 첫 이미지)만 반환

# In[297]:


from SPARQLWrapper import SPARQLWrapper, JSON

def getImage(ids):
    sparql = SPARQLWrapper("http://data.visitkorea.or.kr/sparql")
    prefix = """
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc: <http://purl.org/dc/elements/1.1/>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX vi: <http://www.saltlux.com/transformer/views#>
                PREFIX kto: <http://data.visitkorea.or.kr/ontology/>
                PREFIX ktop: <http://data.visitkorea.or.kr/property/>
                PREFIX ids: <http://data.visitkorea.or.kr/resource/>
                PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX geo: <http://www.saltlux.com/geo/property#>
                PREFIX pf: <http://www.saltlux.com/DARQ/property#> 
             """

    select_state = """
                    SELECT *
                    WHERE {
                        ids:""" + str(ids) + """ a kto:Place ;
                            foaf:depiction ?depiction .
                        ?depiction foaf:depicts ?depicts ;
                            foaf:thumbnail ?thumbnail .
                    }
                   """
    sparql.setQuery(prefix + select_state)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    # 가장 첫 이미지 주소 반환
    try :
        return result['results']['bindings'][0]['depiction']['value']
    except:
        return ''

# In[298]:


getImage(125587)

# #### 3. 한국관광공사 LOD : 제주도 정보

# - 제주도 정보 : 1362개
#   - IDS
#   - 이름
#   - 카테고리
#   - 개요
#   - 타입
#   - 주소

# In[235]:


from SPARQLWrapper import SPARQLWrapper, JSON

def getJeju(ASC = True):
    sparql = SPARQLWrapper("http://data.visitkorea.or.kr/sparql")
    prefix = """
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc: <http://purl.org/dc/elements/1.1/>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX vi: <http://www.saltlux.com/transformer/views#>
                PREFIX kto: <http://data.visitkorea.or.kr/ontology/>
                PREFIX ktop: <http://data.visitkorea.or.kr/property/>
                PREFIX ids: <http://data.visitkorea.or.kr/resource/>
                PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX geo: <http://www.saltlux.com/geo/property#>
                PREFIX pf: <http://www.saltlux.com/DARQ/property#> 
             """

    # select_state = """
    #                 SELECT (COUNT(?name) AS ?CNT)
    #                 WHERE {
    #                     ?resource a kto:Place ;
    #                         rdfs:label ?name ;
    #                         ktop:address ?address .
    #                         FILTER (contains(?address, "제주") )
    #                 }
    #                """
    if ASC:
        select_state = """
                        SELECT *
                        WHERE {
                            ?resource a kto:Place ;
                                rdfs:label ?name ;
                                ktop:category ?category ;
                                dc:description ?description ;
                                ktop:address ?address .
                                FILTER (contains(?address, "제주"))
                            ?category rdfs:label ?category_name .
                            FILTER langMatches( lang(?category_name), "KO" )
                        }
                        ORDER BY ASC(?name)
                    """
    else:
        select_state = """
                        SELECT *
                        WHERE {
                            ?resource a kto:Place ;
                                rdfs:label ?name ;
                                ktop:category ?category ;
                                dc:description ?description ;
                                ktop:address ?address .
                                FILTER (contains(?address, "제주"))
                            ?category rdfs:label ?category_name .
                            FILTER langMatches( lang(?category_name), "KO" )
                        }
                        ORDER BY DESC(?name)
                    """
    sparql.setQuery(prefix + select_state)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    # for r in result['results']['bindings']:
    #     print(r['name']['value'], ':', r['category_name']['value'])
    return result

# - 테스트

# In[233]:


test = getJeju()

# - 내용 예시

# 'head': {'vars': ['resource', 'name', 'category', 'description', 'type', 'address', 'type_name', 'category_name']},  
# 'results': {'bindings': [{'resource': {'type': 'uri', 'value': 'http://data.visitkorea.or.kr/resource/130494'},  
# 'name': {'type': 'literal', 'xml:lang': 'ko', 'value': '이중섭 미술관'},  
# 'category': {'type': 'uri', 'value': 'http://data.visitkorea.or.kr/resource/A02060200'},  
# 'description': {'type': 'literal', 'xml:lang': 'ko', 'value': '※ 코로나바이러스감염증-19 공지사항 ※ 내용 : 사전예약제 (2020.06.18 ~ 별도안내시) → 코로나...'},  
# 'type': {'type': 'uri', 'value': 'http://data.visitkorea.or.kr/ontology/Attraction'},  
# 'address': {'type': 'literal', 'xml:lang': 'ko', 'value': '제주특별자치도 서귀포시 이중섭로 27-3'},  
# 'type_name': {'type': 'literal', 'xml:lang': 'ko', 'value': '명소'},  
# 'category_name': {'type': 'literal', 'xml:lang': 'ko', 'value': '기념관'}}  

# - 첫 인덱스 값 확인

# In[198]:


test0 = test['results']['bindings'][0]

# In[199]:


test0['resource']['value'].split('/')[-1], test0['name']['value'], test0['category_name']['value'], test0['description']['value'][:50], test0['address']['value']

# #### 4. 한국관광공사 LOD : 제주도 정보 => DF화

# - df 추출 함수 정의

# In[305]:


import pandas as pd

def getJeju_df():
    ids = []
    name = []
    category_name = []
    description = []
    address = []
    img = []
    # 1000개 씩 결과를 가져오기 때문에 오름차순, 내림차순으로 정렬하여 확인
    jeju = getJeju(True)
    for value in jeju['results']['bindings']:
        ids.append(value['resource']['value'].split('/')[-1])
        name.append(value['name']['value'])
        category_name.append(value['category_name']['value'])
        description.append(value['description']['value'])
        address.append(value['address']['value'])
    last_ids = ids[-1]

    jeju = getJeju(False)
    for value in jeju['results']['bindings']:
        if value['resource']['value'].split('/')[-1] == last_ids:
            break
        ids.append(value['resource']['value'].split('/')[-1])
        name.append(value['name']['value'])
        category_name.append(value['category_name']['value'])
        description.append(value['description']['value'])
        address.append(value['address']['value'])
    
    for i in ids:
        img.append(getImage(i))

    jeju_df = pd.DataFrame({
        'ids' : ids,
        'name' : name,
        'category' : category_name,
        'description' : description,
        'address' : address,
        'img' : img,
    })

    return jeju_df

# In[ ]:


test_df = getJeju_df()

# - type 컬럼 추가

# In[ ]:


from SPARQLWrapper import SPARQLWrapper, JSON
def getType(ids):
    type_list = []

    sparql = SPARQLWrapper("http://data.visitkorea.or.kr/sparql")
    prefix = """
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc: <http://purl.org/dc/elements/1.1/>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX vi: <http://www.saltlux.com/transformer/views#>
                PREFIX kto: <http://data.visitkorea.or.kr/ontology/>
                PREFIX ktop: <http://data.visitkorea.or.kr/property/>
                PREFIX ids: <http://data.visitkorea.or.kr/resource/>
                PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX geo: <http://www.saltlux.com/geo/property#>
                PREFIX pf: <http://www.saltlux.com/DARQ/property#> 
             """

    select_state = """
                    SELECT * 
                    WHERE {
                        ids:"""+str(ids)+""" a kto:Place ;
                            rdf:type ?type .
                        ?type rdfs:label ?type_name .
                        FILTER langMatches( lang(?type_name), "KO" ) 
                    }
                   """
    sparql.setQuery(prefix + select_state)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    for r in result['results']['bindings']:
        type_list.append(r['type_name']['value'])
    
    return type_list

# In[309]:


test_df['type'] = ''
for idx, row in test_df.iterrows():
    type_list = getType(row['ids'])

    test_df.loc[idx, 'type'] = ','.join(type_list)  

# In[311]:


test_df.info()

# - 주소가 제주도인 경우 모두 DataFrame로 추출 : 총 1358개
# - 이미지가 없는 경우 459개, 있는 경우 899개

# In[324]:


(test_df['img'] != '').value_counts()

# - 데이터 저장

# In[325]:


# test_df.to_excel('./data/220110/한국관광공사_LOD_제주도.xlsx')

# ### - 관광 / 숙박 분리

# - 관광 / 숙박은 카테고리상 차이가 나기 때문에 분리해주도록 한다.

# #### 1. 데이터 확인

# - 필터링1 버전으로 실행
# - 필터링2는 레저/스포츠 부분만 전처리를 진행하였기 때문에 관광/숙박 시설은 필터링1과 동일

# In[ ]:


import pandas as pd

df = pd.read_excel('./data/제주도 장소(POI) - 필터링1.xlsx')
df.head()

# In[ ]:


df.info()

# - 구분 컬럼으로 카운트 확인

# In[ ]:


df['구분'].unique()

# In[ ]:


df['구분'].value_counts()

# #### 2. 관광 / 숙박 : 숙박 시설 확인

# - 관광/숙박 컬럼 선택

# In[ ]:


# all = df.query('구분 == "관광/숙박"')
all = df[df['구분'] == '관광/숙박']
all.head()

# In[ ]:


all.info()

# - 숙박 시설 확인
#   - '호텔', '민박', '모텔', '여관', '리조트', '펜션', '여인숙', '별장', '팬션', '콘도', '호스텔', '하우스'
#   - '--텔'로 끝나는 경우
#   - 2480개

# In[ ]:


accommodations = ['호텔', '민박', '모텔', '여관', '리조트', '펜션', '여인숙', '별장', '팬션', '콘도', '호스텔', '하우스']

accommodation_df = all.query(f'장소명.str.contains("{"|".join(accommodations)}") or 장소명.str.endswith("텔")', engine='python').copy()

# - 숙박 시설 DataFrame

# In[ ]:


accommodation_df.info()

# In[ ]:


len(accommodation_df['장소명'].unique())

# In[ ]:


# accommodation_df.to_excel('./accomodation.xlsx')

# #### 3. 관광 / 숙박 : 관광 시설 확인

# - 숙박 시설의 인덱스를 제거하여 관광 시설 판별

# In[ ]:


tourism_df = all.drop(accommodation_df.index, axis=0).copy()
tourism_df.info()

# In[ ]:


len(tourism_df['장소명'].unique())

# In[ ]:


# tourism_df.to_excel('tourism.xlsx')

# #### 4. 관광 / 숙박 : 관광 시설 추가 관찰

# - 엑셀을 이용해 직접 확인

# ### - 중복 좌표 처리

# #### 1. 데이터 확인

# - 필터링2 버전으로 실행
# - 같은 좌표가 2개 이상인 경우만 추가하여 확인

# In[1]:


import pandas as pd

df = pd.read_excel('./data/제주도 장소(POI) - 필터링2.xlsx')
df.head()

# In[2]:


df.info()

# In[3]:


df.columns

# In[4]:


include_index = []      # 탐색한 좌표
duplicate_index = []    # 중복 좌표

for idx, row in df.iterrows():
    # 중복 좌표가 아닌 경우 탐색
    if idx not in include_index:
        # 중복 좌표의 인덱스 확인
        temp = list(df[((df['위치좌표 X축값 '] == row['위치좌표 X축값 ']) & (df['위치좌표 Y축값 '] == row['위치좌표 Y축값 ']))].index)
        # 길이가 2 이상인 경우 : 중복 좌표가 존재함을 의미
        if len(temp) >=2 :
            include_index.extend(temp)
            duplicate_index.append(temp)
        # 길이가 1인 경우 : 중복 좌표가 존재하지 않음을 의미
        else:
            include_index.append(idx)

# - 전체 인덱스 개수

# In[5]:


len(include_index)

# - 중복 좌표 개수

# In[6]:


len(duplicate_index)

# #### 2. 중복 좌표 삭제

# In[7]:


total = 0
names = {}
for idx, index_list in enumerate(duplicate_index, start=1):
    total += len(index_list)    # 중복 좌표의 개수 확인
    names[index_list[0]] = []   # 중복 좌표의 다른 이름 추가
    for idx2, index in enumerate(index_list):
        if idx2 != 0:
            # 다른 이름 추가
            names[index_list[0]].append(df.loc[index, '장소명'])
            # 행 삭제
            df.drop(index, axis=0, inplace=True)

# - 전체 중복 좌표 수

# In[8]:


total

# - 삭제한 행의 수

# In[9]:


total - len(duplicate_index)

# - 중복 컬럼 삭제 후 정보

# In[10]:


df.info()

# In[11]:


df['구분'].value_counts()

# In[12]:


# 추가 이름 컬럼 생성
# 중복 좌표의 '이름' 추가, 없을 경우 '.'으로 표현
df['Additional_Name'] = '.'
for idx, value in names.items():
    df.loc[idx, 'Additional_Name'] = ','.join(value)

# In[13]:


df.head()

# - 중복 좌표 삭제

# In[ ]:


# df.to_excel('./data/제주도 장소(POI) - 필터링3.xlsx')

# ### - 데이터 분리(구분)

# - 필터링3 활용
# - 구분 컬럼별로 데이터를 분리하여 저장

# In[13]:


import pandas as pd

df_poi = pd.read_excel("./data/제주도 장소(POI) - 필터링3.xlsx", index_col=0)
df_poi.head(2)

# In[24]:


df_poi['구분'].unique()

# In[26]:


df_poi['구분'].unique()
for kind in df_poi['구분'].unique():
    df_poi[df_poi['구분'] == kind].to_excel('''./data/220110/POI_{}.xlsx'''.format(kind.replace('/', '_')))

# ### - 데이터 확인

# #### 1. 각 엑셀 데이터 확인

# - 장소 정보1

# In[21]:


import pandas as pd

park_df = pd.read_excel('./data/220110/네이버 API 결과 추가/공원_장소처리.xlsx')
tour_df = pd.read_excel('./data/220110/네이버 API 결과 추가/관광지_장소처리.xlsx')
culture_df = pd.read_excel('./data/220110/네이버 API 결과 추가/문화예술_장소처리.xlsx')
accom_df = pd.read_excel('./data/220110/네이버 API 결과 추가/숙박_장소처리.xlsx')
leisure_df = pd.read_excel('./data/220110/네이버 API 결과 추가/레저_스포츠_장소처리.xlsx')

# In[24]:


print(park_df.shape, tour_df.shape, culture_df.shape, accom_df.shape, leisure_df.shape)
print(sum([park_df.shape[0], tour_df.shape[0], culture_df.shape[0], accom_df.shape[0], leisure_df.shape[0]]))

# #### 2. 각 POI 정보 결합

# - 장소 정보2
#   - 각 엑셀 데이터 결합

# In[29]:


import pandas as pd

poi_df = pd.read_excel('./data/220111/POI_장소처리.xlsx')
poi_df.info()

# #### 3. 식당 데이터

# - 식당 정보

# In[27]:


restaurant_df = pd.read_excel('./data/식당/제주도 식당 정보_전체.xlsx')
restaurant_df.shape

# In[28]:


restaurant_df.columns

# ### - 레져/스포츠 필요없는 데이터 삭제

# #### 1. 필요없는 장소 삭제

# - ['헬스', '휘트니스', '리조트', '연수원', '당구', '탁구', '볼링', '수련', '체육', '교육원', '테니스', '대피소', '주차장', '매표소', '요가', '게이트볼', '유도', '학교', '수양', '훈련', '휴게소', '사무소', '악지소'] 데이터 삭제

# In[30]:


import pandas as pd

poi_df = pd.read_excel('./data/220111/POI_장소처리.xlsx')

# In[40]:


poi_df.info()

# In[31]:


poi_df['구분'].unique()

# In[39]:


leisure = ['헬스', '휘트니스', '리조트', '연수원', '당구', '탁구', '볼링', '수련', '체육', '교육원', '테니스', '대피소', '주차장', '매표소', '요가', '게이트볼', '유도', '학교', '수양', '훈련', '휴게소', '사무소', '악지소']
leisure_df = poi_df.query('구분 == "레져/스포츠"')
drop_index = leisure_df.query(f'장소명.str.contains("{"|".join(leisure)}")', engine='python').index
len(drop_index)

# In[41]:


poi_df.drop(drop_index, axis=0, inplace=True)
poi_df.reset_index(drop=True, inplace=True)

# In[42]:


poi_df.info()

# In[43]:


# poi_df.to_excel('./data/220111/POI_장소처리2.xlsx', index=False)

# #### 2. 중복 장소 삭제

# - 엑셀을 통해 직접 눈으로 보며 같은 장소이면서 좌표가 다른 경우 삭제

# In[45]:


import pandas as pd

poi_df3 = pd.read_excel('./data/220111/POI_장소처리3.xlsx')

# In[46]:


poi_df3.info()

# ### - 필요없는 데이터 삭제

# - 문화/종교/예술, 공원/산/동.식물원, 숙박, 관광지 데이터 중 필요없는 데이터 삭제
#   - 같은 장소이지만 경도, 위도가 다른 경우
#   - 관광지가 아닌 경우 (ex) 놀이터(어린이 공원), 동네 운동장 등

# ### - ㅇ
