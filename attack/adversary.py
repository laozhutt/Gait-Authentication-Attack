'''
@description: This code is used to generate different samples for attacks on different classifiers using kmeans++ method.
@author: MeL0dy
@date: 2018/5/1
'''
import random
import math
import time
import numpy as np

class Adversary(object):

	def __init__(self, Auth):
		'''
		@Auth: An object of interface "Authentication" for specific classifier
		'''

		self.authInfo = Auth

	def run(self):
		'''
		@limitedNum: The upper bound of the number to make tries.

		TODO: Generate attack samples for authentication and return the index of the first successful attempt.(-1 means all tries on attacks failed.)
		'''
		dataSet = self.authInfo.attackDataSet
		limitedNum = self.authInfo.limitedTryNum

		dataNum = len(dataSet)
		featureList = []
		for i in range(dataNum):
			featureList.append(self.getFeature(dataSet[i]))

		attackSample = []
		random.seed(time.time())
		pos = random.randint(0, dataNum - 1)
		initial_sample = featureList[pos]
		attackSample.append(initial_sample)
		
		authRes = False
		tryNum = 1

		while tryNum <= limitedNum:

			if self.authInfo.oneSampleTest(dataSet[pos]) == True:
				authRes = True
				break

			distance = []
			for i in range(dataNum):
				distance.append(self.calNearestDist(featureList[i], attackSample))

			probDist = []
			totalDist = sum(distance)
			for i in range(dataNum):
				distance[i] = distance[i] / float(totalDist)

			probDist.append(0.0)
			for i in range(dataNum - 1):
				tmp = probDist[i]
				probDist.append(tmp + distance[i])
			probDist.append(1.0)
			
			# print(probDist)
			random.seed(time.time())
			roll = random.random()
			# print(roll)
			pos = self.binarySearch(roll, probDist)
			# print(pos)

			attackSample.append(featureList[pos])
			tryNum = tryNum + 1

		if authRes == True:
			return tryNum, pos
		else:
			return -1, -1

	def getAvg(self, x):
		array = np.array(x)
		return np.mean(array)

	def getStd(self, x):
		return np.std(x)

	def getRms(self, x):
		rootSum = 0
		for x_ in x:
			rootSum = rootSum + x_ * x_

		rms = math.sqrt(rootSum / float(len(x)))
		return rms

	def getFeature(self, cycle):

		feature = []
		myLen = len(cycle[0])
		dimension = len(cycle)
		magnitudeList = []

		for i in range(myLen):
			magnitude = 0
			for j in range(dimension):
				magnitude = magnitude + cycle[j][i] * cycle[j][i]
			magnitude = math.sqrt(magnitude)
			magnitudeList.append(magnitude)

		cycle.append(magnitudeList)

		for i in range(dimension):
			feature.append(self.getAvg(cycle[i]))
			feature.append(self.getStd(cycle[i]))
			feature.append(max(cycle[i]))
			feature.append(min(cycle[i]))
			feature.append(self.getRms(cycle[i]))

		cycle.pop()

		return feature

	# def getMeanVector(self, data):
	# 	'''
	# 	Calculate the mean vector of all data used to attack.
	# 	'''
	# 	mean_vector = []
	# 	num = len(data)
	# 	featureLength = len(data[0])

	# 	for i in range(featureLength):
	# 		mean_vector.append(0)

	# 	for i in range(num):
	# 		for j in range(featureLength):
	# 			mean_vector[j] = mean_vector[j] + data[i][j]

	# 	for i in range(featureLength):
	# 		mean_vector[i] = mean_vector[i] / float(num)

	# 	return mean_vector

	# def Authentication(self, attack):
	# 	'''
	# 	@attack: Sample used to attack

	# 	TODO: According to different classifiers which the user wants to attack, 
	# 	call different functions for authentication and get results back.

	# 	Need fixed: Here I need the interfaces of all the classifier code you guys developed.
	# 	'''

	# 	Auth = False

	# 	# if self.classifier == "...":
	# 	# 	Auth = xxx.authFunc(self.victim, attack)
	# 	# elif self.classifier == "...":
	# 	# 	Auth = xxx.authFunc(self.victim, attack)
	# 	# ...
	# 	# else Auth = xxx.authFunc(self.victim, attack)

	# 	return Auth

	def calNearestDist(self, data, allSample):
		'''
		@data: A single sample vector.
		@allSample: All samples which have been used as attack-samples before.
	
		TODO: Calculate the square of distances between the single sample and all attack samples used, then return the smallest one.
		'''
		dist = []
		featureLength = len(data)

		for sample in allSample:

			curDist = 0
			for i in range(featureLength):
				curDist = curDist + (data[i] - sample[i]) * (data[i] - sample[i])

			dist.append(curDist)

		dist.sort()
		return dist[0]

	def binarySearch(self, k, Seq):
		'''
		@k: Value to search.
		@Seq: Sequence used for searching.

		TODO: Find the position of the biggest number in the sequence whose value is smaller than k.
		'''
		l = 0
		r = len(Seq) - 1
		while r - l > 1:
			mid = (l + r) >> 1
			# print("({0}, {1})".format(l, r))
			if(Seq[mid] <= k):
				l = mid
			else:
				r = mid

		return l