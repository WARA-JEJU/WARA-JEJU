from pandas import read_csv
import pandas as pd
from selenium import webdriver
import time

jeju_range = read_csv("./제주특별자치도_음식_병합_case1_네이버_이미지_변환.csv", encoding="UTF-8")


# 크롬드라이버 크롤링 Start
def kakao_crawling():
    results = []
    for idx, i in jeju_range.iterrows():
        if i["place_url"] != '' and not pd.isna(i['place_url']):
            if (i["kakao_grade"] == '' or pd.isna(i['kakao_grade'])) and (i["kakao_review"] == '' or pd.isna(i['kakao_review'])):
                print("경로 = %s (%d건 진행중)" % (i['place_url'], idx))
                time.sleep(0.7)
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')        # Head-less 설정
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                driver = webdriver.Chrome('chromedriver', options=options)
                #driver = webdriver.Chrome("./chromedriver.exe")  # 크롬 드라이버 경로 지정
                url = i["place_url"]
                driver.implicitly_wait(4)
                driver.get(url)

                try:
                    grade = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b")
                except:
                    grade = '0'
                    i["kakao_grade"] = grade
                else:
                    kakao_grade = grade.text
                    i["kakao_grade"] = kakao_grade
                    print("평점 = %s (%d건 진행중)" % (kakao_grade, idx))

                try:
                    review = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(5) > span")
                except:
                    review = '0'
                    i["kakao_review"] = review
                    driver.quit()
                else:
                    kakao_review = review.text
                    i["kakao_review"] = kakao_review
                    print("리뷰 = %s (%d건 진행중)" % (kakao_review, idx))
                    driver.quit()
        results.append(i.copy())
    return pd.DataFrame(results).reset_index(drop=True)


jeju_range = kakao_crawling()
jeju_range.to_csv('./제주특별자치도_음식_병합_case1_네이버_이미지_변환_크롤링.csv', index=False)  # 구분자를 탭으로 하여 저장. 인덱스칼럼은 저장 안함.
# 크롬드라이버 크롤링 End
