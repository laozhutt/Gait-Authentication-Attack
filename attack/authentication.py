from abc import ABCMeta, abstractmethod

class Authentication(object):
	__metaclass__ = ABCMeta

	def __init__(self):
		pass

	@abstractmethod
	def oneSampleTest(self): 
		'''
		TODO: Return authentication result, True if pass and False otherwise
		'''
		pass
