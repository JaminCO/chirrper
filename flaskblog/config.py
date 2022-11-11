import os

class Config:
	SECRET_KEY = 'fbf21f273c2b6864d2d3ee1e9ad6014f'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = ""
	MAIL_PASSWORD = ""
