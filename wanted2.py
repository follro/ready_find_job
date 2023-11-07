# 최종본

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs   
import time
import datetime
from tqdm import trange

# 스크래핑할 웹 사이트의 url을 선언, f-string을 이용해 page number를 바꾸어가며 탐색할 수 있도록 함.
page_no = 1
url = f"https://www.jobkorea.co.kr/Search/?duty=1000229%2C1000230%2C1000231%2C1000232%2C1000233%2C1000234%2C1000235%2C1000236%2C1000237%2C1000238%2C1000239%2C1000240%2C1000241%2C1000242%2C1000243%2C1000244%2C1000245%2C1000246%2C1000247&jobtype=1%2C3&tabType=recruit&Page_No={page_no}"

# DataFrame 선언
df = pd.DataFrame( columns = ['회사로고'])

# 스크래핑할 웹 사이트의 총 페이지 수 파악
# '총 OOOO건' 이라는 검색 결과를 스크래핑하여 한 페이지당 표시 수인 20으로 나누기

response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
soup = bs(response.text,'html.parser')

pages = soup.find('p','filter-text').find('strong').text.replace(',','')
pages = round(int(pages)/20)

# For문을 이용해 웹 사이트 탐색
# 바깥의 for문을 통해 페이지를 바꾸어가며 탐색하고
# 안쪽의 for문으로 페이지 내 20개의 공고를 옮겨가며 탐색한다.

for i in trange(20):                       # for i in trange(pages): 를 통해 전체 페이지 탐색 가능. 시간이 오래걸려 일단 20페이지만 탐색

    url = f"https://www.jobkorea.co.kr/Search/?duty=1000229%2C1000230%2C1000231%2C1000232%2C1000233%2C1000234%2C1000235%2C1000236%2C1000237%2C1000238%2C1000239%2C1000240%2C1000241%2C1000242%2C1000243%2C1000244%2C1000245%2C1000246%2C1000247&careerType=1&jobtype=1%2C3&tabType=recruit&Page_No={page_no}"

    response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
    soup = bs(response.text,'html.parser')
    
    info = soup.find_all('a','title dev_view')
    

    j = 0  # 초기 인덱스
    while j < 20:
        print(f"인덱스 {j}를 처리 중")

        url2 = f"https://www.jobkorea.co.kr/" + info[j]['href']
        response = requests.get(url2, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}, timeout=(10, 30))
        soup2 = bs(response.text, 'html.parser')

        company_logo = soup2.find_all('img', {'id': 'cologo'})
        

        if company_logo:
            df.loc[20 * page_no + j] = [company_logo[0]['src']]
            print(company_logo[0]['src'])
        else:
            df.loc[20 * page_no + j] = ['none']
            print('로고가 없습니다.')
        
        # 매 10번째 반복마다 사용자 입력 받기
        if (j + 1) % 10 == 0 :
            user_input = input(f"{j + 1}번 항목에서 계속 진행하려면 'gg'를 입력하세요. 10번 전으로 돌아가려면 'ss'를 입력하세요: ")
            if user_input == 'gg':
                pass  # 계속 진행
            elif user_input == 'ss':
                j -= 10  # 10번 전으로 돌아감

        j += 1  # 다음 인덱스로 이동


       



    page_no += 1
    
    time.sleep(0.1)

file_name = str(datetime.date.today()) + "_it 신입 인턴 개발자_채용공고new2.csv"
df.to_csv(file_name,index=False)
pd.read_csv(file_name)