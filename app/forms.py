from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from .models.user import User


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    login = StringField('Login', validators=[DataRequired(), Length(min=2, max=20)])
    status = SelectField('Status', choices=['user', 'teacher'], coerce=str, render_kw={'class':'form-control'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=100)])
    confirmPassword= PasswordField('Confirm password', validators=[DataRequired(), Length(min=4, max=100), EqualTo('password')])
    submit = SubmitField('Done')


    def validate_login(self, login):
        user = User.find_by_login(login.data)
        if user:
            raise ValidationError('login is already use')


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Done')


class StudentForm(FlaskForm):
    student = SelectField('Student', choices=[], coerce=int, render_kw={'class':'form-control'})


class TeacherForm(FlaskForm):
    teacher = SelectField('Teacher', choices=[], render_kw={'class':'form-control'})