# 2019.07.20-KimSeokMin
# 필요 라이브러리 : selenium, bs4(beautifulsoup)
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as BS
from multiprocessing.pool import Pool, ThreadPool
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
import threading
import re
import csv

casenum = 1


def getCaseNum(html): # 판례번호 받아오기
    global casenum
    bs = BS(html, "lxml")
    csnum = bs.find_all("a", {"class": "layer_pop_open"})
    arr = []
    for i in csnum:
        cs = i.get('id')
        cs = cs.replace("py_", "")
        arr += [[casenum, int(cs)]]
        print(casenum, cs)
        casenum += 1
    return arr


def getCase(case): # 판례 얻기
    f = open("../PRJ_Movie_for_you-1-1/case.csv", mode="a", encoding='utf-8', newline='') # case.csv 파일을 연다
    wr = csv.writer(f) # 쓰기 버전으로 연다
    driver = get_driver() # 세팅된 드라이버를 받는다.
    link = url2 + str(case[1]) # url2에 문자열 case[1](판례번호) 을 붙여 link로 받는다.
    driver.get(link) # 웹페이지 연다
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'page')))
    time.sleep(2.5)
    html = driver.page_source
    bs = BS(html, 'lxml')
    prescripts = bs.find("div", {"class": "page"}) #dive 내에 class= page라는 것을 받아온다.
    if prescripts == None: # 만약 없으면 넘어가
        return
    else: #있다면
        scripts = prescripts.find_all("p") # 모든 p가 들어간 값을 가져와서 리스트로 만듬
    result = ''
    for script in scripts:
        strong_elements = script.find_all("strong") # strong 들어간거 다받아온다.
        for strong in strong_elements: # 리스트함수에서의 각 값을
            strong.extract() #값만 추출한다.
    for script in scripts:
        result += script.get_text() # 텍스트 받아온다.
    wr.writerow([case[0], case[1], result]) # 열로 만들어서
    print(case[0])
    f.close()#닫는다.


threadLocal = threading.local() #  함수에 의해 생성되는 객체는 스레드별로 독립적인 네임스페이스로 동작한다.


def get_driver():
    driver = getattr(threadLocal, 'driver', None) # 객체에 driver의 속성값을 가져온다. 디폴트값은 None으로 준다.
    if driver is None: # driver가 default라면...
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2,
                                                            'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                            'notifications': 2, 'auto_select_certificate': 2,
                                                            'fullscreen': 2,
                                                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                            'media_stream_mic': 2, 'media_stream_camera': 2,
                                                            'protocol_handlers': 2,
                                                            'ppapi_broker': 2, 'automatic_downloads': 2,
                                                            'midi_sysex': 2,
                                                            'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                            'metro_switch_to_desktop': 2,
                                                            'protected_media_identifier': 2, 'app_banner': 2,
                                                            'site_engagement': 2,
                                                            'durable_storage': 2}}
        options.add_argument('headless')
        options.add_experimental_option('prefs', prefs)
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        driver = webdriver.Chrome(path, chrome_options=options)
        setattr(threadLocal, 'driver', driver) # 새로운 속성을 부여함 threadlocal.driver=> driver라는 의미이다.
    return driver # driver 값을 반환한다.


path = "./chromedriver"
url = "https://glaw.scourt.go.kr/wsjo/panre/sjo050.do"
url2 = "https://glaw.scourt.go.kr/wsjo/panre/sjo100.do?contId="

checknum = 1


def CaseNum(): # 판례 번호 받기
    global checknum
    # 1.대법원 사이트 접속
    case = list()
    driver = get_driver()
    driver.get(url)
    time.sleep(2)
    search_box = driver.find_element_by_name("srchw") # 검색어 위치 연결
    search_box.send_keys("손해배상") # 검색어 보내기
    driver.find_element_by_xpath('//*[@id="search"]/div[2]/fieldset/a[1]').click()# 검색버튼
    driver.find_element_by_xpath('//*[@id="search"]/div[2]/fieldset/div/p/a').click() # 자동완성 창 닫기

    # 2. 판례 번호 크롤링
    for i in range(10):
        if i == 0:
            html = driver.page_source # html은 driver.page_source
            case += getCaseNum(html) # 홈페이지에 있는 모든 판례번호 받아오기
            time.sleep(0.3)
            driver.find_element_by_xpath('//*[@id="tabwrap"]/div/div/div[1]/div[3]/div/fieldset/p/a[1]').click() # 다음페이지
            checknum += 1 # checknum 1추가
        elif (i >= 1 and i <= 9):
            html = driver.page_source
            case += getCaseNum(html) # 판례번호 받아오기
            time.sleep(0.3)
            driver.find_element_by_xpath('//*[@id="tabwrap"]/div/div/div[1]/div[3]/div/fieldset/p/a[2]').click() # 다음 페이지
            checknum += 1
        elif (i >= 10 and i < 622):
            html = driver.page_source
            case += getCaseNum(html) # 판례번호 받아오기
            time.sleep(0.5)
            button = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="tabwrap"]/div/div/div[1]/div[3]/div/fieldset/p/a[3]'))) # 5초기다리되 해당 요소가 나오면 바로 실행 다음버튼
            button.click() # 버튼 클릭
            checknum += 1
        if i == 622:
            html = driver.page_source
            case += getCaseNum(html) # 판례 번호 받아오기
            time.sleep(0.3)
            driver.find_element_by_xpath('//*[@id="tabwrap"]/div/div/div[1]/div[3]/div/fieldset/p/a[3]').click()
            html = driver.page_source
            case += getCaseNum(html)
            time.sleep(0.3)

    f = open("../PRJ_Movie_for_you-1-1/casenum.csv", mode="w", encoding='utf-8', newline='') # 쓰기 모드로 열기
    wr = csv.writer(f)
    for cs in case: # case 리스트에서 cs를 뽑아서
        wr.writerow([cs[0], cs[1]]) # 1차원 리스트에 대한 열저장
    f.close() # 닫는다.


# 1.먼저 casenum.csv 생성
CaseNum()  # 이건 처음 한번만 하고 지우기 판례번호 생성
print(checknum) # 완료 됐는지 여부 판단

f = open('../PRJ_Movie_for_you-1-1/casenum.csv', mode='r', encoding='utf-8') # 읽기 모드로 열기
rd = csv.reader(f)
arr = list(rd)  # casenum 리스트
f.close()
case = arr[:1000]  # 판례 내용에서 arr[0] 부터 arr[999]까지 자르기 알아서 원하는 개수만큼 잘라써라

# 2. case.csv 생성 *중요 : 처음 실행시에 mode = 'w'이고, 다음부턴 mode = 'a'
f2 = open("../PRJ_Movie_for_you-1-1/case.csv", mode="w", encoding='utf-8', newline='')
wr2 = csv.writer(f2)
wr2.writerow(['caseindex', 'casenum', 'script'])
f2.close()

ThreadPool(6).map(getCase, case) # 판례 받기와 판례변호인자를 maping하여 쓰레드풀을 만들어 돌린다. 즉 case 내 인자들을 이용하여 getCase를 돌린다.
#driver.close()