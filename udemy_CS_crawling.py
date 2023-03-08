from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import urllib.request
import time
import selenium
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
# reviewDriver = webdriver.Chrome()
conn = sqlite3.connect("lectureDB.db", isolation_level=None)
c = conn.cursor()

originalURL = 'https://www.udemy.com/courses/search/?p=1&q=computer+science&src=ukw'
originalSoup = BeautifulSoup(urlopen(originalURL), 'html.parser')
driver.get(originalURL)

time.sleep(3)

preMaxPage = driver.find_elements(By.CLASS_NAME, 'pagination--page--13HGb')
maxPage = preMaxPage[-1].text
lectureList = []

lectureID = 0
tagID = 0
curID = 0
reviewID = 0

print(maxPage)

for page in range(1, int(maxPage)+1):
    URL = 'https://www.udemy.com/courses/search/?p=' + str(page) + '&q=computer+science&src=ukw'
    soup = BeautifulSoup(urlopen(URL), 'html.parser')
    time.sleep(2)
    driver.get(URL)

    # try:
    #     element = WebDriverWait(driver, 100).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, 'course-card--container--1QM2W'))
    #     )
    # except:
    #     print("time out")
    # finally:
    #     pass

    for a in driver.find_elements(By.CLASS_NAME, 'course-card--container--1QM2W'):
        # try:
        #     element1 = WebDriverWait(driver, 100).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, ".course-card--course-title--vVEjC > a")) and 
        #         EC.presence_of_element_located((By.CLASS_NAME, "css-bku0rr")) and
        #         EC.presence_of_element_located((By.CLASS_NAME, 'css-zl0kzj'))
        #     )
        # except:
        #     print("time out")
        # finally:
        #     pass

        print(a.find_element(By.CLASS_NAME, 'ud-sr-only').text)

#         innerURL = a.find_element(By.CSS_SELECTOR, 'div > a').get_attribute('href')
#         innerSoup = BeautifulSoup(urlopen(innerURL), 'html.parser')

#         name = a.find_element(By.CLASS_NAME, 'css-bku0rr').text.strip().replace("'", "").replace('"', "")
#         print(str(lectureID) + " " + name)
        
#         try:
#             star = float(a.find_element(By.CLASS_NAME, 'css-zl0kzj').text)
#         except AttributeError:
#             star = 0
#         except NoSuchElementException:
#             star = 0
#         print(star)

#         try:
#             regCount = int(innerSoup.select_one('._1fpiay2').findChild('span').findChild('strong').findChild('span').string.replace(",", ""))
#         except AttributeError:
#             regCount = 0
#         print(regCount)

#         lecturers = innerSoup.select('.instructor-name')
#         lecturer = ""
#         for l in lecturers:
#             lecturer = lecturer + l.text.replace("'", "").replace('"', "") + ", "
#         lecturer = lecturer[:-2]
#         print(lecturer)

#         tag = []
#         for _ in innerSoup.select('._ontdeqt'):
#             tag.append(str(_.string).strip())
#             # try:
#             #     c.execute("INSERT INTO tag values(" + str(tagID) + ", "  + str(lectureID) + ", '" + str(_.string).strip().replace("'", "").replace('"', "") + "')")
#             #     conn.commit()
#             # except sqlite3.IntegrityError:
#             #     pass
#             tagID = tagID + 1
#         print(tag)

#         curriculum = []
#         if (len(innerSoup.select('._1tqo7r77 > div > h3')) != 0):
#             for _ in innerSoup.select('._1tqo7r77 > div > h3'):
#                 curriculum.append(str(_.string).strip())
#                 # try:
#                 #     c.execute("INSERT INTO cur values(" + str(curID) + ", "  + str(lectureID) + ", '" + str(_.string).strip().replace("'", "").replace('"', "") + "')")
#                 #     conn.commit()
#                 # except sqlite3.IntegrityError:
#                 #     pass
#                 curID = curID + 1
#         elif (len(innerSoup.select('._1tqo7r77 > a > div > h3')) != 0):
#             for _ in innerSoup.select('._1tqo7r77 > a > div > h3'):
#                 curriculum.append(str(_.string).strip())
#                 # try:
#                 #     c.execute("INSERT INTO cur values(" + str(curID) + ", "  + str(lectureID) + ", '" + str(_.string).strip().replace("'", "").replace('"', "") + "')")
#                 #     conn.commit()
#                 # except sqlite3.IntegrityError:
#                 #     pass
#                 curID = curID + 1
#         print(curriculum)

#         reviewURL = innerURL + "/reviews"
#         try:
#             res = urllib.request.urlopen(reviewURL)
#             reviewDriver.get(reviewURL)

#             try:
#                 reviewElement = WebDriverWait(reviewDriver, 10).until(
#                     EC.presence_of_element_located((By.CLASS_NAME, '_b0s5mt2'))
#                 )
#             except:
#                 print("time out")
#                 lectureID = lectureID + 1
#                 continue
#             finally:
#                 pass
#             preReviewMaxPage = reviewDriver.find_elements(By.CLASS_NAME, '_b0s5mt2')
#             reviewMaxPage = preReviewMaxPage[-1].find_element(By.CLASS_NAME, '_1lutnh9y').text

#             print("reviewMaxPage : " + str(reviewMaxPage))
            
#             reviewCount = 0
#             for reviewPage in range(1, int(reviewMaxPage)+1):
#                 innerReviewURL = reviewURL + '?page=' + str(reviewPage)
#                 innerReviewSoup = BeautifulSoup(urlopen(innerReviewURL), 'html.parser')

#                 reviewDriver.get(innerReviewURL)

#                 starList = []
#                 reviewList = []

#                 for _ in reviewDriver.find_elements(By.CSS_SELECTOR, '.rc-ReviewsContainer > .rc-ReviewsList > div > div > .css-1cyk8pe'):
#                     # starList.append(int(str(_.text).strip()))
#                     print("Filled Star : " + str(_.text.count("Filled Star")))
#                 # for _ in reviewDriver.find_elements(By.CSS_SELECTOR, '.rc-ReviewsContainer > .rc-ReviewsList > div > div > .reviewText'):
#                 #     print(str(_.text).strip().replace("'", "").replace('"', ""))
#                 #     reviewList.append(str(_.text).strip().replace("'", "").replace('"', ""))
#                 #     reviewCount = reviewCount + 1
#             print(reviewList)

#         except HTTPError as e:
#             err = e.read()
#             code = e.getcode()
#             print(code) ## 404
#             pass

#         lectureID = lectureID + 1

# conn.close()s import NoSuchElementException

