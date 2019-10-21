'''
Flask configuration class
'''
import os

class Config:

	TESTING = os.environ.get('TESTING')
	DEBUG = os.environ.get('DEBUG')
	SECRET_KEY = os.environ.get('SECRET_KEY')
	DATABASE = os.environ.get('DATABASE')