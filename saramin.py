# -*- coding: utf-8 -*-
"""Untitled10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/116q5JrprxSUrjxdL7Hsj3pq6H0llgiK9
"""

from IPython.utils.text import dedent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

import pandas as pd

service = Service(executable_path=r'/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
options.add_argument(f"user-agent={headers['User-Agent']}")
driver = webdriver.Chrome(service=service, options=options)

# 페이지 수 설정
total_pages = 1

# 데이터를 저장할 빈 리스트 생성
data = []

base_url = "https://www.saramin.co.kr"

for page in range(1, total_pages + 1):
    # 웹 페이지 URL 설정
    url = f"https://www.saramin.co.kr/zf_user/search?cat_mcls=2&exp_cd=1&job_type=1%2C4&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y&recruitPage={page}&recruitSort=relation&recruitPageCount=40&inner_com_type=&searchword=&show_applied=&quick_apply=&except_read=&ai_head_hunting=&mainSearch=n"

    # 웹 페이지에 접속
    driver.get(url)

    # 페이지 HTML 가져오기
    html = driver.page_source

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html, "html.parser")

    div_recruit = driver.find_element(By.ID, "recruit_info_list")

    name = div_recruit.find_elements(By.CLASS_NAME,"corp_name")
    tit = div_recruit.find_elements(By.CLASS_NAME, "job_tit")
    date = div_recruit.find_elements(By.CLASS_NAME, "date")
    href = div_recruit.find_elements(By.XPATH, "//a[@class='data_layer']")

    list_name = [item.text.strip() for item in name]
    list_tit = [item.text.strip() for item in tit]
    list_date = [item.text.strip() for item in date]
    list_href = [item.get_attribute("href") for item in href]
    list_logo = []
    list_dt = []
    list_dd = []
    dic_info = {
       "기업형태": [], "사원수": [],  "업종": [],
       "설립일": [],  "매출액": [], "대표자명": [],
       "홈페이지": [], "기업주소": []
    }

    for link in list_href:
       driver.get(link)
       driver.implicitly_wait(time_to_wait=10)
       xpath_cont = driver.find_element(By.XPATH, "//*[@id='content']/div[3]/section[1]/div[1]")
       div_company = xpath_cont.find_element(By.CLASS_NAME, "company")
       # logo 가져오기
       try:
          div_logo = xpath_cont.find_element(By.CLASS_NAME, "logo")
          img_logo = div_logo.find_element(By.CSS_SELECTOR, "img")
          list_logo.append(img_logo.get_attribute('src'))
          print("logo:")
          print(img_logo.get_attribute('id'))
       except NoSuchElementException:
          list_logo.append("NULL")
       print(link)
       print("=====")
       print(div_company.text)
       print("*****")
       try:
          div_tit = xpath_cont.find_element(By.CLASS_NAME, "title")
          div_info = xpath_cont.find_element(By.XPATH, "//div[@class='info']")
          dl_elements = div_info.find_elements(By.CSS_SELECTOR, "dl")
          for dl_element in dl_elements:
             dt = dl_element.find_element(By.CSS_SELECTOR, "dt")
             dd = dl_element.find_element(By.CSS_SELECTOR, "dd")
             key = dt.text.replace("*","")
             value = dd.text.strip()
             dic_info[key].append(value)
          print(div_tit.text)
          print(div_info.text)
          print("///")
          print(dic_info)
          print("////")
       except NoSuchElementException:
          print("NULL!!!")
       print("\n-----\n")
       """try:
          xpath_element = driver.find_element(By.CLASS_NAME, "address")
          extracted_data = xpath_element.text.strip()
          list_adr.append(extracted_data)
       except NoSuchElementException:
          print("요소를 찾을 수 없음")
          list_adr.append("")

       try:
          div_element = driver.find_elements(By.CLASS_NAME, "logo")
          for logo_element in div_element:
             img_element = logo_element.find_element(By.TAG_NAME, 'img')
             img = img_element.get_attribute('src')
             print(img)
             list_img.append(img)
       except NoSuchElementException:
          print("요소를 찾을 수 없음")"""

    for corp_name, corp_tit, corp_date, corp_href, corp_logo in zip(list_name, list_tit, list_date, list_href, list_logo):
        data.append({
            "회사명": corp_name,
            "채용공고": corp_tit,
            "마감일": corp_date,
            "href": corp_href,
            "logo": corp_logo
        })

# 웹 드라이버 종료
driver.quit()

# 데이터를 CSV 파일로 저장
df = pd.DataFrame(data, columns=["채용공고", "회사명", "마감일", "href", "logo"])
df.to_csv("it개발, 데이터.csv", index=False, encoding="utf-8-sig")

print(f"{total_pages} 페이지에서 데이터를 성공적으로 CSV 파일로 저장했습니다.")