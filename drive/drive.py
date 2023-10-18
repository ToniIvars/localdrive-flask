from flask import Blueprint, render_template
from flask_login import login_required

drive = Blueprint('drive', __name__)

@drive.route('/')
@login_required
def index():
    return render_template('drive/index.html')