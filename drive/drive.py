from flask import Blueprint

drive = Blueprint('drive', __name__)

@drive.route('/')
def index():
    return 'Index'

@drive.route('/profile')
def profile():
    return 'Profile'