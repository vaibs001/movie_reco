import csv
import sys
import operator
from math import sqrt

class load_data:

	def readToDictionary(self):
		fo = open("database.txt", "r")
		database = fo.read()
		data = {}

		user = None
		headers = None

		for line in database.splitlines():
			if line.startswith("user-id"):
				user = line.split('=')[1].strip()
				headers = None
				continue
			if user is not None and headers is None:
				headers = line.split('|')
				continue
			if user is not None and headers is not None and line:
				if not user in database:
					data[user] = []
				datum = dict(zip(headers, map(float, line.split('|'))))
				data[user] = (datum)

		return data

	def convertToCSV(self, txt_file):
		#txt_file = r"u.data"
		csv_file = r"newcsv.csv"

		out_csv = csv.writer(open(csv_file, "wb"))

		csv_sort = csv.reader(open(txt_file, 'r'), delimiter = '\t')
		sort = sorted(csv_sort, key=operator.itemgetter(0))
		out_csv.writerows(sort)
		return csv_file
			

	def csvToDictionary(self):
		#csv_file = r"userdata.csv"
		csv_file = self.convertToCSV(r"u.data")
		reader = csv.reader(open(csv_file, 'r'))
		data = {}
		temp = {}
		previousUser = "None"

		for row in reader:
			user, movie, rating, time = row

			if user is not previousUser and previousUser is not "None":
				data[previousUser] = temp
				temp = {}
			previousUser = user
			temp[movie] = float(rating)
		data[previousUser] = temp

		return data

class recommender:
	def __init__(self, input, k, n):
		"""k is number of nearest neighbors to be found
		  n is the maximum number of recommendations to be made
		  input is the dictionary containing the users and movies they have rated"""
		self.k = k
		self.n = n
		self.input = input

	def manhatan(input, rating1, rating2):
		distance = 0.0

		for movie in rating1:
			if movie in rating2:
				distance = abs(rating1[movie] - rating2[movie])

		return distance

	def pearson(input, rating1, rating2):
		""" returns measure of similarity between two users """
		sumx = 0
		sumy = 0
		sumxy = 0
		sumy2 = 0
		sumx2 = 0
		n = 0
		denominator = 0

		for movie in rating1:
			if movie in rating2:
				n = n + 1
				x = rating1[movie]
				y = rating2[movie]
				sumx = sumx + x
				sumy = sumy + y
				sumxy = sumxy + x * y
				sumx2 = sumx2 + x * x
				sumy2 = sumy2 + y * y

		if (n != 0):
			denominator = sqrt(sumx2 - (sumx ** 2) / float(n)) * sqrt(sumy2 - (sumy ** 2) / float(n))
			numerator = sumxy - (sumx * sumy) / n

		if denominator == 0:
			return 0.0
		else :
			return float(numerator / denominator)

	def nearestNeighbor(self, username):
		""" returns a sorted list of users based on the similarity with a given user """
		distance = {}
		for user in self.input:
			if user != username:
				x = self.manhatan(self.input[user], self.input[username])
				#x = self.pearson(self.input[user], self.input[username])
				#distance.append((user, x))
				distance[user] = float(x)

		sorted_distance = sorted(distance.items(), key=operator.itemgetter(1), reverse = True)

		return sorted_distance

	def computeRecommendation(self):

		orig_stdout = sys.stdout
		f = file('out.txt', 'w')
		sys.stdout = f

		for user in self.input:
			distance = self.nearestNeighbor(user)
			count = 0
			flag = 0
			visited = {}

			print "Hi user " + user + ", You should watch the following movies"

			for instance in distance:
				movies = self.input[instance[0]]	
				#print "Similar user " + instance[0]	+ " and similarity ", instance[1]		

				for movie in movies:

					if movie not in visited:
						if movies[movie] >= 3.0 and self.input[user].has_key(movie) == False:
						    print movie
						    count = count + 1
						    visited[movie] = 0
						elif movies[movie] >= 4.0 and self.input[user].has_key(movie) == False:
						    print " Must Watch " + movie
						    count = count + 1
						    visited[movie] = 0

						if count >= self.n:
							flag = 1
							break

				if flag == 1:
					break
		sys.stdout = orig_stdout
		f.close()

obj = load_data()
#obj.convertToCSV()
users = obj.csvToDictionary()
data1 = recommender(users, 3, 5)
data1.computeRecommendation()



