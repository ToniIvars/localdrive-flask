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

    elif request.form.get('modal') == 'folder':
        folder_name = request.form.get('folder-name')
        res = file_handling.create_dir(base_path, path, folder_name)

        flash(
            'drive_folder_created' if res else 'drive_folder_exists',
            'notification-success' if res else 'notification-danger'
        )
    
    return redirect(request.url)

@drive.route('/<modification>/<name>/', defaults={'path': ''}, methods=['POST'])
@drive.route('/<modification>/<name>/<path:path>', methods=['POST'])
@login_required
def modify(modification, name, path):
    if modification not in ('delete', 'rename'):
        return redirect(url_for('drive.storage', name=name, path=path))
    
    if name not in ('shared', 'my-drive'):
        flash('drive_path_not_found', 'notification-danger')
        return redirect(url_for('drive.index'))

    base_path = 'shared' if name == 'shared' else str(current_user.uuid)

    if modification == 'delete':
        item_name = request.form.get('item-name')
        file_handling.delete(base_path, path, item_name)

    else:    
        item_name = request.form.get('item-name')
        new_name = request.form.get('new-name')
        file_handling.rename(base_path, path, item_name, new_name)

    flash(f'drive_item_{modification}', 'notification-success')
    return redirect(url_for('drive.storage', name=name, path=path))

# @drive.route('/delete/<name>/', defaults={'path': ''}, methods=['POST'])
# @drive.route('/delete/<name>/<path:path>', methods=['POST'])
# @login_required
# def delete(name, path):
#     if name not in ('shared', 'my-drive'):
#         flash('drive_path_not_found', 'notification-danger')
#         return redirect(url_for('drive.index'))

#     base_path = 'shared' if name == 'shared' else str(current_user.uuid)
#     item_name = request.form.get('item-name')

#     file_handling.delete(base_path, path, item_name)

#     flash('drive_item_delete', 'notification-success')
#     return redirect(url_for('drive.storage', name=name, path=path))

# @drive.route('/rename/<name>/', defaults={'path': ''}, methods=['POST'])
# @drive.route('/rename/<name>/<path:path>', methods=['POST'])
# @login_required
# def rename(name, path):
#     if name not in ('shared', 'my-drive'):
#         flash('drive_path_not_found', 'notification-danger')
#         return redirect(url_for('drive.index'))

#     base_path = 'shared' if name == 'shared' else str(current_user.uuid)
    
#     item_name = request.form.get('item-name')
#     new_name = request.form.get('new-name')
    
#     file_handling.rename(base_path, path, item_name, new_name)

#     flash('drive_item_rename', 'notification-success')
#     return redirect(url_for('drive.storage', name=name, path=path))