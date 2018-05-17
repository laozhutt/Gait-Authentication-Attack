"""
score on 320 dataset utilizing manhattan and dtw 

author: tiantian
date: 2018-4-29
"""


import numpy as np
import os
import sys
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw




if len(sys.argv)!=2:
	'''
	e.g. python score_320.py ID130007
	'''
	print "Usage: python score.py dirname"
	exit()


test_session = sys.argv[1]


ROOT = '/home/tiantian/onecycleattack/Gait-Authentication-Attack/dtw_and_manhattan'
RESULTS_DIR = 'pcc_data_splitted/744_magnitude_ren_data_splitted'

def train(x):
	if 'seq0' in x:
		return x

def test(x):
	if 'seq1' in x:
		return x

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

	'''
	1. Make seq0 as train set and seq1 as test set.
	'''
	#store paticipant's filename

	model_list = np.loadtxt(os.path.join(ROOT, 'model.txt'))

	#train_list = os.listdir(os.path.join(ROOT, RESULTS_DIR))
	#test_list = os.listdir(os.path.join(ROOT, RESULTS_DIR))

	train_list = ['ID' + "%06d" % i for i in model_list]
	test_list = ['ID' + "%06d" % i for i in model_list]




	#store the values correspongding to the filename
	train_value_list = []
	test_value_list = []
	for train_session_name in train_list:
		train_value = []
		train_filepath = os.path.join(ROOT, RESULTS_DIR, train_session_name, 'seq0')
		for train_file in os.listdir(train_filepath):
			train_value.append(np.loadtxt(os.path.join(train_filepath, train_file)))
		train_value_list.append(train_value)

	for test_session_name in test_list:
		test_value = []
		test_filepath = os.path.join(ROOT, RESULTS_DIR, test_session_name, 'seq1')
		for test_file in os.listdir(test_filepath):
			test_value.append(np.loadtxt(os.path.join(test_filepath, test_file)))
		test_value_list.append(test_value)


	print 'Finish the data loading.'
	


	# init the directory
	target_dir = os.path.join(ROOT, 'target', '320')
	if not os.path.exists(target_dir):
		os.system('mkdir -p {0}'.format(target_dir))

	'''
	2. Calculate the similarity score and record.
	'''
	count = 0
	#
	count = count + 1
	test_listpath = test_value_list[test_list.index(test_session)]

	with open (os.path.join(target_dir, test_session), 'w') as f:
		for train_session in train_list:
			min_score = 999999.0
			#train_filepath = os.path.join(ROOT, RESULTS_DIR, train_session)
			train_listpath = train_value_list[train_list.index(train_session)]
		
			for test_value in test_listpath:
			
				for train_value in train_listpath:
					if train_session == test_session:
						score = cal_fastdtw(test_value, train_value, False)
					else:
						score = cal_fastdtw(test_value, train_value, False)
					
					if score < min_score:
						min_score = score

					
			print str(count) + ' ' + test_session + ': finish comparing ' + train_session
			f.write(train_session + ' ' + str(min_score) + '\n')
			f.flush()
	print test_session + ': finish all.'  






	