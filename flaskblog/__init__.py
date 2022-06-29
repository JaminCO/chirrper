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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://slxxbwwbduxogu:816de0361e2a6e345c7b175fd9dc088e2f12b307597349c67af97b430c74ba16@ec2-44-194-145-230.compute-1.amazonaws.com:5432/ddgrod6q8l2gef'
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
