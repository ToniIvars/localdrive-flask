from flask import Blueprint, render_template

drive = Blueprint('drive', __name__)

@drive.route('/')
def index():
    return render_template('drive/index.html')