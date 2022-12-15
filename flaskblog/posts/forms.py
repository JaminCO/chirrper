from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Choose a cover picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'GIF', 'ico'])])
    submit = SubmitField('Post')
