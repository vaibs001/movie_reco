import csv
import sys
import operator
from math import sqrt

class LoadData:

	def read_to_dictionary(self):
		"""to store the text file contents in a dictionary"""

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
		fo.close()

		return data

	def convert_to_csv(self, txt_file):
		""" To convert the text file to sorted csv file """

		#txt_file = r"u.data"
		csv_file = r"newcsv.csv"

		out_csv = csv.writer(open(csv_file, "wb"))

		csv_sort = csv.reader(open(txt_file, 'r'), delimiter = '\t')
		sort = sorted(csv_sort, key=operator.itemgetter(0))
		out_csv.writerows(sort)
		return csv_file			

	def csv_to_dictionary(self):
		""" to convert the sorted csv to dictionary """
		#csv_file = r"userdata.csv"
		csv_file = self.convert_to_csv(r"database.txt")
		reader = csv.reader(open(csv_file, 'r'))
		data = {}
		temp = {}
		flag = 0
		previousUser = None

		for row in reader:
			user, movie, rating, time = row
			if flag == 0:
				data = {user : {movie : float(rating)}}
				flag = 1
			else :
				if user not in data:
					data[user] = {}
				data[user][movie] = float(rating)
		"""	if user is not previousUser and previousUser is not None:
				data[previousUser] = temp
				temp = {}
			previousUser = user"""
			#temp[movie] = float(rating)
			#temp.append((movie, float(rating)))
		#data[previousUser] = temp
		#data = sorted(data.items(), key=operator.itemgetter(0))
		#print data

		return data

class Recommender:
	def __init__(self, input, k, n):
		"""k is number of nearest neighbors to be found
		  n is the maximum number of recommendations to be made
		  input is the dictionary containing the users and movies they have rated"""
		self.k = k
		self.n = n
		self.input = input

	def manhatan(input, rating1, rating2):
		""" returns the measure of similarity between two users """

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

	def cosine(self, rating1, rating2):
		""" compute similarity between users """
		sumxy = 0.0
		productx = 0.0
		producty = 0.0

		for movie in rating1:
			if movie in rating2:
				sumxy = sumxy + rating1[movie] * rating2[movie]
			productx = productx + rating1[movie] * rating1[movie]

		for movie in rating2:
			producty = producty + rating2[movie] * rating2[movie]

			productx = sqrt(productx)
			producty = sqrt(producty)
			distance = (float(sumxy) / float(productx * producty))

		return distance

	def nearest_neighbor(self, username, method_type):
		""" returns a sorted list of users based on the similarity with a given user """

		distance = {}
		for user in self.input:
			if user != username:
				if method_type == 1:
					x = self.manhatan(self.input[user], self.input[username])
				elif method_type == 2:
					x = self.pearson(self.input[user], self.input[username])
				else:
					x = self.cosine(self.input[user], self.input[username])
				#x = self.pearson(self.input[user], self.input[username])
				#distance.append((user, x))
				distance[user] = float(x)

		sorted_distance = sorted(distance.items(), key=operator.itemgetter(1), reverse = True)

		return sorted_distance

	def compute_recommendation_manhatan(self):
		""" to output the recommendations for different users """

		orig_stdout = sys.stdout
		f = file('out_manahatan.txt', 'w')
		sys.stdout = f

		for user in self.input:
			distance = self.nearest_neighbor(user, 1)
			count = 0
			flag = 0
			visited = {}

			print "\nHi user "+ user + ", You should watch the following movies\n"

			for instance in distance:
				movies = self.input[instance[0]]	
				#print "Similar user " + instance[0]	+ " and similarity ", instance[1]		

				if instance[1] >= 0.75:
					for movie in movies:
						if movie not in visited:
						    if movies[movie] >= 4.0 and self.input[user].has_key(movie) == False:
						        print " -----> Must Watch --> " + movie
						        count = count + 1
						        visited[movie] = 0
						    elif movies[movie] >= 3.0 and self.input[user].has_key(movie) == False:
						        print " -----> " + movie
						        count = count + 1
						        visited[movie] = 0

						    if count >= self.n:
							    flag = 1
							    break
					if flag == 1:
					    break
				else:
					break
			if count == 0:
				print "Perhaps you should rate a few more movies to get recommendations"
		sys.stdout = orig_stdout
		f.close()
	def compute_recommendation_pearson(self):
		""" to output the recommendations for different users """

		orig_stdout = sys.stdout
		f = file('out_pearson.txt', 'w')
		sys.stdout = f

		for user in self.input:
			distance = self.nearest_neighbor(user, 2)
			count = 0
			flag = 0
			visited = {}

			print "\nHi user "+ user + ", You should watch the following movies\n"
			for instance in distance:
				movies = self.input[instance[0]]	
				#print "Similar user " + instance[0]	+ " and similarity ", instance[1]		

				if instance[1] >= 0.75:
					for movie in movies:
						if movie not in visited:
						    if movies[movie] >= 4.0 and self.input[user].has_key(movie) == False:
						        print " -----> Must Watch -->" + movie
						        count = count + 1
						        visited[movie] = 0
						    elif movies[movie] >= 3.0 and self.input[user].has_key(movie) == False:
						        print " -----> " + movie
						        count = count + 1
						        visited[movie] = 0

						    if count >= self.n:
							    flag = 1
							    break
					if flag == 1:
					    break
				else:
					break
			if count == 0:
				print "Perhaps you should rate a few more movies to get recommendations"
		sys.stdout = orig_stdout
		f.close()

	def compute_recommendation_cosine(self):
		""" to output the recommendations for different users """

		orig_stdout = sys.stdout
		f = file('out_cosine.txt', 'w')
		sys.stdout = f

		for user in self.input:
			distance = self.nearest_neighbor(user, 3)
			count = 0
			flag = 0
			visited = {}

			print "\nHi user "+ user + ", You should watch the following movies\n"

			for instance in distance:
				movies = self.input[instance[0]]	
				#print "Similar user " + instance[0]	+ " and similarity ", instance[1]

				if instance[1] >= 0.75:
					for movie in movies:
						if movie not in visited:
						    if movies[movie] >= 4.0 and self.input[user].has_key(movie) == False:
						        print " -----> Must Watch --> " + movie
						        count = count + 1
						        visited[movie] = 0
						    elif movies[movie] >= 3.0 and self.input[user].has_key(movie) == False:
						        print " -----> " + movie
						        count = count + 1
						        visited[movie] = 0

						    if count >= self.n:
							    flag = 1
							    break
					if flag == 1:
					    break
				else:
					break
			if count == 0:
				print "Perhaps you should rate a few more movies to get recommendations"
		sys.stdout = orig_stdout
		f.close()


if __name__ == "__main__":
	obj = LoadData()
	users = obj.csv_to_dictionary()
	data1 = Recommender(users, 2, 2)
	data1.compute_recommendation_manhatan()
	data1.compute_recommendation_pearson()
	data1.compute_recommendation_cosine()
	print "Done"
