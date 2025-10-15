from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import current_user, login_user, logout_user

from ..extensions import db, bcrypt
from ..models.user import User
from ..forms import RegistrationForm, LoginForm


user = Blueprint('user', __name__)


@user.route('/user/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('post.all'))

    form = RegistrationForm()

    if request.method == 'GET':
         return render_template('user/register.html', form=form)
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        try:
            user = User.create_user(status=form.status.data, name=form.name.data, login=form.login.data, password_hsd=hashed_password)
            flash(f"User {user.login} was registered", "success")
            return redirect(url_for('user.login'))
        except Exception as e:
            print(str(e))
            flash(f"Registration error", "danger")

    return render_template('user/register.html', form=form)


@user.route('/user/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('post.all'))

    form = LoginForm()

    if request.method == 'GET':
        return render_template('user/login.html', form=form)
    
    if form.validate_on_submit():
        user = User.find_by_login(form.login.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Congratz, {form.login.data}! Login success", "success")
            return redirect(next_page) if next_page else redirect(url_for('post.all'))
        else:
            flash("Login error, please repeat", "danger")

    return render_template('user/login.html', form=form)


@user.route('/user/logout', methods=['POST', 'GET'])
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('post.all'))
    
    logout_user()
    return redirect(url_for('post.all'))