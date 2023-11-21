# 최종본

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs  # 스크래핑을 패키지
import time
import datetime
from tqdm import trange

# 스크래핑할 웹 사이트의 url을 선언, f-string을 이용해 page number를 바꾸어가며 탐색할 수 있도록 함.
page_no = 1
url = f"https://www.jobkorea.co.kr/Search/?duty=1000229%2C1000230%2C1000231%2C1000232%2C1000233%2C1000234%2C1000235%2C1000236%2C1000237%2C1000238%2C1000239%2C1000240%2C1000241%2C1000242%2C1000243%2C1000244%2C1000245%2C1000246%2C1000247&jobtype=1%2C3&tabType=recruit&Page_No={page_no}"

# DataFrame 선언 첫번째 열에 
df = pd.DataFrame( columns = ['회사명','공고명','채용 형태(경력, 신입)','직장 위치','키워드','마감 기한','공고 링크'])

# 스크래핑할 페이지 요청
response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
#파싱
soup = bs(response.text,'html.parser')


# 스크래핑할 웹 사이트의 총 페이지 수 파악
# 잡코리아 검색결과의 '총 OOOO건' 이라는 검색 결과를 스크래핑하여 한 페이지당 표시 수인 20으로 나누기
pages = soup.find('p','filter-text').find('strong').text.replace(',','')
pages = round(int(pages)/20)

# For문을 이용해 웹 사이트 탐색
# 바깥의 for문을 통해 페이지를 바꾸어가며 탐색하고
# 안쪽의 for문으로 페이지 내 20개의 공고를 옮겨가며 탐색한다.

for i in trange(20):    # for i in trange(pages): 를 통해 전체 페이지 탐색 가능. 시간이 오래걸려 일단 20페이지만 탐색

    # 스크래핑을 위한 url을 재설정 page_no이 증가함에 따라 다음 페이지로 넘어가 크롤링을 진행한다. 
    url = f"https://www.jobkorea.co.kr/Search/?duty=1000229%2C1000230%2C1000231%2C1000232%2C1000233%2C1000234%2C1000235%2C1000236%2C1000237%2C1000238%2C1000239%2C1000240%2C1000241%2C1000242%2C1000243%2C1000244%2C1000245%2C1000246%2C1000247&careerType=1&jobtype=1%2C3&tabType=recruit&Page_No={page_no}"

    # url 재설정 후 스크래핑하기 위한 페이지 요청 
    response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
    soup = bs(response.text,'html.parser')
    
    # 태그와 클래스를 통해서 find_all을 통해서 페이지에서 태그에 맞는 모든 텍스트 정보들을 list로 가져온다.
    exp = soup.find_all('span','exp') # 채용 형태
   # edu = soup.find_all('span','edu') # 학력
    loc = soup.find_all('span','loc long') #회사 위치
    date = soup.find_all('span','date') # 마감 기한
    company_name = soup.find_all('a','name dev_view') # 회사 이름
    info = soup.find_all('a','title dev_view') # 공고명
    etc = soup.find_all('p','etc') # 기타 정보(키워드를 위한)
    
    # find_all로 가져온 이번 페이지에서 얻은 20개의 기업 공고를 csv로 만들기 위한 과정
    for j in trange(20):
        print(f"Processing index {j}")
        print(f"Company Name length: {len(company_name)}, Info length: {len(info)}, etc length: {len(etc)}")

        # 키워드를 20개까지 보여준다
        keywords = ''
        if j < len(etc):
            keywords = ','.join(etc[j].text.split(',')[:20])

        df.loc[20*i + j] = [
            company_name[j].text,       # 회사 이름
            info[j].text.strip(),       # 공고명
            exp[j].text,                # 채용 형태(경력, 신입)
          #  edu[j].text,                # 학력
            loc[j].text,                # 회사 위치
            keywords,                   # 키워드
            date[j].text,               # 마감 기한
            "https://www.jobkorea.co.kr/" + info[j]['href']  # 공고 링크
        ]

    page_no += 1
    
    time.sleep(0.1)

file_name = str(datetime.date.today()) + "_it 신입 인턴 개발자_채용공고.csv"
df.to_csv(file_name,index=False)
pd.read_csv(file_name)