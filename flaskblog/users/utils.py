import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail
from flaskblog.models import User, Post


def save_picture(form_picture):
    print(form_picture)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_picture_c(picture): 
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/content_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender="chirrper@gmail.com",
                  recipients=[user.email])
    msg.body = f'''Hello {(user.username).title()}. There was a Request To reset your password, please visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
For Additional Measures Contact Us.
'''
    mail.send(msg)

def verify_api_token(token):
        token_owner = User.query.filter_by(api_token=token).first
        print(token_owner)
        try:
            user = User.query.filter_by(api_token=token).first()
        except:
            return None
        return user


def send_redeem_email(transaction):
    token=transaction.token
    msg = Message('$$$ You were Gifted $$$',
                  sender="chirrper@gmail.com",
                  recipients=[transaction.reciever.email])
    msg.body = f'''{(transaction.reciever.username).title()}!!!
You Just recieved {transaction.amount}$ worth of Chirrpey from {transaction.sender.username}
$       .       .       .       .       .       $       .       .       .       .       .       $|
To Redeem your gift click the url here -->>: {url_for('users.redeem_gift', token=token, _external=True)}
For more details on your gift check the below url
{url_for('users.gift_details', token=token, _external=True)}
'''
    mail.send(msg)
