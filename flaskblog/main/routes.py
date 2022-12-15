
from flask import render_template, request, Blueprint
from flaskblog.models import Post
import json

main = Blueprint('main', __name__)

@main.route("/")
def landing():
    return "landing page"

@main.route("/explore")
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title='FEED')

@main.route("/feed")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title='EXPLORE')

@main.route("/about")
def about():
    return render_template('about.html', title='About')
    

@main.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')