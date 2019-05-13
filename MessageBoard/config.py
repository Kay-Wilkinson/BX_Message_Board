import os
from os.path import abspath, dirname, join

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') #Set DB defaults here 
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('SMTP_USERNAME')
	MAIL_PASSWORD = os.environ.get('SMTP_PASSWORD')

class TestingConfig:
	SECRET_KEY = 'cerealBox' #insecure credentials as just writing to a small test suite instance. 
	SQLALCHEMY_DATABASE_URI = "///sqlite.testing.db" #Set DB defaults here 
	SQLALCHEMY_ECHO = True