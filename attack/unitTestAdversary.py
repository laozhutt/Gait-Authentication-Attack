import os, sys
from adversary import *
from authentication import Authentication
from cycle_detection import tools
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw


if len(sys.argv)!=2:
	'''
	e.g. python unitTestAdversary.py ID130007
	'''
	print "Usage: python unitTestAdversary.py attackSample"
	exit()

ATTACK = sys.argv[1]

ROOT = '/home/tiantian/onecycleattack/Gait-Authentication-Attack/dtw_and_manhattan'
RESULTS_DIR = 'pcc_data_splitted/744_ren_data_splitted'
TRAIN_DIR = 'pcc_data_splitted/744_magnitude_ren_data_splitted'
THRESHOLD_DIR = 'target_pcc_acc_13_no_rotate_best/th_744'
LOG_DIR = '/home/tiantian/onecycleattack/Gait-Authentication-Attack/attack'

def test_binarySearch(ad):
	Seq = [0.0, 0.13, 0.24, 0.31, 0.49, 0.56, 0.61, 0.77, 0.84, 0.98] 
	testItem = [0.0, 0.04, 0.13, 0.156, 0.24, 0.30, 0.31, 0.371, 0.49, 0.491, 0.56, 0.586, 0.61, 0.666, 0.77, 0.79, 0.84, 0.954, 0.98, 0.999]

	for i in testItem:
		pos = ad.binarySearch(i, Seq)
		print(pos)

def get_dataset(attackSample):
	test_list = os.listdir(os.path.join(ROOT, RESULTS_DIR))
	cycle_test_list = ['seq0','seq1']
	test_value_list = []

	for test_session_name in test_list:

		if test_session_name != attackSample:
			for cycle_test in cycle_test_list:
				test_filepath = os.path.join(ROOT, RESULTS_DIR, test_session_name, cycle_test)
				for test_file in os.listdir(test_filepath):
					if os.path.getsize(os.path.join(test_filepath, test_file)) != 0:
						test_value_list.append(np.transpose(np.genfromtxt(os.path.join(test_filepath, test_file),delimiter=',')).tolist())

	return test_value_list





class myAuth(Authentication):

	def __init__(self, DataSet, Victim, Num):
		self.attackDataSet = DataSet
		self.victim = Victim
		self.limitedTryNum = Num
		self.count = 0

		self.timestamps_interpolated = None
		self.data_interpolated = None
		self.timestamps = None
		self.data = None
		self.sample_rate = 100
		self.data_smoothed = None
		self.smoothing_factor = 0.3
		

		self.threshold = 0.09

	def oneSampleTest(self, attackSample):
		self.count = self.count + 1
		print(str(self.count))

		#print(str(self.count) + ". " + str(attackSample))
		auth_result = self.authFunc(attackSample)
		if auth_result:
			with open(os.path.join(LOG_DIR, 'log'), 'a') as f:
				f.write(self.victim + ' ' + str(self.count) + '\n')

			print 'pass'
		else:
			print 'not pass'
		return auth_result



	def get_data(self, data_magnitude):
		data = []
		# timestamps = np.arange(0, 1.1, 1.0 / (len(data_magnitude) - 1))
		# if len(timestamps) > len(data_magnitude):
		# 	timestamps = timestamps[:len(data_magnitude)]
		# timestamps_interpolated, data_interpolated = \
		# tools.get_interpolation(timestamps, data_magnitude, target_sample_rate=self.sample_rate)  

		# for line in data_interpolated[0]:
		for line in data_magnitude:
			data.append(line)
                    
		return data

	'''
	@para victim: the No. of the victim, e.g., (ID471437 or 00m)
	@para attackSample: the cycle sample selected by kmeans++

	Return 
	True: attacker can pass the victim's model
	False: attacker can't pass the victim's model
	'''
	def authFunc(self, attackSample):
		#self.timestamps = np.arange(0.0, 1.0, 0.1)
		self.data = np.array(attackSample)


		data_magnitude = []
		for i in range(len(self.data[0])):
			data_magnitude.append(np.sqrt(np.sum(np.square(self.data[:,i]))))



		test_value = self.get_data(np.array(data_magnitude))



		'''
		1. Make seq0 as train set
		'''
		#store paticipant's filename


		#store the values correspongding to the filename

		train_values = []
		train_filepath = os.path.join(ROOT, TRAIN_DIR, self.victim, 'seq0')
		for train_file in os.listdir(train_filepath):
			train_values.append(np.loadtxt(os.path.join(train_filepath, train_file)))




		'''
		2. Calculate the similarity score and record.
		'''


		min_score = 999999.0
		for train_value in train_values:
			score = self.cal_fastdtw(test_value, train_value, False)
			if score < min_score:
				min_score = score

		'''
		3. Make a decision.
		'''
		with open(os.path.join(ROOT, THRESHOLD_DIR, self.victim),'r') as rf:
			lines = rf.readlines()
			max_num = float(lines[0].strip())
			min_num = float(lines[1].strip())


		acc = (min_score - min_num) / (max_num - min_num)
		if acc < self.threshold:
			return True
		else:
			return False


	def cal_fastdtw(self, cycle1, cycle2, rotate):
		"""Return fast dtw distance of the two cycles.

		:param cycle1: the first cycle stored the normalized maginitude data.
		:param cycle2: the second cycle stored the normalized maginitude data.
		:return: Return the dtw distance. NOte: when the lengths of the data in two cycle is the same, dtw and manhattan are the same.
		"""

		min_distance, path = fastdtw(cycle1, cycle2, dist=euclidean)

		if rotate:
			for i in range(len(cycle1)):
				distance, path = fastdtw(np.roll(cycle1,i), cycle2, dist=euclidean)
				if distance < min_distance:
					min_distance = distance
		else:
			pass

		return min_distance


if __name__ == '__main__':

	# ad = Adversary("kmeans", [])
	# test_binarySearch(ad)
	attackSample = ATTACK

	dataSet = get_dataset(attackSample)
	#dataSet = [[[1,2,3], [2,3,4], [4,5,6]], [[1,4,3], [7,3,4], [4,1,6]], [[5,1,6], [3,3,3], [1,1,6]], [[1,2,3], [2,3,4], [4,7,3]], [[5,1,9], [2,3,2], [1,9,4]], [[4,2,8], [1,6,4], [3,5,4]]]
	auth = myAuth(dataSet, attackSample , 100)
	ad = Adversary(auth)
	tryNum, pos = ad.run()