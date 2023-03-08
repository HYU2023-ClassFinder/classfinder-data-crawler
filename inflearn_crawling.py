from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
import time
import selenium
import sqlite3
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
conn = sqlite3.connect("lectureDB.db", isolation_level=None)
c = conn.cursor()

originalURL = 'https://www.inflearn.com/courses?order=popular&page=1'
originalSoup = BeautifulSoup(urlopen(originalURL), 'html.parser')

maxPage = originalSoup.select('#courses_section > div > div > div > footer > nav > div > ul > li > a')
lectureList = []

lectureID = 0
tagID = 0
curID = 0
reviewID = 0

for page in range(1, eval(maxPage[-1].attrs['fxd-data'])['slug']+1):
    URL = 'https://www.inflearn.com/courses?order=popular&page=' + str(page)
    soup = BeautifulSoup(urlopen(URL), 'html.parser')

    for a in soup.select('.course_card_front'):
        print(a.attrs['href'])

        innerURL = 'https://www.inflearn.com' + quote(a.attrs['href'])
        innerSoup = BeautifulSoup(urlopen(innerURL), 'html.parser')

        name = innerSoup.select_one(".cd-header__title").text.strip()
        print(str(lectureID) + " " + name)

        try:
            star = float(innerSoup.select_one('.dashboard-star__num').string)
        except AttributeError:
            star = 0

        try:
            regCount = int(innerSoup.select_one('#main > section > div.cd-sticky-wrapper > div.cd-header.cd-header__not-owned-course > div > div > div.cd-header__right.ac-cd-7.ac-ct-12 > div.cd-header__info-cover > span:nth-child(3) > strong').string.replace("명", ""))
        except AttributeError:
            regCount = 0

        try:
            price = float(re.sub(r'[^0-9]', '', innerSoup.select_one('.cd-price__reg-price').string))
        except AttributeError:
            price = 0

        lecturer = innerSoup.select_one('#main > section > div.cd-sticky-wrapper > div.cd-mb-information > div.cd-floating__info--wrapper > div > div:nth-child(1) > a').string.replace("'", "").replace('"', "")

        driver.get(innerURL)
        length = driver.find_element(By.XPATH, '//*[@id="main"]/section/div[1]/div[2]/div[3]/div/div[2]').text.replace("'", "").replace('"', "")

        print(regCount)
        print(price)
        print(lecturer)
        print(length)

        try:
            # c.execute("INSERT INTO lecture VALUES(" + str(lectureID) + ", '"  + name.replace("'", "").replace('"', "") + "', " + str(star) + ")")
            c.execute("update lecture set regCount = " + str(regCount) + ", price = " + str(price) + ", lecturer = '" + lecturer + "', len = '" + length + "' where name = '" + str(name).replace("'", "").replace('"', "") + "'")
            conn.commit()
            print(star)
        except sqlite3.IntegrityError:
            pass

        # tag = []
        # for _ in innerSoup.select('.cd-header__tag'):
        #     # tag.append(str(_.string).strip())
        #     try:
        #         c.execute("INSERT INTO tag values(" + str(tagID) + ", "  + str(lectureID) + ", '" + str(_.string).strip().replace("'", "").replace('"', "") + "')")
        #         conn.commit()
        #     except sqlite3.IntegrityError:
        #         pass
        #     tagID = tagID + 1

        # curriculum = []
        # for _ in innerSoup.select('.cd-accordion__section-title'):
        #     # curriculum.append(str(_.string).strip())
        #     try:
        #         c.execute("INSERT INTO cur values(" + str(curID) + ", "  + str(lectureID) + ", '" + str(_.string).strip().replace("'", "").replace('"', "") + "')")
        #         conn.commit()
        #     except sqlite3.IntegrityError:
        #         pass
        #     curID = curID + 1

        # try:
        #     reviewCount = int(innerSoup.select_one('.dashboard-star__text').string.rstrip("개의 수강평"))
        # except AttributeError:
        #     reviewCount = 0
        # print(reviewCount)

        # # 더보기 버튼 끝까지 클릭
        # #reviews > div.cd-review__more > button
        # driver.get(innerURL)
        
        # if(reviewCount > 0):
        #     if(reviewCount > 5):
        #         try:
        #             element = WebDriverWait(driver, 100).until(
        #                 EC.presence_of_element_located((By.CSS_SELECTOR, ".e-show-more-review"))
        #             )
        #         except:
        #             print("time out")
        #         finally:
        #             pass

        #         while driver.find_element(By.CSS_SELECTOR, ".e-show-more-review").is_displayed:
        #             try:
        #                 WebDriverWait(driver, 5).until(
        #                     EC.visibility_of_element_located((By.CSS_SELECTOR, ".e-show-more-review"))
        #                 ).send_keys(Keys.ENTER)
        #             except ElementNotInteractableException:
        #                 continue
        #             except TimeoutException:
        #                 break
        #     print(len(driver.find_elements(By.CSS_SELECTOR, '.review-el__body')))

        #     starList = []
        #     reviewList = []

        #     for _ in driver.find_elements(By.CSS_SELECTOR, '.review-el__star-num'):
        #         starList.append(int(str(_.text).strip()))
        #     for _ in driver.find_elements(By.CSS_SELECTOR, '.review-el__body'):
        #         reviewList.append(str(_.text).strip().replace("'", "").replace('"', ""))
        #     for i in range(reviewCount):
        #         try:
        #             c.execute("INSERT INTO review values(" + str(reviewID) + ", "  + str(lectureID) + ", " + str(starList[i]) + ", '" + reviewList[i] + "')")
        #             conn.commit()
        #         except sqlite3.IntegrityError:
        #             pass
        #         reviewID = reviewID + 1

        # # lecture = {'name' : name, 'star' : star, 'tag' : tag, 'curriculum' : curriculum, 'review' : review}
        # # lectureList.append(lecture)

        # lectureID = lectureID + 1

conn.close()