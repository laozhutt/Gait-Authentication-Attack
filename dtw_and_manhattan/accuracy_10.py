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

ROOT = '/home/tiantian/onecycleattack/Gait-Authentication-Attack/dtw_and_manhattan'
RESULTS_DIR = 'target/10'
THRESHOLD_DIR = 'target/th_10'



if __name__ == '__main__':
	TP = 0.0
	FP = 0.0
	FN = 0.0
	TN = 0.0
	#FAR = FP/(FP+TN)
	#FRR = FN/(FN+TP)
	FAR = []
	FRR = []
	far_list = []
	frr_list = []
	far_list.append(0.0)
	frr_list.append(1.0)


	filepath = os.path.join(ROOT, RESULTS_DIR)
	file_list = os.listdir(filepath)

	'''
	1. Normalization 
	'''
	threshold_dir = os.path.join(ROOT, THRESHOLD_DIR)
	if not os.path.exists(threshold_dir):
		os.system('mkdir -p {0}'.format(threshold_dir))

	for filename in file_list:
		with open(os.path.join(filepath, filename),'r') as f:
			max_num = 0.0
			min_num = 1000.0
			for line in f.readlines():
				num = float(line.strip().split(' ')[1])
				if num < min_num:
					min_num = num
				if num > max_num:
					max_num = num
			with open(os.path.join(ROOT, THRESHOLD_DIR, filename),'w') as tf:
				tf.write(str(max_num))
				tf.write('\n')
				tf.write(str(min_num))
				tf.flush()





	'''
	2. Calculate the FAR and FRR.
	'''

	if os.path.exists(os.path.join(ROOT, 'result.txt')):
		os.remove(os.path.join(ROOT, 'result.txt'))

	th = 0.0
	while(th <1):
		FAR = []
		FRR = []
		with open(os.path.join(ROOT, 'result.txt'), 'a') as r:
			

			for filename in file_list:

				with open(os.path.join(ROOT, THRESHOLD_DIR, filename),'r') as rf:
					lines = rf.readlines()
					max_num = float(lines[0].strip())
					min_num = float(lines[1].strip())


				with open(os.path.join(filepath, filename),'r') as f:
					TP = 0.0
					FP = 0.0
					FN = 0.0
					TN = 0.0
					for line in f.readlines():
						acc = (float(line.strip().split(' ')[1]) - min_num) / (max_num - min_num)
						#acc = float(line.strip().split(' ')[1])
						#print acc

						

						#find the acc of owner
						if filename in line.strip().split(' ')[0]:
							#print line.strip().split(' ')[0].split('_')[1]
							#print filename
							#print line.strip().split(' ')[1]
							if acc <= th:
								TP = TP + 1
							else:
								FN = FN + 1
						#acc of other
						else:
							if acc <= th:
								FP = FP + 1
							else:
								TN = TN + 1
				#print 'Finish calculating ' + filename + ' in threshold ' + str(th)
				#print TP
				#print FP
				#print FN
				#print TN

					FAR.append((float)(FP)/(FP+TN))
					FRR.append((float)(FN)/(FN+TP))

			far_list.append(sum(FAR)/len(FAR))
			frr_list.append(sum(FRR)/len(FRR))
			r.write(str(sum(FAR)/len(FAR)) + ' ' + str(sum(FRR)/len(FRR)) + '\n')
			r.flush()
			print 'Threshold ' + str(th) + ' down.' 
		th = th + 0.001

	far_list.append(1.0)
	frr_list.append(0.0)
	'''
	3. Plot curve.
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
	#plt.legend(loc='upper right', shadow=False)
	plt.ylabel('FRR')
	plt.xlabel('FAR')

	#plt.show()
	plt.savefig("pic10" + ".png")