
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog import db, bcrypt
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                            RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_picture, send_reset_email
import json
from uuid import uuid4

users = Blueprint('users', __name__)

 
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        token = str(uuid4())
        print(token)
        user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password, api_token=token)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)



@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login Successful WELCOME! { current_user.username }', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash('you just logged out!', 'success')
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            print(form.picture.data)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        # current_user.membership = form.membership.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        # form.membership.data = current_user.membership
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@users.route("/<int:id>/membership_upgrade", methods=['GET', 'POST'])
@login_required
def upgrade_membership(id):
    user_id = id
    user = User.query.filter_by(id=user_id).first()
    if user.membership == "Basic":
        user.membership = "Standard"
        flash(f'You are now a {user.membership} memeber', 'success')
    elif user.membership == 'Standard':
        user.membership = 'Premium'
        flash(f'You are now a {user.membership} memeber', 'success')
    elif user.membership == 'Premium':
        flash("You are already a Premium member that is the highest rank", 'info')

    db.session.commit()
    
    return redirect(url_for('users.account'))

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
    	.order_by(Post.date_posted.desc())\
    	.paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route("/delete", methods=['GET', 'POST'] )
@login_required
def delete_user():
    user = User.query.filter_by(email=current_user.email, username=current_user.username).first()
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash('Your account has been deleted!', 'info')
    return redirect(url_for('main.home'))

@users.route("/generate/token", methods=['GET', 'POST'] )
@login_required
def new_token():
    token = uuid4()
    current_user.api_token = str(token)
    print(token)
    db.session.commit()
    flash('Your API KEY has been generated', 'success')
    return redirect(url_for('users.account'))
