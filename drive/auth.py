from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.route('/logout')
def logout():
    return 'Logout'