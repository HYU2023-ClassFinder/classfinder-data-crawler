from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import urllib.request
import time
import selenium
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()
reviewDriver = webdriver.Chrome()
conn = sqlite3.connect("lectureDB.db", isolation_level=None)
c = conn.cursor()

originalURL = 'https://www.coursera.org/search?query=computer%20science&page=1'
originalSoup = BeautifulSoup(urlopen(originalURL), 'html.parser')
driver.get(originalURL)

time.sleep(3)

preMaxPage = driver.find_elements(By.CLASS_NAME, 'number')
maxPage = preMaxPage[-1].find_element(By.CLASS_NAME, 'cds-33').text
lectureList = []

# c.execute('select max(lecture.id) from lecture')
# lectureID = int(c.fetchall()[0][0]) + 1
# c.execute('select max(tag.id) from tag')
# tagID = int(c.fetchall()[0][0]) + 1
# c.execute('select max(cur.id) from cur')
# curID = int(c.fetchall()[0][0]) + 1
# c.execute('select max(review.id) from review')
# reviewID = int(c.fetchall()[0][0]) + 1

lectureID = 2326
tagID = 4395
curID = 14605
reviewID = 105314

print(maxPage)
print(lectureID)
print(tagID)
print(curID)
print(reviewID)

for page in range(1, int(maxPage)+1):
    URL = 'https://www.coursera.org/search?query=computer%20science&page=' + str(page) + '&index=prod_all_launched_products_term_optimization'
    soup = BeautifulSoup(urlopen(URL), 'html.parser')
    driver.get(URL)

    try:
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'css-1pa69gt'))
        )
    except:
        print("time out")
    finally:
        pass
    time.sleep(2)

    for a in driver.find_elements(By.CLASS_NAME, 'css-1pa69gt'):
        try:
            element1 = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div > a")) and 
                EC.presence_of_element_located((By.CLASS_NAME, "css-bku0rr")) and
                EC.presence_of_element_located((By.CLASS_NAME, 'css-zl0kzj'))
            )
        except:
            print("time out")
        finally:
            pass
        time.sleep(2)

        innerURL = a.find_element(By.CSS_SELECTOR, 'div > a').get_attribute('href')
        innerSoup = BeautifulSoup(urlopen(innerURL), 'html.parser')

        name = a.find_element(By.CLASS_NAME, 'css-bku0rr').text.strip().replace("'", "").replace('"', "")
        print(str(lectureID) + " " + name)
        
        try:
            star = float(a.find_element(By.CLASS_NAME, 'css-zl0kzj').text)
        except AttributeError:
            star = 0
        except NoSuchElementException:
            star = 0
        print(star)

        try:
            regCount = int(innerSoup.select_one('._1fpiay2').findChild('span').findChild('strong').findChild('span').string.replace(",", ""))
        except AttributeError:
            regCount = 0
        print(regCount)

        lecturers = innerSoup.select('.instructor-name')
        lecturer = ""
        for l in lecturers:
            lecturer = lecturer + l.text.replace("'", "").replace('"', "") + ", "
        lecturer = lecturer[:-2]
        print(lecturer)

        length = ''

        try:
            c.execute("INSERT INTO lecture VALUES(" + str(lectureID) + ", '"  + name.replace("'", "").replace('"', "") + "', " + str(star) + ", " + str(regCount) + ", " + str(0) + ", '" + str(lecturer) + "', '" + str('')  + "')")
            conn.commit()
        except sqlite3.IntegrityError:
                pass

        tag = []
        for _ in innerSoup.select('._ontdeqt'):
            tag.append(str(_.string).strip())
            try:
                c.execute("INSERT INTO tag values(" + str(tagID) + ", "  + str(lectureID) + ", '" + str(_.string).strip().replace("'", "").replace('"', "") + "')")
                conn.commit()
            except sqlite3.IntegrityError:
                pass
            tagID = tagID + 1
        print(tag)

        curriculum = []
        if (len(innerSoup.select('._1tqo7r77 > div > h3')) != 0):
            for _ in innerSoup.select('._1tqo7r77 > div > h3'):
                curriculum.append(str(_.string).strip())
                try:
                    c.execute("INSERT INTO cur values(" + str(curID) + ", "  + str(lectureID) + ", '" + str(_.string).strip().replace("'", "").replace('"', "") + "')")
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass
                curID = curID + 1
        elif (len(innerSoup.select('._1tqo7r77 > a > div > h3')) != 0):
            for _ in innerSoup.select('._1tqo7r77 > a > div > h3'):
                curriculum.append(str(_.string).strip())
                try:
                    c.execute("INSERT INTO cur values(" + str(curID) + ", "  + str(lectureID) + ", '" + str(_.string).strip().replace("'", "").replace('"', "") + "')")
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass
                curID = curID + 1
        print(curriculum)

        reviewURL = innerURL + "/reviews"
        try:
            res = urllib.request.urlopen(reviewURL)
            reviewDriver.get(reviewURL)

            try:
                reviewElement = WebDriverWait(reviewDriver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, '_b0s5mt2'))
                )
            except:
                print("time out")
                lectureID = lectureID + 1
                continue
            finally:
                pass
            preReviewMaxPage = reviewDriver.find_elements(By.CLASS_NAME, '_b0s5mt2')
            reviewMaxPage = preReviewMaxPage[-1].find_element(By.CLASS_NAME, '_1lutnh9y').text

            print("reviewMaxPage : " + str(reviewMaxPage))
            
            for reviewPage in range(1, int(reviewMaxPage)+1):
                innerReviewURL = reviewURL + '?page=' + str(reviewPage)
                innerReviewSoup = BeautifulSoup(urlopen(innerReviewURL), 'html.parser')

                reviewDriver.get(innerReviewURL)

                starList = []
                reviewList = []

                reviewCount = 0
                checkCount = 0

                for _ in reviewDriver.find_elements(By.CSS_SELECTOR, '.rc-ReviewsContainer > .rc-ReviewsList > div > div > .css-1cyk8pe'):
                    starList.append(int(str(_.text.count("Filled Star"))))
                    # print("Filled Star : " + str(_.text.count("Filled Star")))
                    checkCount = checkCount + 1
                for _ in reviewDriver.find_elements(By.CSS_SELECTOR, '.rc-ReviewsContainer > .rc-ReviewsList > div > div > .reviewText'):
                    # print(str(_.text).strip().replace("'", "").replace('"', ""))
                    reviewList.append(str(_.text).strip().replace("'", "").replace('"', ""))
                    reviewCount = reviewCount + 1
                print(str(checkCount) + " " + str(reviewCount) + " " + str(checkCount == reviewCount))
                for i in range(reviewCount):
                    try:
                        c.execute("INSERT INTO review values(" + str(reviewID) + ", "  + str(lectureID) + ", " + str(starList[i]) + ", '" + reviewList[i] + "')")
                        conn.commit()
                    except sqlite3.IntegrityError:
                        pass
                    reviewID = reviewID + 1
            print(reviewList)

        except HTTPError as e:
            err = e.read()
            code = e.getcode()
            print(code) ## 404
            pass

        except URLError as e:
            print("No URL")
            pass

        lectureID = lectureID + 1

conn.close()