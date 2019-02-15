from flask import Flask, render_template, request
import pymongo
import copy
import numpy

app = Flask(__name__)

def similarity(target_user,user):
	return numpy.dot(target_user, user)/(numpy.linalg.norm(target_user)*numpy.linalg.norm(user))

def itemCF():
	Number_of_Users = 10
	Number_of_Movies_Rated = 10
	K = 5
	Number_of_Most_similar_movies = 3
	Users = [[2, 3, 4, 1, 4, 4, 4, 1, 3, 4], [5, 0, 0, 2, 0, 4, 4, 5, 3, 1], [5, 0, 2, 3, 5, 5, 1, 2, 5, 4], [5, 1, 3, 3, 5, 4, 2, 2, 3, 4], [2, 0, 2, 1, 0, 4, 0, 4, 3, 5], [1, 0, 1, 4, 4, 5, 5, 1, 4, 4], [5, 4, 3, 3, 5, 5, 0, 1, 2, 0], [5, 2, 5, 5, 1, 3, 4, 0, 3, 5], [4, 3, 5, 1, 0, 4, 5, 4, 3, 1], [2, 3, 5, 3, 2, 5, 3, 1, 1, 4]]
	Original_Users = copy.deepcopy(Users)
	target_user = [2, 3, 4, 1, 4, 0, 0, 0, 0, 0]

	Users = numpy.array(Users)
	Original_Users = numpy.array(Original_Users)
	target_user = numpy.array(target_user)
	User_transpose = numpy.transpose(Users)
	Original_Users_transpose = copy.deepcopy(User_transpose)

	# print(Original_Users)
	# print(target_user)
	# print()
	# print(User_transpose)

	#Normalizing Movies
	a = numpy.sum(User_transpose,axis=1)
	b = numpy.count_nonzero(User_transpose,axis=1)
	mean = numpy.divide(a,b)
	User_transpose = User_transpose.astype(numpy.float64)

	for i in range(len(User_transpose)):
		mask = User_transpose[i] !=0
		User_transpose[i][mask] -= mean[i]
	# print(User_transpose)	

	Ratings = []
	#for movie 6
	for ij in range(Number_of_Movies_Rated):
		Sim = []
		for i in range(len(User_transpose)):
			sim = similarity(User_transpose[ij],User_transpose[i])
			Sim.append(sim)

		# print("Similarity", Sim)

		Similar_movies_index = []
		Similar_movies_values = []
		copySim = copy.deepcopy(Sim)
		for i in range(Number_of_Most_similar_movies):
			maxval = max(copySim)
			index = Sim.index(maxval)
			Similar_movies_index.append(index)
			Similar_movies_values.append(maxval)
			copySim.remove(maxval)

		# print("Similar_movies_index",Similar_movies_index)
		# print("Similar_movies_values",Similar_movies_values)

		num=0
		den=0
		for i in range(len(Similar_movies_values)):
			num += Original_Users_transpose[Similar_movies_index[i]][ij]*Similar_movies_values[i]
			if(Original_Users_transpose[Similar_movies_index[i]][ij]!=0):
				den+=Similar_movies_values[i]
			rat=0
			if(den==0):
				rat = num
			else:
				rat = num/den
		#print(rat)
		Ratings.append(rat)	
		# print()		
	# print("Ratings",Ratings)

	Max_ratings = []
	Max_ratings_index = []

	copyRatings = copy.deepcopy(Ratings)

	for i in range(K):
		maxval = max(copyRatings)
		index = Ratings.index(maxval)
		Max_ratings_index.append(index)
		Max_ratings.append(maxval)
		copyRatings.remove(maxval)
	# # print()
	# print(Max_ratings)
	# print(Max_ratings_index)
	return Max_ratings,Max_ratings_index


