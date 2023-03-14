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

# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36

opts = Options()
opts.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
)

driver = uc.Chrome()
driver.get('https://www.udemy.com' + results['url'])

# //*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[3]/div/div/div[3]/div/div[2]/div/a/span[1]/span[2]
# //*[@id="udemy"]/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[1]/span[1]/span[2]
star = driver.find_element(By.CSS_SELECTOR, '#udemy > div.ud-main-content-wrapper > div.ud-main-content > div > div > div.paid-course-landing-page__container > div.top-container.dark-background > div > div > div:nth-child(3) > div > div.clp-lead__badge-ratings-enrollment > div > a > span.star-rating-module--star-wrapper--VHfnS.star-rating-module--medium--3kDsb.star-rating-module--dark-background--3p2UF > span.ud-heading-sm.star-rating-module--rating-number--2xeHu').text
print(star)

regCount = re.sub(r'[^0-9]', '', driver.find_element(By.CLASS_NAME, 'enrollment').text)
print(regCount)

try:
    length = driver.find_element(By.CSS_SELECTOR, '#udemy > div.ud-main-content-wrapper > div.ud-main-content > div > div > div:nth-child(2) > div.heading > div.ud-container.lead-container > div.course-landing-page__main-content > div > div.clp-lead__badge-ratings-enrollment > div.clp-lead__element-item.clp-lead__element-item--row > div.course-content-length--course-content-length--zNAIv > span')
except:
    length = ''
print(length)

driver.quit()
# driver.get('https://www.udemy.com' + results['url'])

# # //*[@id="u53-tabs--14-tab-0"] 배울 내용
# # //*[@id="u53-tabs--14-tab-1"] 강의 내용
# # //*[@id="u53-tabs--14-tab-2"] 후기
# # //*[@id="u53-tabs--14-tab-3"] 강사


# lengthUnchecked = True
# while lengthUnchecked:
#     driver = uc.Chrome()
#     opts = Options()
#     opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
#     driver.get('https://www.udemy.com' + results['url'])
    
#     menuButtons = driver.find_elements(By.CLASS_NAME, 'ud-nav-button')
#     try:
#         driver.execute_script("arguments[0].click();", menuButtons[1])
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '.curriculum--content-length--5Nict'))
#         )
#         length = driver.find_element(By.CSS_SELECTOR, '.curriculum--content-length--5Nict').text
#         if length == '':
#             raise StaleElementReferenceException
#         lengthUnchecked = False
#         print(length)
#     except TimeoutException:
#         print("time out")
#         time.sleep(random.randint(1, 5))
#         driver.quit()
#         continue
#     except StaleElementReferenceException:
#         print("stale element")
#         time.sleep(random.randint(1, 5))
#         driver.quit()
#         continue
# print("length check")
# driver.quit()

# reivewUnchecked = True
# while reivewUnchecked:
#     driver = uc.Chrome()
#     opts = Options()
#     opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
#     driver.get('https://www.udemy.com' + results['url'])

#     menuButtons = driver.find_elements(By.CLASS_NAME, 'ud-nav-button')
#     try:
#         driver.execute_script("arguments[0].click();", menuButtons[2])
#         # menuButtons[2].send_keys(Keys.ENTER)
#         # reivewUnchecked = False
#         # time.sleep(10)
#         # //*[@id="u240-tabs--14-content-2"]/div/div/div/div/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/p
#         # //*[@id="u240-tabs--14-content-2"]/div/div/div/div/div/div/div[3]/div/div[1]/div[2]/div/div[2]/div[3]/div/div/div/p
#         # //*[@id="u122-tabs--14-content-2"]/div/div/div/div/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/p
#         # //*[@id="u137-tabs--14-content-2"]/div/div/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/p
#         # //*[@id="u137-tabs--14-content-2"]/div/div/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/p
        
