"""
accuracy on 744 dataset utilizing manhattan and dtw 

author: tiantian
date: 2018-4-30
"""


import numpy as np
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = '/home/tiantian/onecycleattack/mimicry-master/experiment/cycle_generation_from_dataset_774'
RESULTS_DIR = 'target'



if __name__ == '__main__':
	TP = 0.0
	FP = 0.0
	FN = 0.0
	TN = 0.0
	#FAR = FP/(FP+TN)
	#FRR = FN/(FN+TP)
	far_list = []
	frr_list = []


	filepath = os.path.join(ROOT, RESULTS_DIR)
	file_list = os.listdir(filepath)


	'''
	1. Calculate the FAR and FRR.
	'''

	th = 0.0
	while(th <10):
		with open(os.path.join(ROOT, 'result.txt'), 'a') as r:

			for filename in file_list:
				with open(os.path.join(filepath, filename)) as f:
					for line in f.readlines():

						#find the acc of owner
						if line.strip().split(' ')[0].split('_')[1] in filename:
							#print line.strip().split(' ')[0].split('_')[1]
							#print filename
							#print line.strip().split(' ')[1]
							if float(line.strip().split(' ')[1]) <= th:
								TP = TP + 1
							else:
								FN = FN + 1
						#acc of other
						else:
							if float(line.strip().split(' ')[1]) <= th:
								FP = FP + 1
							else:
								TN = TN + 1
				#print 'Finish calculating ' + filename + ' in threshold ' + str(th)
				#print TP
				#print FP
				#print FN
				#print TN

			FAR = (float)(FP)/(FP+TN)
			FRR = (float)(FN)/(FN+TP)
			far_list.append(FAR)
			frr_list.append(FRR)
			r.write(str(FAR) + ' ' + str(FRR) + '\n')
			r.flush()
			print 'Threshold ' + str(th) + ' down.' 
		th = th + 0.1


	'''
	2. Plot curve.
	'''
	font = {
		'family' : 'Bitstream Vera Sans',
		'weight' : 'bold',
		'size'   : 18
	}

	matplotlib.rc('font', **font)

	width = 12
	height = 12
	plt.figure(figsize=(width, height))

	plt.plot(np.array(far_list), np.array(frr_list), 'r')

	plt.title("ROC Curve")
	plt.legend(loc='upper right', shadow=False)
	plt.ylabel('FRR')
	plt.xlabel('FAR')

	#plt.show()
	plt.savefig("pic" + ".png")









	