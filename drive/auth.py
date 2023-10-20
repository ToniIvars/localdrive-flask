from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

from .file_handling import create_user_directory
from .models import db, User

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('alert_bad_login', 'danger')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    flash('notification_login_success', 'notification-success')
    return redirect(url_for('drive.index'))

@auth.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat-password')

    user = User.query.filter_by(username=username).first()
    if user:
        flash('alert_username_in_use', 'danger')
        return render_template('auth/signup.html', password=password, repeat_password=repeat_password)
    
    if password != repeat_password:
        flash('alert_password_mismatch', 'danger')
        return render_template('auth/signup.html', username=username, password=password)
    
    new_user = User(username=username, password=generate_password_hash(password), uuid=uuid4())
    db.session.add(new_user)
    db.session.commit()
    
    create_user_directory(new_user.uuid)

    login_user(new_user, remember=True)
    flash('notification_signup_success', 'notification-success')
    return redirect(url_for('drive.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))