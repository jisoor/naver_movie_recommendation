# 영준님 - 17년도 / 장일님 - 21년 / 지수 - 16년 /지석님 - 18년 / 동빈님 - 19년
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=ko_KR')
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=options)

review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a' # 리뷰 버튼 20년도와 다름
# review_button_xpath_6 = '//*[@id="movieEndTabMenu"]/li[6]/a' # 리뷰 버튼 6인 것도 있음. 이거하고 6다시 크로링 돌려서 콘캣
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
try:
    for i in range(1, 60): #총 59페이지
        url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2016&page={}'.format(i)
        titles = []
        reviews = []
        for j in range(1, 21):
            print(j+((i-1)*20), '번째 영화 크롤링 중')
            try:
                driver.get(url)
                movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j) #영화 제목 따오기
                title = driver.find_element_by_xpath(movie_title_xpath).text

                driver.find_element_by_xpath(movie_title_xpath).click() # 영화제목 클릭

                review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href') # 안에 주소를 긁어옴
                driver.get(review_page_url) #리뷰 링크로 들어가기
                review_range = int(driver.find_element_by_xpath(review_number_xpath).text.replace(',', '')) # 총 리뷰건수 예를들면 1,234->1234로 바꿔줌
                review_range = review_range // 10 + 2 # 한페이지당 리뷰 10개 잇으니깐
                if review_range > 6 : review_range = 5
                for k in range(1, review_range):

                    driver.get(review_page_url + '&page={}'.format(k)) # n번째 페이지를 가져와라
                    time.sleep(0.3)
                    for l in range(1, 11):
                        review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)  # 첫번째 리뷰 제목 크롤링
                        try:
                            driver.find_element_by_xpath(review_title_xpath).click()  #첫번째 리뷰 제목 클릭
                            time.sleep(0.3)
                            review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text #리뷰 내용 전부 크롤링
                            # print('================================= =================================')
                            # print(title)
                            # print(review)
                            titles.append(title)
                            reviews.append(review)
                            driver.back() # 뒤로가기
                        except:
                            # print(l, '번째 리뷰가 없다')
                            # driver.back()
                            # driver.back() #리뷰 끊기면 뒤로가기 두번해서 다시 다음 영화제목으로, 아니ㅣ면 다시 driver.get(url)
                            # driver.get(url)
                            break
            except:
                print('error')
        # try:
        #     for i in range(1, 38): .....
        # except:
        #     print('totally error')
        # finally:
        #     driver.close()

        df_review_16 = pd.DataFrame({'title':titles, 'reviews':reviews})
        df_review_16.to_csv('./crawling_data_2016_li[6]/reviews_{}_{}.csv'.format(2016, i), index=False)
except:
    print('totally error')
finally: #에러나든 안나든 모조건 실행
    driver.close()
# df_review = pd.DataFrame({'title':titles, 'reviews':'reviews'})
# df_review.to_csv('./crawling_data/reviews_{}.csv').format(2020)