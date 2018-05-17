"""
black-box attack interface

author: tiantian
date: 2018-5-6
"""

import numpy as np
import os
import sys

from cycle_detection import tools


ROOT = '/home/tiantian/onecycleattack/Gait-Authentication-Attack/dtw_and_manhattan'
RESULTS_DIR = 'results/744_data_magnitude_splitted'

class dtw_manhattan(object):

	def __init__(self, victim):


		self.victim= victim

		self.timestamps_interpolated = None
		self.data_interpolated = None
		self.timestamps = None
		self.data = None
		self.sample_rate = 50
		self.data_smoothed = None
		self.smoothing_factor = 0.3
		

		self.eer = 0.3





	def get_data(self, data_magnitude):
		data = []
		timestamps = np.arange(0, 1.1, 1.0 / (len(data) - 1))
		if len(timestamps) > len(data):
			timestamps = timestamps[:len(data)]
		if len(timestamps) == 0:
			continue
		timestamps_interpolated, data_interpolated = \
		tools.get_interpolation(timestamps, data_magnitude, target_sample_rate=self.sample_rate)   #get 101 sample totally
		with open(os.path.join(target_dir, str(i)), 'w') as f:
			for line in data_interpolated[0]:
				data.append[line]
                    
		return data


	'''
	@para victim: the No. of the victim, e.g., (ID471437 or 00m)
	@para attack: the cycle sample selected by kmeans++

	Return 
	True: attacker can pass the victim's model
	False: attacker can't pass the victim's model
	'''
	def authFunc(self, victim, attack):
		self.timestamps = np.arange(0.0, 1.0, 0.1)
		self.data = attack
		if len(timestamps) > len(data):
			timestamps = timestamps[:len(data)]
		
		self.timestamps_interpolated, self.data_interpolated = \
			tools.get_interpolation(self.timestamps, self.data, target_sample_rate=self.sample_rate)
		self.data_smoothed = tools.get_weighted_moving_average(self.data_interpolated, self.smoothing_factor)
		self.data_magnitude = tools.get_magnitude(self.data_smoothed)
		data = get_data(self.data_magnitude)


		'''
		1. Make seq0 as train set and seq1 as test set.
		'''
		#store paticipant's filename

		train_list = os.listdir(os.path.join(ROOT, RESULTS_DIR))


		#store the values correspongding to the filename
		train_value_list = []
		for train_session_name in train_list:
			train_value = []
			train_filepath = os.path.join(ROOT, RESULTS_DIR, train_session_name, 'seq0')
			for train_file in os.listdir(train_filepath):
				train_value.append(np.loadtxt(os.path.join(train_filepath, train_file)))
			train_value_list.append(train_value)
		print 'Finish the data loading.'

		'''
		2. Calculate the similarity score and record.
		'''


		min_score = 999999.0

		train_listpath = train_value_list[train_list.index(victim)]
	
		for train_value in train_listpath:
			score = cal_fastdtw(test_value, train_value)
			if score < min_score:
				min_score = score

		'''
		3. Make a decision.
		'''
		with open(os.path.join(ROOT, THRESHOLD_DIR, filename),'r') as rf:
			lines = rf.readlines()
			max_num = float(lines[0].strip())
			min_num = float(lines[1].strip())


		acc = (min_score - min_num) / (max_num - min_num)
		if acc < self.eer:
			return True
		else:
			return False


