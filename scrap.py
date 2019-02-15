import requests
from bs4 import BeautifulSoup
import json
import re
import csv
import pymongo

codes = []
with open('links.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            codes.append(row[1])
        line_count += 1
            
#print(codes)


num=0
for element in codes:
	num = num+1
	if num >250:
		break
	code = element
	result = requests.get("https://www.imdb.com/title/tt"+code+"/")
	src = result.content

	soup = BeautifulSoup(src, 'html.parser')

	info = soup.findAll("script",type="application/ld+json")
	info = info[0].text
	info = json.loads(info)
	# print(info)
	name = info.get('name')
	imageurl = info.get('image')
	genre = info.get('genre')
	synopsis = info.get('description')


	date = soup.findAll("a",title="See more release dates")
	date = date[0].text

	count=0
	year=""
	for i in date:
		if(i.isdigit()==True):
			count+=1
			year+=i
		else:
			count=0;
			year=""
		if(count==4):
			break		
	
	myclient = pymongo.MongoClient('mongodb://localhost:27017/')
	mydb = myclient['MyDatabase']
	mycol = mydb["Movies"]


	mydict = { "name" : name, "code" : code, "image" : imageurl,"year" : year,"genre":genre,"synopsis" : synopsis}
	print(mydict)	

	x = mycol.insert_one(mydict)
	print(x.inserted_id)
	print(num)
	print()