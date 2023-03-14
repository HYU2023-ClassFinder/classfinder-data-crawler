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

resp = requests.get('https://www.udemy.com/course/amazon-web-services-aws-v/')
html = resp.text
soup = BeautifulSoup(html, 'html.parser')
tar = soup.find(class_ = 'tabs-module--tabs-container--f-q9T').findChildren(recursive=False)

print(tar[2].get('id'))