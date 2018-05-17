"""
accuracy on 744 dataset utilizing manhattan and dtw 
author: tiantian
date: 2018-4-30
"""



import numpy as np
import os
import sys
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


if len(sys.argv)!=2:
	'''
	e.g. python attack_dtw_owner_10.py 00m
	'''
	print "Usage: python attack_dtw_owner_10.py ID"
	exit()

train_session = sys.argv[1]

ROOT = '/home/tiantian/onecycleattack/Gait-Authentication-Attack/dtw_and_manhattan'
RESULTS_DIR = 'pcc_data_splitted/owner_magnitude_ren_data_splitted'
THRESHOLD_DIR = 'target/th_10_owner'
MIMICRY_DIR = 'pcc_data_splitted/mimicry_magnitude_ren_data_splitted'


def cal_fastdtw(cycle1, cycle2, rotate):
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
	TP = 0.0
	FP = 0.0
	FN = 0.0
	TN = 0.0
	max_num = 0.0
	min_num = 0.0

	TH = 0.051
	#FAR = FP/(FP+TN)
	#FRR = FN/(FN+TP)
	with open(os.path.join(ROOT, THRESHOLD_DIR, train_session),'r') as rf:
		lines = rf.readlines()
		max_num = float(lines[0].strip())
		min_num = float(lines[1].strip())


	'''
	1. Make train set and test set.
	'''
	#store paticipant's filename

	train_list = os.listdir(os.path.join(ROOT, RESULTS_DIR))
	test_list = os.listdir(os.path.join(ROOT, RESULTS_DIR))

	cycle_train_list = ['00','01','10','11','20']
	cycle_test_list = ['21','30','31','40','41']

	#train set includs the self data from owner and mimicry
	for cycle_train_name in cycle_train_list:
		train_values = []
		train_filepath = os.path.join(ROOT, RESULTS_DIR, train_session, cycle_train_name)
		for train_file in os.listdir(train_filepath):
			train_values.append(np.loadtxt(os.path.join(train_filepath, train_file)))
		train_filepath = os.path.join(ROOT, MIMICRY_DIR, train_session, cycle_train_name)
		for train_file in os.listdir(train_filepath):
			train_values.append(np.loadtxt(os.path.join(train_filepath, train_file)))





	print 'Finish the data loading.'


	'''
	2. Calculate the similarity score.
	'''
	#each time we need test N sequence

	for test_session in test_list:
		for cycle_test_name in cycle_test_list:
			test_values = []
			test_filepath = os.path.join(ROOT, RESULTS_DIR, test_session, cycle_test_name)
			for test_file in os.listdir(test_filepath):
				test_values.append(np.loadtxt(os.path.join(test_filepath, test_file))) # get each sequence

			min_score = 999999.0
			for test_value in test_values:
				for train_value in train_values:
					score = cal_fastdtw(test_value, train_value, False)
					if score < min_score:
						min_score = score

			acc = (min_score - min_num) / (max_num - min_num)


			if train_session == test_session:
				print min_score
				if acc <= TH:
					TP = TP + 1
					print 'TP ' + str(TP)
				else:
					FN = FN + 1
					print 'FN ' + str(FN)
			else:
				if acc <= TH:
					FP = FP + 1
					print 'FP ' + str(FP)
				else:
					TN = TN + 1
					print 'TN ' + str(TN)

	print TP
	print FN
	print FP
	print TN
	print 'owner'
	print ((float)(TP)/(TP+FN))
	print ((float)(TN)/(TN+FP))





						












