import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



LOG_DIR = '/home/tiantian/onecycleattack/Gait-Authentication-Attack/attack'

if __name__ == '__main__':


	'''
	1. Calulate the attampts and the percentage of compromised users
	'''


	num_list = [i for i in range(101)]
	percentage_list = [0.0 for i in range(101)]
	with open(os.path.join(LOG_DIR,'log'),'r') as f:
		for line in f.readlines():
			value = int(line.strip().split(' ')[1])
			for i in range(101):
				if value <= i:
					percentage_list[i] += 1




	percentage_list = [v / 745 for v in percentage_list]
	print '1 attempt: ' + str(percentage_list[1])
	print '10 attempts: ' + str(percentage_list[10])
	print '50 attempts: ' + str(percentage_list[50])
	

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

	plt.plot(np.array(num_list), np.array(percentage_list), 'r',linestyle='--' ,label="Dtw classifier")

	#plt.title("Attack result")
	plt.legend(loc='lower right', shadow=False)
	plt.ylabel('The percentage of compromised users')
	plt.xlabel('Number of attempts')

	#plt.show()
	plt.savefig("attack" + ".png")