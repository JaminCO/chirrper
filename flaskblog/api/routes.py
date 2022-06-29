from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.models import User, Post
from flaskblog.users.utils import verify_api_token
import json, requests

api = Blueprint('api', __name__)

@api.route("/api")
def api_home2():
    return render_template('api/home.html',  title='API Home')

@api.route("/api/home")
def api_home():

    return render_template('api/home.html', title='API Home')


@api.route("/api/endpoint")
def api_endpoint():

    return render_template('api/api_endpoints.html',  title='API ENDPOINTS')

@api.route("/api/docs")
def api_docs():
    return render_template('api/api_docs.html',  title='API DOCS')


@api.route("/api/post/<int:id>", methods=['GET', 'POST'])
def api_post(id):
    page = request.args.get('page', 1, type=int)
    post = Post.query.filter_by(id=id).first()#order_by(Post.date_posted.desc())#.paginate(page=page, per_page=5)


    # for post in posts:
    #     post_data = {
    #                     "id":post.id,
    #                     # "date_posted":post.date_posted,
    #                     "title":post.title,
    #                     "content":post.content,
    #                     "author_id":post.user_id
    #                 }

    #     payload = json.dumps(post_data)
    #     print(payload)

    post_data = {
                        "id":post.id,
                        "date_posted":post.date_posted.strftime(' Published On %A-%d-%B-%Y'),
                        "title":post.title,
                        "content":post.content,
                        "author":post.author.username
                    }

    payload = json.dumps(post_data)
    # print(payload)
    print(post_data)

    return payload
    # return post_data

@api.route("/api/post/all", methods=['GET', 'POST'])
def api_all_post():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.all()#order_by(Post.date_posted.desc())#.paginate(page=page, per_page=5)

    load = []
    for post in posts:
        post_data = {
                        "id":post.id,
                        "author":post.author.username,
                        "date_posted":post.date_posted.strftime(' Published On %A-%d-%B-%Y'),
                        "title":post.title,
                        "content":post.content,
                    }

        # payload = json.dumps(post_data)
        payload = post_data
        load.append(payload)
        print(payload)
        # print(load)
        data = {"posts":load}

    return data
    # return render_template('home.html', posts=posts, title='Home')


@api.route("/api/membership", methods=['GET', 'POST'])
# @login_required
def api_membership():
    data =  {
                "membership":current_user.membership
            }
    # payload = json.dumps(data)
    # print(payload)
    # return payload

    print(data)
    return data


@api.route("/api/membership/<string:username>", methods=['GET', 'POST'])
# @login_required
def api_membership_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        data =  {
                "email":user.email,
                "username":user.username,
                "membership":user.membership
            }
        # payload = json.dumps(data)
        # print(payload)
        print(data)
    else:
        data =  {
                "email":"error",
                "username":"error",
                "membership":"error",
                "error":"INVALID USERNAME PROVIDED PLEASE CHECK THE USERNAME",
            }
        # payload = json.dumps(data)
        # print(payload)
        print(data)

    # return payload
    return data

@api.route("/api/login/email=<string:email>&password=<string:password>", methods=['GET', 'POST'])
def api_login_user(email, password):
    if current_user.is_authenticated:
        return redirect(url_for('api.api_home'))
    user = User.query.filter_by(email=email).first_or_404()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user, remember=True)
        next_page = request.args.get('next')
        print(user)
        posts = Post.query.filter_by(author=user)
        post_total = 0
        for post in posts:
            post_total += 1
        print(post_total)
        return {"username":user.username,"email":user.email,"number_of_posts":post_total,"membership":user.membership,"api_key":user.api_token}
    else:
        return {"username":None,"error":"LOGIN UNSUCCESFUL CHECK USERNAME AND PASSWORD"}

@api.route("/api/login", methods=['GET', 'POST'])
def api_login():
    if current_user.is_authenticated:
        return redirect(url_for('api.api_home'))
    return """
    <h1> LOGIN </h1>
    <p> Enter your login in details above in the url</p>
    <p>Example: http://127.1.1.1:5000/api/login/email=youremail&password=yourpassword</p>
    """

@api.route("/api/post/new", methods=['GET', 'POST'])
# @login_required
def new_post():

    return render_template("api/api_create_post.html", title="API NEW POST")

@api.route("/api/post/new/<string:token>/title=<string:title>&content=<string:content>", methods=['GET', 'POST'])
def api_new_post(token, title, content):
    # if current_user.is_authenticated:
        # return redirect(url_for('main.home'))
    user = verify_api_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('api.home'))
    print(user)
    new_title = title.replace("%20", " ")
    new_content = content.replace("%20", " ")
    print(new_title)
    print(new_content)
    post = Post(title=title, content=content, author=user)
    db.session.add(post)
    db.session.commit()
    print("Post submited")
    flash('Your post has been created!', 'success')
    return redirect(url_for('main.home'))


@api.route("/api/account", methods=['GET', 'POST'])
@login_required
def api_account():
    # form = UpdateAccountForm()
    # if form.validate_on_submit():
    #     if form.picture.data:
    #         picture_file = save_picture(form.picture.data)
    #         current_user.image_file = picture_file
    #     current_user.username = form.username.data
    #     current_user.email = form.email.data
    #     current_user.membership = form.membership.data
    #     db.session.commit()
    #     flash('Your account has been updated!', 'success')
    #     return redirect(url_for('users.account'))
    if request.method == 'GET':
        username = current_user.username
        email = current_user.email
        membership = current_user.membership
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    else:
        username = current_user.username
        email = current_user.email
        membership = current_user.membership
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    payload =   {
                    'id':current_user.id,
                    'usename':username,
                    'email':email,
                    'membership':membership,
                    'image_file':image_file,
                    'api_key':current_user.api_token
                }

    # data = json.dumps(payload)
    print(payload)
    return payload

@api.route("/api/<string:token>/account/<string:username>", methods=['GET', 'POST'])
def account(token, username):
    user = verify_api_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('api.home'))
    print(user)
    searched = User.query.filter_by(username=username).first()
    if request.method == 'GET':
        username = searched.username
        email = searched.email
        membership = searched.membership
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    else:
        username = searched.username
        email = searched.email
        membership = searched.membership
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    payload =   {
                    'id':searched.id,
                    'usename':username,
                    'email':email,
                    'membership':membership,
                    'image_file':image_file,
                    'api_token':"classified"
                }

    # data = json.dumps(payload)
    print(payload)
    return payload
