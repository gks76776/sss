from selenium import webdriver as wd
from urllib.request import urlopen
import time
from selenium.webdriver.common.by import By
# WebDriverWait는 Selenium 2.4.0 이후 부터 사용 가능합니다.
from selenium.webdriver.support.ui import WebDriverWait
# expected_conditions는 Selenium 2.26.0 이후 부터 사용 가능합니다.
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm_notebook
from datetime import datetime as dt
import datetime
import pandas as pd
class naver_crawler():
    def __init__(self,stock_code,deadline_date):
        self.stock_code = stock_code
        self.deadline_date = deadline_date        
        self.collected_date = set()
        

    def click_next_title():
        # 다음 글로 넘어 가기 위한 제목 목록 
        tr = driver.find_elements_by_css_selector('#content > div.section.inner_sub > div:nth-child(5) > table > tbody > tr ')       
        for idx, element in enumerate(tr):
            # 첫번째는 빈칸이다.
            if idx==0:
                continue        
            try:
                #현재 글의 위치를 찾기 위해 strong을 검색
                td = element.find_elements_by_css_selector('td')[1].find_element_by_css_selector('strong')            
            except Exception as e:            
                continue
            else:           
                driver.find_element_by_css_selector('#content > div.section.inner_sub > div:nth-child(5) > table > tbody > tr:nth-child({0}) > td:nth-child(2) > a'.format(2+idx)).click()
                break

    def minus_days(days):        
        return str(dt.now - datetime.timedelta(days=1))

    def save_csv(idx, jungbo, stock_code):
        if idx % 100== 0:         
            frame = pd.DataFrame(jungbo)
            with open('./naver_{0}.csv'.format(stock_code), 'a',encoding='utf-8') as f:
                frame.to_csv(f, header=False, encoding='utf-8')            
            jungbo.clear()

    def collecting(input_date,collected_date,stock_code):
        stime = time.time()
        idx = 0
        while True:
        # 게시글에 제목, 작성일, 조회수, 공감수, 비공감수. 내용을 크롤링
            date = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#content > div.section.inner_sub > table.view > tbody > tr:nth-child(2) > th.gray03.p9.tah')))
            #date        = driver.find_element_by_css_selector('#content > div.section.inner_sub > table.view > tbody > tr:nth-child(2) > th.gray03.p9.tah')
            if (dt.strptime(date.text.split(' ')[0],"%Y.%m.%d").date() - dt.strptime(self.deadline_date,"%Y.%m.%d").date()).days < 0 :
                break
            title = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#content > div.section.inner_sub > table.view > tbody > tr:nth-child(1) > th:nth-child(1) > strong')))
            # title       = driver.find_element_by_css_selector('#content > div.section.inner_sub > table.view > tbody > tr:nth-child(1) > th:nth-child(1) > strong')
            self.collected_date.add(date.text.split(' ')[0])
            #print(date.text.split(' ')[0],len(date.text.split(' ')[0]))
            # 작성자
            # writer = driver.find_element_by_css_selector('#content > div.section.inner_sub > table.view > tbody > tr:nth-child(2) > th.info > span.gray03 > strong')
            # 작성자 ip
            writer_chunck = driver.find_element_by_css_selector('#content > div.section.inner_sub > table.view > tbody > tr:nth-child(2) > th.info > span.gray03 ').text
            writer = writer_chunck.split(' ')[0]
            writer_ip = writer_chunck.split(' ')[1]
            # name 은 정보를 가진 덩어리 - 
            name        = driver.find_element_by_css_selector('#content > div.section.inner_sub > table.view > tbody > tr:nth-child(1) > th:nth-child(2)')
            views       = name.find_element_by_tag_name('span')
            Sympathy    = name.find_elements_by_tag_name('strong')
            text = driver.find_element_by_css_selector('#body')
            reply_list = []
            mord = [date.text, views.text,writer,writer_ip,Sympathy[0].text,Sympathy[1].text,text.text]   
            # 댓글 창 정보에 대한 태그
            reply = driver.find_element_by_css_selector('#ncomment')    
            # 댓글 창 정보가 있으면
            if reply != None:        
                reply_url = reply.get_attribute('src')
                driver.get(reply_url)
                replies = driver.find_elements_by_class_name('cbox_desc')
                reply_list=[reply.text for reply in replies]          
                driver.back()            
                # 다음 페이지로 넘긴다.
            mord.append(reply_list)
            mord = tuple(mord)        
            data.append(mord)
            save_csv(idx,data,stock_code)
            idx+=1
            
            # dict가 update를 쓴다.
            click_next_title()

        dtime = time.time()
        print('걸린시간:',dtime-stime)


    def date_set(self):
        print(self.collected_date)

    def execute(self):
        driver = wd.Chrome('./data/chromedriver.exe')
        driver.get( 'https://finance.naver.com/' )
        data = []   
        tag_name = driver.find_element_by_css_selector('#stock_items')

        tag_name.send_keys(self.stock_code)
        #tag_name.send_keys('119610')
        driver.find_element_by_css_selector('#header > div.snb_area > div > div.sta > form > fieldset > div > button').click()
        time.sleep(3)
        # 분석게시판으로 들어가는 기능 
        driver.find_element_by_css_selector('#content > ul > li:nth-child(7) > a > span').click()
        # 첫번째 게시글로 진입
        driver.find_element_by_css_selector('#content > div.section.inner_sub > table.type2 > tbody > tr:nth-child(3) > td.title > a').click()


        # # deadline_date를 변경해준다.

        # 게시글에 제목, 작성일, 조회수, 공감수, 비공감수. 내용을 크롤링
        title       = driver.find_element_by_css_selector('#content > div.section.inner_sub > table.view > tbody > tr:nth-child(1) > th:nth-child(1) > strong')
        date        = driver.find_element_by_css_selector('#content > div.section.inner_sub > table.view > tbody > tr:nth-child(2) > th.gray03.p9.tah')
        # name 은 정보를 가진 덩어리
        name        = driver.find_element_by_css_selector('#content > div.section.inner_sub > table.view > tbody > tr:nth-child(1) > th:nth-child(2)')
        views       = name.find_element_by_tag_name('span')
        Sympathy    = name.find_elements_by_tag_name('strong')
        text = driver.find_element_by_css_selector('#body')
        print('작성일 : %s 제목: %s 조회수 : %s 공감 : %s 비공감 : %s 내용 : %s' %(date.text,title.text, views.text, Sympathy[0].text,Sympathy[1].text,text.text))
        # 데이터 객체에 집어넣기 위한 장치와 데이터에 추가
        mord = (date.text, views.text, Sympathy[0].text,Sympathy[1].text,text.text)
        data.append(mord)
        time.sleep(1)
        # 다음 페이지로 넘긴다.
        driver.find_element_by_css_selector('#content > div.section.inner_sub > div:nth-child(5) > table > tbody > tr:nth-child(3) > td:nth-child(2) > a').click()
        #############################################################################################
        # deadline_date = '2017.09.17'#YYYY.MM.DD
        #############################################################################################
        # 수집 시작
        

        collecting(self.deadline_date, self.collected_date,self.stock_code)
        # # 에러 발생, 다시 수집
        collecting(self.deadline_date, self.collected_date)
        # # 확인
        

n = naver_crawler('000660','2017-09-07')

n.execute()