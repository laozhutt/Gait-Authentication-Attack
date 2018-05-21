import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



LOG_DIR = '/home/tiantian/onecycleattack/Gait-Authentication-Attack/attack'
TH_DIR = '/home/tiantian/onecycleattack/Gait-Authentication-Attack/attack/threshold'

if __name__ == '__main__':

	one_attempt = [1.0]
	five_attempt = [1.0]
	ten_attempt = [1.0]
	fifth_attempt = [1.0]




	'''
	1. Calulate the attampts and the percentage of compromised users
	'''
	th = 1.01

	while(th > 0):

		th = th - 0.01

		num_list = [i for i in range(101)]
		percentage_list = [0.0 for i in range(101)]
		if not os.path.exists(os.path.join(TH_DIR,str(th))):
			continue
		with open(os.path.join(TH_DIR,str(th)),'r') as f:
			for line in f.readlines():
				value = int(line.strip().split(' ')[1])
				for i in range(101):
					if value <= i:
						percentage_list[i] += 1




		percentage_list = [v / 320 for v in percentage_list]


		one_attempt.append(percentage_list[1])
		five_attempt.append(percentage_list[5])
		ten_attempt.append(percentage_list[10])
		fifth_attempt.append(percentage_list[50])

	

		


		print '1 attempt: ' + str(percentage_list[1])
		print '5 attempts: ' + str(percentage_list[5])
		print '10 attempts: ' + str(percentage_list[10])
		print '50 attempts: ' + str(percentage_list[50])
		print '100 attempts: ' + str(percentage_list[100])

	one_attempt.append(0.0)
	five_attempt.append(0.0)
	ten_attempt.append(0.0)
	fifth_attempt.append(0.0)

	

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

	x = [i for i in range(101)]
	print len(x)
	print len(one_attempt)
	index =  [num/100.0 for i, num in enumerate(x) if i % 5 == 0]
	one_attempt =  [num for i, num in enumerate(one_attempt) if i % 5 == 0]
	five_attempt =  [num for i, num in enumerate(five_attempt) if i % 5 == 0]
	ten_attempt =  [num for i, num in enumerate(ten_attempt) if i % 5 == 0]
	fifth_attempt =  [num for i, num in enumerate(fifth_attempt) if i % 5 == 0]

	print index
	print one_attempt

	#print x[i % 5 == 0]
	plt.plot(np.array(index), np.array(one_attempt), 'blue',linestyle='-' ,label="1st try",marker='o',markerfacecolor='blue',markersize=12)
	plt.plot(np.array(index), np.array(five_attempt), 'orange',linestyle='-' ,label="5th try",marker='o',markerfacecolor='orange',markersize=12)
	plt.plot(np.array(index), np.array(ten_attempt), 'grey',linestyle='-' ,label="10th try",marker='o',markerfacecolor='grey',markersize=12)
	plt.plot(np.array(index), np.array(fifth_attempt), 'yellow',linestyle='-' ,label="50th try",marker='o',markerfacecolor='yellow',markersize=12)



	#plt.title("Attack result")
	plt.legend(loc='lower left', shadow=False)
	plt.ylabel('The percentage of compromised users')
	plt.xlabel('The threshold of black-box')

	#plt.show()
	plt.savefig("th_320" + ".png")
