import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	SECRET_KEY = os.getenv("SECRET_KEY")
	SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.getenv("MAIL_USERNAME")
	MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
	SQLALCHEMY_TRACK_MODIFICATIONS=True
	# os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
