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
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver

while(True):
    driver = webdriver.Chrome()
    opts = Options()
    opts.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    driver.get('https://www.udemy.com/course/amazon-web-services-aws-v/')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    menuButtons = driver.find_elements(By.CLASS_NAME, 'ud-nav-button')
    driver.execute_script('arguments[0].click()', menuButtons[2])

    print("ok")
    driver.quit()

