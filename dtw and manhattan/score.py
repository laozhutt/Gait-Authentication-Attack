"""
score on 744 dataset utilizing manhattan and dtw 

author: tiantian
date: 2018-4-29
"""


import numpy as np
import os
import sys
from cycle_detection import tools as tool

if len(sys.argv)!=2:
	'''
	e.g. python score.py T0_ID130007_Center_seq1
	'''
	print "Usage: python score.py filename"
	exit()


test_session = sys.argv[1]


ROOT = '/home/tiantian/onecycleattack/mimicry-master/experiment/cycle_generation_from_dataset_774'
RESULTS_DIR = 'results_magnitude/data_magnitude_splitted'

def train(x):
	if 'seq0' in x:
		return x

def test(x):
	if 'seq1' in x:
		return x

if __name__ == '__main__':

	'''
	1. Make seq0 as train set and seq1 as test set.
	'''
	#store paticipant's filename
	train_list = filter(train, os.listdir(os.path.join(ROOT, RESULTS_DIR)))
	test_list = filter(test, os.listdir(os.path.join(ROOT, RESULTS_DIR)))

	#store the values correspongding to the filename
	train_value_list = []
	test_value_list = []
	for train_session_name in train_list:
		train_value = []
		train_filepath = os.path.join(ROOT, RESULTS_DIR, train_session_name)
		for train_file in os.listdir(train_filepath):
			train_value.append(np.loadtxt(os.path.join(train_filepath, train_file)))
		train_value_list.append(train_value)

	for test_session_name in test_list:
		test_value = []
		test_filepath = os.path.join(ROOT, RESULTS_DIR, test_session_name)
		for test_file in os.listdir(test_filepath):
			test_value.append(np.loadtxt(os.path.join(test_filepath, test_file)))
		test_value_list.append(test_value)


	print 'Finish the data loading.'
	


	# init the directory
	target_dir = os.path.join(ROOT, 'target')
	if not os.path.exists(target_dir):
		os.system('mkdir -p {0}'.format(target_dir))

	'''
	2. Calculate the similarity score and record.
	'''
	count = 0
	#
	count = count + 1
	test_listpath = test_value_list[test_list.index(test_session)]
	#print test_listpath
	#test_filepath = os.path.join(ROOT, RESULTS_DIR, test_session)
	with open (os.path.join(target_dir, test_session), 'w') as f:
		for train_session in train_list:
			min_score = 999999.0
			#train_filepath = os.path.join(ROOT, RESULTS_DIR, train_session)
			train_listpath = train_value_list[train_list.index(train_session)]
		
			for test_value in test_listpath:
			
				for train_value in train_listpath:
					score = tool.cal_fastdtw(test_value, train_value)
					if score < min_score:
						min_score = score
					#print score
					#print min_score
					#print tool.cal_fastdtw(os.path.join(test_filepath, test_file), os.path.join(train_filepath, train_file))
					
			print str(count) + ' ' + test_session + ': finish comparing ' + train_session
			f.write(train_session + ' ' + str(min_score) + '\n')
			f.flush()
	print test_session + ': finish all.'  






	