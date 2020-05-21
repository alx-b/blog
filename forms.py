from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    username = StringField(
        "username", validators=[InputRequired(), Length(min=3, max=20)]
    )
    password = PasswordField(
        "password", validators=[InputRequired(), Length(min=3, max=50)]
    )
    login_button = SubmitField("Log in")


class RegisterForm(FlaskForm):
    username = StringField(
        "username",
        validators=[InputRequired(), Length(min=3, max=20), Regexp("^[a-z0-9_]+$")],
    )
    password = PasswordField(
        "password", validators=[InputRequired(), Length(min=8, max=50)]
    )
    confirm_password = PasswordField(
        "password", validators=[InputRequired(), EqualTo("password")]
    )
    register_button = SubmitField("Create Account")


class ComposePostForm(FlaskForm):
    title = StringField("title", validators=[InputRequired(), Length(max=100)])
    text = TextAreaField("text", validators=[Length(max=2000)])
    submit_button = SubmitField("Submit post")
