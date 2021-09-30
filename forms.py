from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):

    username = StringField("Username", validators = [InputRequired(), Length(min=4, max=20)])

    password = PasswordField('New Password', validators=[InputRequired(), 
        EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')

    email = StringField('Email Address', validators = [InputRequired(), 
        Email(message="Please enter a valid email"), Length(min=6, max=35)])

    first_name = StringField("First Name", validators = [InputRequired()])

    last_name = StringField("Last Name", validators = [InputRequired()])


class LoginForm(FlaskForm):

    username = StringField("Username", validators = [InputRequired(), Length(min=4, max=20)])

    password = PasswordField('Password', validators=[InputRequired()])


class AddFeedbackForm(FlaskForm):

    title = StringField("Title", validators=[InputRequired(), Length(min=4, max=100)])

    content = TextAreaField("Content", validators=[InputRequired()])


class EditFeedbackForm(FlaskForm):
    
    title = StringField("Title", validators=[InputRequired(), Length(min=4, max=100)])

    content = TextAreaField("Content", validators=[InputRequired()])


class ForgotPasswordForm(FlaskForm):

    email = StringField('Email Address', validators = [InputRequired(), 
    Email(message="Please enter a valid email"), Length(min=6, max=35)])


class CreateNewPasswordForm(FlaskForm):

    password = PasswordField('New Password', validators=[InputRequired(), 
        EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')



    