import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import urllib.request
import time
import selenium
import sqlite3
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def send_api(path, method):
    API_HOST = "https://www.udemy.com"
    url = API_HOST + path
    headers = {
                "Accept": "application/json, text/plain, */*",
                "Authorization": "Basic bkxBbk9sMXJYV29JMFB4YnE3MHdlQ3ZGWmxkUXdBRHdSQWZycHdndzpYS1RCaWVSWmVXcld2S0VObWpqd1hqejlEV0lwU3lWVG9XTUpid28zVDlVZXZtSURVR2t4cTVVWjVFY29XT1Y4WXVvaml4ZWQ4TU8wNjI5blR1S1ZNVjlIdHhXQnVkSW8yQzl3aFNRRGFwcnNPa0ZLRUtIVXh6eVNhV0U1R3JjTQ==",
                "Content-Type": "application/json"
    }
    body = {
        "key1": "value1",
        "key2": "value2"
    }
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
        print("response status %r" % response.status_code)
        results = json.loads(response.text)['results'][0]
        name = results['title']
        # star = results['avg_rating']
        # regCount = results['num_subscribers']
        price = results['price']
        lecturer = results['visible_instructors'][0]['title']
        length = ''

        print(results)
        print(name)
        print(price)
        print(lecturer)

        driver = webdriver.Chrome()
        driver.get('https://www.udemy.com' + results['url'])

        star = driver.find_element(By.CLASS_NAME, 'star-rating--rating-number--3l80q').text
        print(star)
        
        regCount = re.sub(r'[^0-9]', '', driver.find_element(By.CLASS_NAME, 'enrollment').text)
        print(regCount)

        menuButtons = driver.find_elements(By.CLASS_NAME, 'ud-nav-button')
        print(len(menuButtons))
        # menuButtons[1].click()
        # time.sleep(10)
        # length = driver.find_element(By.CSS_SELECTOR, '#u65-tabs--27-content-1 > div > div > div:nth-child(3) > div > div > div.curriculum--curriculum-sub-header--m_N_0 > div > span > span > span').text
        # print(length)
        
        menuButtons[2].click()
        time.sleep(10)
        driver.find_element(By.CLASS_NAME, 'reviews--trigger-button-container--3IVtJ').click()

        # reviews-modal--show-more-reviews-button--2nPrB
        while(EC.presence_of_element_located(driver.find_element(By.CLASS_NAME, 'reviews-modal--show-more-reviews-button--2nPrB'))):
            driver.find_element(By.CLASS_NAME, 'reviews-modal--show-more-reviews-button--2nPrB').click()
            time.sleep(3)


        time.sleep(10)

    except Exception as ex:
        print(ex)

send_api("/api-2.0/courses/?page=2&page_size=1", "GET")
