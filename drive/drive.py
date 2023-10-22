from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import file_handling

drive = Blueprint('drive', __name__)

@drive.route('/')
@login_required
def index():
    return render_template('drive/index.html')

@drive.route('/<name>/', defaults={'path': ''})
@drive.route('/<name>/<path:path>')
@login_required
def storage(name, path):
    if name not in ('shared', 'my-drive'):
        flash('drive_path_not_found', 'notification-danger')
        return redirect(url_for('drive.index'))

    base_path = 'shared' if name == 'shared' else str(current_user.uuid)
    content = file_handling.list_dir(base_path, path)
    
    path = [p for p in path.split('/') if p != '']
    return render_template('drive/storage.html', translate=f'drive_{name.replace("-", "")}', url_name=name, path=path, content=content)

@drive.route('/<name>/', defaults={'path': ''}, methods=['POST'])
@drive.route('/<name>/<path:path>', methods=['POST'])
@login_required
def storage_post(name, path):
    if name not in ('shared', 'my-drive'):
        flash('drive_path_not_found', 'notification-danger')
        return redirect(url_for('drive.index'))

    base_path = 'shared' if name == 'shared' else str(current_user.uuid)
    if request.form.get('modal') == 'upload':
        files = request.files.getlist('upload-file')
        for f in files:
            filename = secure_filename(f.filename)
            file_handling.save_file(base_path, f, filename, path)

        flash('drive_file_uploaded', 'notification-success')
    
    return redirect(request.url)