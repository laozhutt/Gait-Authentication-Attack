import numpy as np


if __name__ == '__main__':
	
	age = np.loadtxt('10.txt')

	gender = np.loadtxt('fm.txt')

	female = gender.T[0] # female
	male = gender.T[1] # male



	with open('model.txt','w') as f:
		for i in female[0:36]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[0:36]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()

		for i in female[72:113]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[72:113]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()

		for i in female[154:173]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[154:173]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()

		for i in female[192:212]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[192:212]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()

		for i in female[232:262]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[232:262]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()

		for i in female[293:307]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[293:307]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()



	with open('attack.txt','w') as f:
		for i in female[36:72]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[36:72]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()

		for i in female[113:154]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[113:154]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()

		for i in female[173:192]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[173:192]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()

		for i in female[212:232]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[212:232]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()

		for i in female[262:293]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[262:293]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()

		for i in female[307:320]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()
		for i in male[307:320]:
			i = "%06d" % i
			f.write(str(i) + '\n')
			f.flush()




	model = np.loadtxt('model.txt')
	attack = np.loadtxt('attack.txt')

	f = 0

	for i in attack:
		if i in female:
			f += 1

	print f

	# m = 0
	# f = 0
	# for i in age:
	# 	if i in female:
	# 		f += 1
	# 	if i in male:
	# 		m += 1

	# print len(age)
	# print 'female: ' + str(f)
	# print 'male: ' + str(m)



