import requests
import json
import time
import random
import sqlite3

conn = sqlite3.connect("lectureDB.db", isolation_level=None)
c = conn.cursor()

lectureID = 3326
tagID = 8665
curID = 19172
reviewID = 357949

print(lectureID)
print(tagID)
print(curID)
print(reviewID)

API_HOST = "https://www.udemy.com"
for i in range(1, 10001):
    path = '/api-2.0/courses/?page=' + str(i) + '&page_size=1'
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
    # print("response status %r" % response.status_code)
    try:
        result = json.loads(response.text)['results'][0]
    except KeyError:
        print(json.loads(response.text))
        break
    # print(result)
    realID = result['id']
    name = result['title'].replace("'", "").replace('"', "")
    # regCount = 
    if(result['price'] != "Free"):
        price = result['price_detail']['amount']
    else:
        price = 0
    lecturer = result['visible_instructors'][0]['display_name'].replace("'", "").replace('"', "")
    # print(i, realID, name, price, lecturer)

    lectureURL = "https://www.udemy.com/api-2.0/courses/" + str(realID) + "/?fields[course]=title,context_info,primary_category,primary_subcategory,avg_rating_recent,visible_instructors,locale,estimated_content_length,num_subscribers"
    lectureData = requests.get(lectureURL).json()

    try:
        star = lectureData['avg_rating_recent']
    except KeyError:
        star = 0

    try:
        regCount = lectureData['num_subscribers']
    except KeyError:
        regCount = 0

    print(i, realID, name, star, regCount, price, lecturer)
    try:
        c.execute("INSERT INTO lecture VALUES(" + str(lectureID) + ", '"  + name + "', " + str(star) + ", " + str(regCount) + ", " + str(price) + ", '" + str(lecturer) + "', '" + str('')  + "')")
        conn.commit()
    except sqlite3.IntegrityError:
            pass

    tag = []
    try:
        tag.append(lectureData['context_info']['category']['title'].replace("'", "").replace('"', ""))
    except KeyError:
        pass
    except TypeError:
        pass
    try:
        tag.append(lectureData['context_info']['label']['title'].replace("'", "").replace('"', ""))
    except KeyError:
        pass
    except TypeError:
        pass
    try:
        tag.append(lectureData['primary_category']['title'].replace("'", "").replace('"', ""))
    except KeyError:
        pass
    except TypeError:
        pass
    try:
        tag.append(lectureData['primary_subcategory']['title'].replace("'", "").replace('"', ""))
    except KeyError:
        pass
    except TypeError:
        pass
    tag = list(set(tag))
    for i in range(len(tag)):
        try:
            c.execute("INSERT INTO tag values(" + str(tagID) + ", "  + str(lectureID) + ", '" + tag[i] + "')")
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        tagID = tagID + 1
    print(tag)

    curriculum = []
    curriculumURL = '''https://www.udemy.com/api-2.0/courses/''' + str(realID) + '''/public-curriculum-items/'''
    curriculumResponse = requests.get(curriculumURL, headers=headers)
    curriculumData = json.loads(curriculumResponse.text)
    try:
        while(True):
            for i in range(0, len(curriculumData['results'])):
                if(curriculumData['results'][i]['_class'] == 'lecture'):
                    curriculum.append(curriculumData['results'][i]['title'].replace("'", "").replace('"', ""))
                    # print(curriculumData['results'][i]['title'])
            if(curriculumData['next'] == None):
                break
            curriculumURL = curriculumData['next']
            curriculumResponse = requests.get(curriculumURL, headers=headers)
            curriculumData = json.loads(curriculumResponse.text)
            time.sleep(random.randint(1,5))
        for i in range(len(curriculum)):
            try:
                c.execute("INSERT INTO cur values(" + str(curID) + ", "  + str(lectureID) + ", '" + curriculum[i] + "')")
                conn.commit()
            except sqlite3.IntegrityError:
                pass
            curID = curID + 1
        print(curriculum)
    except KeyError:
        pass

    review = []
    reviewURL = '''https://www.udemy.com/api-2.0/courses/''' + str(realID) + '''/reviews/?courseId=''' + str(realID) + '''&page=1&is_text_review=1&ordering=course_review_score__rank,-created&fields[course_review]=@default,response,content_html,created_formatted_with_time_since&fields[user]=@min,image_50x50,initials,public_display_name,tracking_id&fields[course_review_response]=@min,user,content_html,created_formatted_with_time_since'''
    reviewData = requests.get(reviewURL).json()
    # print(reviewData)

    try:
        while(True):
            for i in range(len(reviewData['results'])):
                singleReview = []
                reviewStar = reviewData['results'][i]['rating']
                reviewDetail = reviewData['results'][i]['content']

                singleReview.append(reviewStar)
                singleReview.append(reviewDetail.replace("'", "").replace('"', ""))

                review.append(singleReview)
                print(singleReview)

            if(reviewData['next'] == None):
                break

            reviewURL = reviewData['next']
            reviewData = requests.get(reviewURL).json()
            time.sleep(random.randint(1,5))
        for i in range(len(review)):
            try:
                c.execute("INSERT INTO review values(" + str(reviewID) + ", "  + str(lectureID) + ", " + str(review[i][0]) + ", '" + review[i][1] + "')")
                conn.commit()
            except sqlite3.IntegrityError:
                pass
            reviewID = reviewID + 1
        print(review)
    except KeyError:
        pass

    # data = 
    # pprint.pprint()
    # print("---------------------------------------")
    # pprint.pprint(requests.get(reviewURL).json())
    time.sleep(random.randint(1,5))

    lectureID = lectureID+1
conn.close()