def UserCF(xxxx):
	Number_of_Users = 10
	Number_of_Movies_Rated = 15
	K = 5
	Number_of_Most_similar_users = Number_of_Users//2
	Users = [[2, 3, 4, 1, 4, 4, 4, 1, 3, 4, 3, 4, 5, 5, 5], [5, 0, 0, 2, 0, 4, 4, 5, 3, 1, 3, 4, 5, 5, 2], [5, 0, 2, 3, 5, 5, 1, 2, 5, 4, 3, 4, 5, 1, 5], [5, 1, 3, 3, 5, 4, 2, 2, 3, 4, 3, 4, 5, 1, 4], [2, 0, 2, 1, 0, 4, 0, 4, 3, 5, 3, 4, 5, 2, 3], [1, 0, 1, 4, 4, 5, 5, 1, 4, 4, 1, 3, 4, 3, 4], [5, 4, 3, 3, 5, 5, 0, 1, 2, 0, 1, 3, 4, 3, 4], [5, 2, 5, 5, 1, 3, 4, 0, 3, 5, 1, 3, 4, 3, 4], [4, 3, 5, 1, 0, 4, 5, 4, 3, 1, 1, 3, 4, 3, 4], [2, 3, 5, 3, 2, 5, 3, 1, 1, 4, 1, 3, 4, 3, 4]]
	Original_Users = copy.deepcopy(Users)
	#target_user = [2, 3, 4, 1, 4 ,3,0,0,0,0,0,0,0,0,0]
	target_user = xxxx
	for i in range(10):
		target_user.append(0)
	for i in target_user:
		i = int(i)		
	#Normalize
	for i in Users:
		mean = 0
		num=0
		for j in i:
			if(j!=0):
				mean = mean+j
				num+=1
		mean = mean / num			
		#print(mean)		
		for k in range(Number_of_Movies_Rated):
			if(i[k]!=0):
				i[k] -=mean
	targetmean = 0
	targetnum=0
	for j in target_user:
		if(j!=0):
			targetmean = targetmean+int(j)
			targetnum+=1
	targetmean = targetmean / targetnum					
	for k in range(Number_of_Movies_Rated):
		if(target_user[k]!=0):
			target_user[k]  = int(target_user[k]) -  targetmean			


	#print(Users)

	#print(similarity([1,2,3,4,5],[1,2,3,4,5]))
	#Finding Similarity
	Sim = []
	for i in range(Number_of_Users):
		#print("Users " ,target_user[:K]," ",Users[i][:K])
		result = similarity(target_user[:K],Users[i][:K])
		Sim.append(result)
	# print("Similarity",Sim)
	#finding similar users

	Similar_users_index = []
	Similar_users_values = []
	copySim = copy.deepcopy(Sim)
	# print("hel")
	# print(copySim)
	# print(Sim)
	for i in range(Number_of_Most_similar_users):

		maxval = max(copySim)
		index = Sim.index(maxval)
		Similar_users_index.append(index)
		Similar_users_values.append(maxval)
		copySim.remove(maxval)


	# print("Similar_users_index",Similar_users_index)
	# print("Similar_users_values",Similar_users_values)



	#Rating other Movies
	Ratings = []
	for i in range(K,Number_of_Movies_Rated):
		num = 0
		den = 0 
		for j in range(Number_of_Most_similar_users):
			ind = Similar_users_index[j]
			if(Original_Users[ind][i]==0):
				continue
			s = Similar_users_values[j]
			num = num + Original_Users[ind][i] * s
			#print("___for movie ",i," ",num," ",s," ",Original_Users[ind][i])
			if(s<0):
				s = -s
			den = den + s
		rat = num/den
		Ratings.append(rat)	

	# print("Ratings are " , Ratings)
	Max_ratings = []
	Max_ratings_index = []

	copyRatings = copy.deepcopy(Ratings)

	for i in range(K):
		maxval = max(copyRatings)
		index = Ratings.index(maxval)
		Max_ratings_index.append(index)
		Max_ratings.append(maxval)
		copyRatings.remove(maxval)
	# print()
	# print(Max_ratings)
	# print(Max_ratings_index)

	return Max_ratings,Max_ratings_index

