import os

class Config:
	SECRET_KEY = 'fbf21f273c2b6864d2d3ee1e9ad6014f'
	SQLALCHEMY_DATABASE_URI = 'postgres://zxzwzwpqttfjzc:4b838ebe35a280df277340f1c36837863905f99bf19655babb9ddff9ac1f6854@ec2-44-197-128-108.compute-1.amazonaws.com:5432/davhiscuvfhsdg'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = ""
	MAIL_PASSWORD = ""