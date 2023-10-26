from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import file_handling
from .decorators import check_drive

drive = Blueprint('drive', __name__)

@drive.route('/')
@login_required
def index():
    return render_template('drive/index.html')

@drive.route('/<name>/', defaults={'path': ''})
@drive.route('/<name>/<path:path>/')
@login_required
@check_drive
def storage(name, path):
    base_path = 'shared' if name == 'shared' else str(current_user.uuid)

    content = file_handling.list_dir(base_path, path)

    if content is None:
        flash('drive_path_not_found', 'notification-danger')
        return redirect(url_for('drive.index'))
    
    path = [p for p in path.split('/') if p != '']
    return render_template('drive/storage.html', translate=f'drive_{name.replace("-", "")}', url_name=name, path=path, content=content)

@drive.route('/<name>/', defaults={'path': ''}, methods=['POST'])
@drive.route('/<name>/<path:path>/', methods=['POST'])
@login_required
@check_drive
def storage_post(name, path):
    base_path = 'shared' if name == 'shared' else str(current_user.uuid)

    if request.form.get('modal') == 'upload':
        files = request.files.getlist('upload-file')
        for f in files:
            filename = secure_filename(f.filename)
            file_handling.save_file(base_path, f, filename, path)

        flash('drive_file_uploaded', 'notification-success')

    elif request.form.get('modal') == 'folder':
        folder_name = secure_filename(request.form.get('folder-name'))
        res = file_handling.create_dir(base_path, path, folder_name)

        flash(
            'drive_folder_created' if res else 'drive_folder_exists',
            'notification-success' if res else 'notification-danger'
        )
    
    return redirect(request.url)

@drive.route('/<modification>/<name>/', defaults={'path': ''}, methods=['POST'])
@drive.route('/<modification>/<name>/<path:path>/', methods=['POST'])
@login_required
@check_drive
def modify(modification, name, path):
    base_path = 'shared' if name == 'shared' else str(current_user.uuid)

    if modification == 'delete':
        item_name = request.form.get('item-name')
        res = file_handling.delete(base_path, path, item_name)

    elif modification == 'rename':
        item_name = request.form.get('item-name')
        new_name = request.form.get('new-name')
        res = file_handling.rename(base_path, path, item_name, new_name)

    else:
        return redirect(url_for('drive.storage', name=name, path=path))

    flash(
        f'drive_item_{modification}' if res else f'drive_item_{modification}_error',
        'notification-success' if res else 'notification-danger'
    )
    return redirect(url_for('drive.storage', name=name, path=path))

@drive.route('/duplicate/<name>/<path:path>/')
@login_required
@check_drive
def duplicate(name, path):
    base_path = 'shared' if name == 'shared' else str(current_user.uuid)

    path = path.split('/')
    path, item_name = '/'.join(path[:-1]), path[-1]

    file_handling.duplicate(base_path, path, item_name)

    flash('drive_item_duplication', 'notification-success')
    return redirect(url_for('drive.storage', name=name, path=path))