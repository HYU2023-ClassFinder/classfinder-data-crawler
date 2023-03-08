from urllib.error import URLError, HTTPError
import urllib.request

reviewURL = 'https://www.coursera.org/specializations/introduction-computer-science-programming/reviews'
try:
    res = urllib.request.urlopen(reviewURL)
    print(res.status)
except HTTPError as e:
    err = e.read()
    code = e.getcode()
    print(code) ## 404