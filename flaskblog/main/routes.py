from flask import render_template, request, Blueprint
from flaskblog.models import Post
import json

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title='Home')


# @main.route("/home/<int:id>", methods=['GET', 'POST'])
# def home_api(id):
#     page = request.args.get('page', 1, type=int)
#     post = Post.query.filter_by(id=id).first()#order_by(Post.date_posted.desc())#.paginate(page=page, per_page=5)


#     # for post in posts:
#     #     post_data = {
#     #                     "id":post.id,
#     #                     # "date_posted":post.date_posted,
#     #                     "title":post.title,
#     #                     "content":post.content,
#     #                     "author_id":post.user_id
#     #                 }

#     #     payload = json.dumps(post_data)
#     #     print(payload) 

#     post_data = {
#                         "id":post.id,
#                         "date_posted":post.date_posted.strftime(' Published On %A-%d-%B-%Y'),
#                         "title":post.title,
#                         "content":post.content,
#                         "author":post.author.username
#                     }

#     payload = json.dumps(post_data)
#     print(payload) 

#     return payload 
#     # return render_template('home.html', posts=posts, title='Home')

# @main.route("/home/api/", methods=['GET', 'POST'])
# def home_api2():
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.all()#order_by(Post.date_posted.desc())#.paginate(page=page, per_page=5)

#     load = ""    
#     for post in posts:
#         post_data = {
#                         "id":post.id,
#                         "date_posted":post.date_posted.strftime(' Published On %A-%d-%B-%Y'),
#                         "title":post.title,
#                         "content":post.content,
#                     }

#         payload = json.dumps(post_data)
#         load = load + payload
#         print(payload)
#         # print(load)

#     return load
#     # return render_template('home.html', posts=posts, title='Home')


@main.route("/about")
def about():
    return render_template('about.html', title='About')
    
#posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

@main.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')