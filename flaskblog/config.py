import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	SECRET_KEY = os.getenv("SECRET_KEY")
	# 'fbf21f273c2b6864d2d3ee1e9ad6014f'
	SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
	# 'sqlite:///data.db'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.getenv("MAIL_USERNAME")
	# "chirrperapp@gmail.com"
	MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
	# "xwtj hbkp syyx drum"
	SQLALCHEMY_TRACK_MODIFICATIONS=True
	# os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')