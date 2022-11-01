from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flaskblog.users.utils import send_reset_email, save_picture_c
import os
import secrets
from PIL import Image
from flask import current_app

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title_p = (form.title.data).title()
        picture = request.files["picture"]
        print(picture)
        if picture:
            print(picture)
            picture_fn = save_picture_c(picture)
            print(picture_fn)
            post = Post(title=title_p, content=form.content.data, content_img=picture_fn, author=current_user)
        else:
            post = Post(title=title_p, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post', value='/post/new')


@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.content_img: 
        image_file = url_for('static', filename='content_pics/' + post.content_img)
        return render_template('post.html', title=post.title, post=post, image_file=image_file)
    else:
        return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        picture = request.files["picture"]
        if picture.filename:
            print(picture)
            picture_fn = save_picture_c(picture)

            post.title = (form.title.data).title()
            post.content = form.content.data
            post.content_img = picture_fn
        else:
            post.title = (form.title.data).title()
            post.content = form.content.data

        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        # form.picture.data = post.content_img
    # image_file = url_for('static', filename='content_pics/' + post.content_img)
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post', value=f'/post/{post.id}/update')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