@app.route("/")
def hello():
	myclient = pymongo.MongoClient('mongodb+srv://Shreyansh:QWERTY@cluster0-jo6dn.mongodb.net/admin')
	mydb = myclient['MyDatabase']
	mycol = mydb["Movies"]
	data = []

	for x in mycol.find():
		data.append(x)	
		#print(x)
	# print("hello")
	# print(data)
	# print("hello")	
	return render_template('index.html',data = data)

@app.route("/form.html")
def asiuf():
	myclient = pymongo.MongoClient('mongodb+srv://Shreyansh:QWERTY@cluster0-jo6dn.mongodb.net/admin')
	mydb = myclient['MyDatabase']
	mycol = mydb["Movies"]
	data = []
	ctr=0
	for x in mycol.find():
		data.append(x)	
		#print(x)
		ctr+=1
		if( ctr >4):
			break
	return render_template('form.html',data= data)

@app.route("/submit.html", methods=['POST', 'GET'])
def kasf():
	s = str(request)
	x1 = s[s.find('Rating_1')+9]
	x2 = s[s.find('Rating_2')+9]
	x3 = s[s.find('Rating_3')+9]
	x4 = s[s.find('Rating_4')+9]
	x5 = s[s.find('Rating_5')+9]
	Rat = []
	Rat.append(x1)
	Rat.append(x2)
	Rat.append(x3)
	Rat.append(x4)
	Rat.append(x5)
	
	ratings,index = UserCF(Rat)
	# print("hello")
	# print(ratings)
	# print(index)

	myclient = pymongo.MongoClient('mongodb+srv://Shreyansh:QWERTY@cluster0-jo6dn.mongodb.net/admin')
	mydb = myclient['MyDatabase']
	mycol = mydb["Movies"]
	data = []
	data2 = []

	#print(mycol.find()[3])

	
	for i in range(len(index)):
		#data1 = []
		data2.append(round(ratings[i],1))
		data.append(mycol.find()[index[i] + 5])
		#data.append(data1)
	# print(data)
	# x = mycol.find(3)
	# print(t)

	return render_template('usercf.html', data= data, data2 = data2)


@app.route("/itemcf.html")
def assacscas():
	myclient = pymongo.MongoClient('mongodb+srv://Shreyansh:QWERTY@cluster0-jo6dn.mongodb.net/admin')
	mydb = myclient['MyDatabase']
	mycol = mydb["Movies"]
	ratings,index = itemCF()
	# print("hello")
	# print(ratings)
	# print(index)

	myclient = pymongo.MongoClient('mongodb+srv://Shreyansh:QWERTY@cluster0-jo6dn.mongodb.net/admin')
	mydb = myclient['MyDatabase']
	mycol = mydb["Movies"]
	data = []
	data2 = []

	#print(mycol.find()[3])

	
	for i in range(len(index)):
		#data1 = []
		data2.append(round(ratings[i],1))
		data.append(mycol.find()[index[i]+ 5])
		#data.append(data1)
	# print(data)
	# x = mycol.find(3)
	# print(t)

	return render_template('itemcf.html', data= data, data2 = data2)


@app.route("/matrix.html")
def abababa():
	myclient = pymongo.MongoClient('mongodb+srv://Shreyansh:QWERTY@cluster0-jo6dn.mongodb.net/admin')
	mydb = myclient['MyDatabase']
	mycol = mydb["Movies"]
	ratings,index = itemCF()
	# print("hello")
	# print(ratings)
	# print(index)

	myclient = pymongo.MongoClient('mongodb+srv://Shreyansh:QWERTY@cluster0-jo6dn.mongodb.net/admin')
	mydb = myclient['MyDatabase']
	mycol = mydb["Movies"]
	data = []
	data2 = []

	#print(mycol.find()[3])

	
	for i in range(len(index)):
		#data1 = []
		data2.append(round(ratings[i],1))
		data.append(mycol.find()[index[i]+ 17])
		#data.append(data1)
	# print(data)
	# x = mycol.find(3)
	# print(t)

	return render_template('matrix.html', data= data, data2 = data2)	