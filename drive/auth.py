from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, User

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
        return redirect(url_for('auth.signup'))
    
    if password != repeat_password:
        flash('alert_password_mismatch', 'danger')
        return redirect(url_for('auth.signup'))
    
    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    
    login_user(user, remember=True)
    flash('notification_login_success', 'notification-success')
    return redirect(url_for('drive.index'))
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))