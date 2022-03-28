from pandas import read_csv
import pandas as pd
from selenium import webdriver
import time

jeju_range = read_csv("./제주특별자치도_지리_병합_네이버_변환.csv", encoding="UTF-8")
jeju_range["kakao_grade"] = ''
jeju_range["kakao_review"] = ''
jeju_range["kakao_img"] = ''


# 크롬드라이버 크롤링 Start
def kakao_crawling():
    results = []
    for idx, i in jeju_range.iterrows():
        if i["place_url"] != '' and not pd.isna(i['place_url']):
            print("경로 = %s (%d건 진행중)" % (i['place_url'], idx))
            time.sleep(0.7)
            driver = webdriver.Chrome("./chromedriver.exe")  # 크롬 드라이버 경로 지정
            url = i["place_url"]
            driver.implicitly_wait(8)
            driver.get(url)

            try:
                grade = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b")
            except:
                grade = ''
                i["kakao_grade"] = grade
            else:
                kakao_grade = grade.text
                i["kakao_grade"] = kakao_grade
                print("평점 = %s (%d건 진행중)" % (kakao_grade, idx))

            try:
                review = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(5) > span")
            except:
                review = ''
                i["kakao_review"] = review
            else:
                kakao_review = review.text
                i["kakao_review"] = kakao_review
                print("평점 = %s (%d건 진행중)" % (kakao_review, idx))
                
            try:
                image = driver.find_element_by_css_selector("#mArticle > div.cont_photo.no_category > div.photo_area > ul > li.size_l > a")
                print("이미지 = %s (%d건 진행중)" % (image, idx))
            except:
                kakao_img = ''
                i["kakao_img"] = kakao_img
                driver.quit()
            else:
                image = image.get_attribute("style")[23:-3]
                kakao_img = "https:" + image
                i["kakao_img"] = kakao_img
                driver.quit()
                
        results.append(i.copy())
    return pd.DataFrame(results).reset_index(drop=True)


jeju_range = kakao_crawling()
jeju_range.to_csv('./제주특별자치도_지리_병합_네이버_변환_크롤링.csv', index=False)  # 구분자를 탭으로 하여 저장. 인덱스칼럼은 저장 안함.
# 크롬드라이버 크롤링 End
