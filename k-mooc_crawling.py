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

conn = sqlite3.connect("lectureDB.db", isolation_level=None)
c = conn.cursor()

driver = webdriver.Chrome()
driver2 = webdriver.Chrome()

tagID = 0
curID = 0
reviewID = 0

# i t a

URL = 'http://www.kmooc.kr/courses?range=i'
driver.get(URL)

prev_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(5)

    current_height = driver.execute_script('return document.body.scrollHeight')

    if prev_height == current_height:
        break

    prev_height = current_height
time.sleep(5)

iLectureID = 0
iCount = int(re.sub(r'[^0-9]', '', driver.find_element(By.CLASS_NAME, 'search-status-label').text))
for i in range(iCount):
    # #main > section > section > div.courses > ul > li:nth-child(1) > article > a
    # #main > section > section > div.courses > ul > li:nth-child(2) > article > a
    a = driver.find_element(By.CSS_SELECTOR, '#main > section > section > div.courses > ul > li:nth-child(' + str(i+1) + ') > article > a')
    href = a.get_attribute('href')

    driver2.get(href)
    
    iLectureID = iLectureID + 1

print(iLectureID)

# URL = 'http://www.kmooc.kr/courses?range=t'
# driver.get(URL)

# prev_height = driver.execute_script('return document.body.scrollHeight')
# while True:
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#     time.sleep(5)

#     current_height = driver.execute_script('return document.body.scrollHeight')

#     if prev_height == current_height:
#         break

#     prev_height = current_height
# time.sleep(5)

# tLectureID = 0
# tCount = int(re.sub(r'[^0-9]', '', driver.find_element(By.CLASS_NAME, 'search-status-label').text))
# for i in range(tCount):
#     # #main > section > section > div.courses > ul > li:nth-child(1) > article > a
#     # #main > section > section > div.courses > ul > li:nth-child(2) > article > a
#     a = driver.find_element(By.CSS_SELECTOR, '#main > section > section > div.courses > ul > li:nth-child(' + str(i+1) + ') > article > a')
#     href = a.get_attribute('href')

#     driver.get(href)

#     tLectureID = tLectureID + 1

# print(tLectureID)

# URL = 'http://www.kmooc.kr/courses?range=a'
# driver.get(URL)

# prev_height = driver.execute_script('return document.body.scrollHeight')
# while True:
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#     time.sleep(5)

#     current_height = driver.execute_script('return document.body.scrollHeight')

#     if prev_height == current_height:
#         break

#     prev_height = current_height
# time.sleep(5)

# aLectureID = 0
# aCount = int(re.sub(r'[^0-9]', '', driver.find_element(By.CLASS_NAME, 'search-status-label').text))
# for i in range(aCount):
#     # #main > section > section > div.courses > ul > li:nth-child(1) > article > a
#     # #main > section > section > div.courses > ul > li:nth-child(2) > article > a
#     a = driver.find_element(By.CSS_SELECTOR, '#main > section > section > div.courses > ul > li:nth-child(' + str(i+1) + ') > article > a')
#     href = a.get_attribute('href')

#     driver.get(href)

#     aLectureID = aLectureID + 1

# print(aLectureID)

conn.close()