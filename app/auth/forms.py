from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email

class LoginForm(FlaskForm):
    email=StringField('EMAIL',validators=[DataRequired(),Length(1,64),Email()])
    password=PasswordField('PASSWORD',validators=[DataRequired()])
    remember_me=BooleanField('保持登录')
    submit=SubmitField('Login in')