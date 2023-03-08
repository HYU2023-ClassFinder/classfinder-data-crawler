import json



car_group = dict()



k5 = dict()

k5["price"] = "5000"

k5["year"] = "2015"

car_group["K52"] = k5



avante = dict()

avante["price"] = "3000"

avante["year"] = "2014"

car_group["Avante2"] = avante



#json 파일로 저장

with open('./test.json', 'a', encoding='utf-8') as make_file:

    json.dump(car_group, make_file, indent="\t")

