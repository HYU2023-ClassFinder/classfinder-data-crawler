import requests
import json
from bs4 import BeautifulSoup
import csv

# url = "https://api.coursera.org/api/courses.v1?start=0&limit=1&includes="
# data = requests.get(url).json()
# print(data)

url = "https://api.coursera.org/api/courses.v1?start=0&limit=10500&includes=instructorIds,partnerIds,specializations,s12nlds,v1Details,v2Details&fields=instructorIds,partnerIds,specializations,s12nlds,description"
data = requests.get(url).json()
print(len(data['elements']))

file_path = "./sample.json"
with open(file_path, 'w', encoding='UTF-8') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)

