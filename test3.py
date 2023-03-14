import requests
import json
import time
import random
import selenium
import sqlite3
from bs4 import BeautifulSoup
import re
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

API_HOST = "https://www.udemy.com"
path = '/api-2.0/courses/?page=2&page_size=1'
method = 'GET'
url = API_HOST + path
headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Basic bkxBbk9sMXJYV29JMFB4YnE3MHdlQ3ZGWmxkUXdBRHdSQWZycHdndzpYS1RCaWVSWmVXcld2S0VObWpqd1hqejlEV0lwU3lWVG9XTUpid28zVDlVZXZtSURVR2t4cTVVWjVFY29XT1Y4WXVvaml4ZWQ4TU8wNjI5blR1S1ZNVjlIdHhXQnVkSW8yQzl3aFNRRGFwcnNPa0ZLRUtIVXh6eVNhV0U1R3JjTQ==",
            "Content-Type": "application/json",
            # "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
body = {
    "key1": "value1",
    "key2": "value2"
}

if method == 'GET':
    response = requests.get(url, headers=headers)
elif method == 'POST':
    response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
print("response status %r" % response.status_code)
results = json.loads(response.text)['results'][0]

reivewUnchecked = True
while reivewUnchecked:
    driver = uc.Chrome()
    # Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    driver.get('https://www.udemy.com' + results['url'])

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    menuButtons = driver.find_elements(By.CLASS_NAME, 'ud-nav-button')
    driver.execute_script("arguments[0].click();", menuButtons[2])
    pre = soup.find(class_ = 'tabs-module--tabs-container--f-q9T').findChildren(recursive=False)

    try:
        temp = 0
        # #u283-tabs--6-content-2 > div > div > div > div > div > div > div:nth-child(3) > div > div.reviews-section--reviews-show-more--T0fxQ > button
        # #u194-tabs--1-content-2 > div > div > div > div > div > div > div:nth-child(3) > div > div.reviews-section--reviews-show-more--T0fxQ > button
        print('#' + pre[3].get('id') + ' > div > div > div > div > div > div > div:nth-child(3) > div > div.reviews-section--reviews-show-more--T0fxQ > button')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#' + pre[3].get('id') + ' > div > div > div > div > div > div > div:nth-child(3) > div > div.reviews-section--reviews-show-more--T0fxQ > button'))
        )
        while(driver.find_element(By.CSS_SELECTOR, '#' + pre[3].get('id') + ' > div > div > div > div > div > div > div:nth-child(3) > div > div.reviews-section--reviews-show-more--T0fxQ > button').is_displayed()):
            print(temp)
            temp = temp + 1
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#' + pre[3].get('id') + ' > div > div > div > div > div > div > div:nth-child(3) > div > div.reviews-section--reviews-show-more--T0fxQ > button'))
            )
            driver.find_element(By.CSS_SELECTOR, '#' + pre[3].get('id') + ' > div > div > div > div > div > div > div:nth-child(3) > div > div.reviews-section--reviews-show-more--T0fxQ > button').click()
        reivewUnchecked = False
    except StaleElementReferenceException as e:
        print(e)
        time.sleep(random.randint(1, 5))
        driver.quit()
        continue
    except TimeoutException as e:
        print(e)
        time.sleep(random.randint(1, 5))
        driver.quit()
        continue
    except IndexError as e:
        print(e)
        time.sleep(random.randint(1, 5))
        driver.quit()
        continue
    except NoSuchElementException as e:
        print(e)
        time.sleep(random.randint(1, 5))
        driver.quit()
        continue