#         # :nth-child(2) > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(1) > div > div.individual-review--individual-review-content--1EBWH > div.show-more-module--container--2QPRN > div > div > div > p
#         # #u283-tabs--6-content-2 > div > div > div > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(1) > div > div.individual-review--individual-review-content--1EBWH > div.show-more-module--container--2QPRN > div > div > div > p
#         # #u56-tabs--14-content-2 > div > div > div > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > div > div.individual-review--individual-review-content--1EBWH > div.show-more-module--container--2QPRN > div > div > div > p
#         html = driver.page_source
#         soup = BeautifulSoup(html, 'html.parser')
#         pre = soup.find(class_ = 'tabs-module--tabs-container--f-q9T').findChildren(recursive=False)
#         for i in range(1, 6):
#             # print('#' + pre[3].get('id') + ' > div > div > div > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(' + str(i) + ') > div > div.individual-review--individual-review-content--1EBWH > div.show-more-module--container--2QPRN > div > div > div > p')
#             # tar = soup.find(class_ = 'tabs-module--tabs-container--f-q9T').select_one('#' + pre[3].get('id') + ' > div > div > div > div.component-margin > div')
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, '#' + pre[3].get('id') + ' > div > div > div > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(' + str(i) + ') > div > div.individual-review--individual-review-content--1EBWH > div.show-more-module--container--2QPRN > div > div > div > p'))
#             )
#             # review = driver.find_element(By.CLASS_NAME, 'tabs-module--tabs-container--f-q9T').find_element(By.ID, pre[3].get('id')).find_element(By.CSS_SELECTOR, 'div > div > div > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(1) > div > div.individual-review--individual-review-content--1EBWH > div.show-more-module--container--2QPRN > div > div > div > p').text
#             # review = driver.find_element(By.XPATH, '//*[@id="' + pre[3].get('id') + '"]/div/div/div/div/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/p')
#             review = driver.find_element(By.CLASS_NAME, 'tabs-module--tabs-container--f-q9T').find_element(By.CSS_SELECTOR, '#' + pre[3].get('id') + ' > div > div > div > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(' + str(i) + ') > div > div.individual-review--individual-review-content--1EBWH > div.show-more-module--container--2QPRN > div > div > div > p').text
#             print(review)
#             if(review == ''):
#                 raise IndexError
            
#         # print(tar.get_text())
#         # //*[@id="u137-tabs--19-content-2"]/div/div/div/div/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/p/text()
        

#         # firstReview = reviewBox.find_elements(By.CLASS_NAME, 'individual-review--individual-review__comment--2sYGB')[0].text
#         # secondReview = reviewBox.find_elements(By.CLASS_NAME, 'individual-review--individual-review__comment--2sYGB')[1].text
#         # print(firstReview + " " + secondReview)
        
#         reivewUnchecked = False
#         # WebDriverWait(driver, 100).until(
#         #     EC.presence_of_element_located((By.CLASS_NAME, 'reviews--trigger-button-container--3IVtJ'))
#         # )
#         # driver.find_element(By.CLASS_NAME, 'reviews--trigger-button-container--3IVtJ').click()
#         # print("check")
#         # # reviews-modal--show-more-reviews-button--2nPrB
        
#         # temp = 0
#         # while(EC.presence_of_element_located(driver.find_element(By.CSS_SELECTOR, '#u57-tabs--19-content-2 > div > div > div > div > div > div > div:nth-child(3) > div > div.reviews-section--reviews-show-more--T0fxQ > button'))):
#         #     print(temp)
#         #     temp = temp + 1
#         #     driver.find_element(By.CSS_SELECTOR, '#u57-tabs--19-content-2 > div > div > div > div > div > div > div:nth-child(3) > div > div.reviews-section--reviews-show-more--T0fxQ > button').click()
#     except StaleElementReferenceException:
#         print("stale element")
#         time.sleep(random.randint(1, 5))
#         driver.quit()
#         continue
#     except TimeoutException:
#         print("time out")
#         time.sleep(random.randint(1, 5))
#         driver.quit()
#         continue
#     except IndexError:
#         print("No reivews")
#         time.sleep(random.randint(1, 5))
#         driver.quit()
#         continue
#     except NoSuchElementException as e:
#         print(NoSuchElementException)
#         time.sleep(random.randint(1, 5))
#         driver.quit()
#         continue

