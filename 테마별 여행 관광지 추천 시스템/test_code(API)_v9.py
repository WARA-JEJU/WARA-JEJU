#!/usr/bin/env python
# coding: utf-8

# ### - POI 데이터 : 잘못된 이미지 삭제

# In[ ]:


import pandas as pd

jeju_poi = pd.read_excel('./data/220118/_제주도_POI_have_image.xlsx', index_col=0)

# In[ ]:


jeju_poi.head(1)

# #### 1. 사용할 이미지 확인

# - 로고, 장소와 다른 이미지를 삭제하고 남은 이미지 확인
#   - 파일명 : (idx)_(plac ename).jpg
# - .jpg를 삭제하고 '_'를 기준으로 split

# In[ ]:


import os

path = './data/220118/_제주도_POI_IMAGE/'
use_idx = []
for dir_name in os.listdir(path):
    print(dir_name)
    for image in os.listdir(path + dir_name):
        image = image.replace('.jpg', '')
        idx, p_name = image.split('_')
        use_idx.append(int(idx))

# In[ ]:


use_idx[:10], len(use_idx)

# #### 2. 남은 이미지만 사용

# - use_idx를 이용하여 해당하는 인덱스만 사용

# In[ ]:


use_idx.sort()

# In[ ]:


jeju_use = jeju_poi.loc[use_idx, :].copy()

# In[ ]:


jeju_use.info()

# In[ ]:


jeju_use.head(1)

# #### 3. 데이터 저장

# In[ ]:


# jeju_use.to_excel('./data/220118/_제주도_POI_final_use.xlsx')

# ##### ◽ㅇ

# ### - 이미지 RESIZE

# - 이미지의 크기가 다르기 때문에 동일한 크기로 조절
#   - 현재 : (256, 256)

# #### 1. 이미지 Path 확인

# - 폴더별로 이미지가 나누어져 있으므로 폴더를 key 값으로 dict형 구성

# In[ ]:


import os

path = './data/220118/_제주도_POI_IMAGE/'
image_path = {'관광명소' : [], '음식점' : [], '카페' : []}
for dir_name in os.listdir(path):
    print(dir_name)
    for image in os.listdir(path + dir_name):
        image_path[dir_name].append(path + dir_name + '/' + image)

# In[ ]:


image_path['관광명소'][:2], image_path['음식점'][:2], image_path['카페'][:2]

# #### 2. 이미지 Resize

# ##### ◽PIL 사용

# - jpg의 경우 중간에 오류가 발생하여 png로 변경

# In[ ]:


from PIL import Image

home = 'C:/Users/Isanghada/Desktop/테스트/'
for kind in image_path.keys():
    for image in image_path[kind]:    
        name = image.split('/')[-1]
        img = Image.open(image)
        img.resize((256, 256)).save(home+kind+'/'+name[:-3]+'png', 'png')
