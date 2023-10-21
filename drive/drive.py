from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_required

from .file_handling import list_dir

drive = Blueprint('drive', __name__)

@drive.route('/')
@login_required
def index():
    return render_template('drive/index.html')

@drive.route('/<name>/', defaults={'path': ''})
@drive.route('/<name>/<path:path>')
@login_required
def storage(name, path):
    content = None
    if name == 'shared':
        content = list_dir('shared', path)

    elif name == 'my-drive':
        content = list_dir(str(current_user.uuid), path)

    if content is None:
        flash('drive_path_not_found', 'notification-danger')
        return redirect(url_for('drive.index'))
    
    path = [p for p in path.split('/') if p != '']
    return render_template('drive/storage.html', translate=f'drive_{name.replace("-", "")}', url_name=name, path=path, content=content)