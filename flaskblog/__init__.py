from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.config import Config

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zxzwzwpqttfjzc:4b838ebe35a280df277340f1c36837863905f99bf19655babb9ddff9ac1f6854@ec2-44-197-128-108.compute-1.amazonaws.com:5432/davhiscuvfhsdg'
db = SQLAlchemy(app)

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db = SQLAlchemy(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main
	from flaskblog.errors.handlers import errors
	from flaskblog.api.routes import api
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)
	app.register_blueprint(api)

	return app
