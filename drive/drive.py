from flask import Blueprint, flash, render_template, redirect, url_for, request, send_file
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import file_handling
from .decorators import check_drive

drive = Blueprint('drive', __name__)

@drive.route('/')
@login_required
def index():
    return render_template('drive/index.html')

@drive.route('/<drive>/', defaults={'path': ''})
@drive.route('/<drive>/<path:path>/')
@login_required
@check_drive
def storage(drive, path):
    base_path = 'shared' if drive == 'shared' else str(current_user.uuid)

    content = file_handling.list_dir(base_path, path)

    if content is None:
        flash('drive_path_not_found', 'notification-danger')
        return redirect(url_for('drive.index'))
    
    path = [p for p in path.split('/') if p != '']
    return render_template('drive/storage.html', translate=f'drive_{drive.replace("-", "")}', drive=drive, path=path, content=content)

@drive.route('/<drive>/', defaults={'path': ''}, methods=['POST'])
@drive.route('/<drive>/<path:path>/', methods=['POST'])
@login_required
@check_drive
def storage_post(drive, path):
    base_path = 'shared' if drive == 'shared' else str(current_user.uuid)

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

@drive.route('/delete/<drive>/', defaults={'path': ''}, methods=['POST'])
@drive.route('/delete/<drive>/<path:path>/', methods=['POST'])
@login_required
@check_drive
def delete(drive, path):
    base_path = 'shared' if drive == 'shared' else str(current_user.uuid)

    item_name = request.form.get('item-name')
    res = file_handling.delete(base_path, path, item_name)

    flash(
        'drive_item_delete' if res else 'drive_item_delete_error',
        'notification-success' if res else 'notification-danger'
    )
    return redirect(url_for('drive.storage', drive=drive, path=path))

@drive.route('/rename/<drive>/', defaults={'path': ''}, methods=['POST'])
@drive.route('/rename/<drive>/<path:path>/', methods=['POST'])
@login_required
@check_drive
def rename(drive, path):
    base_path = 'shared' if drive == 'shared' else str(current_user.uuid)

    item_name = request.form.get('item-name')
    new_name = request.form.get('new-name')
    res = file_handling.rename(base_path, path, item_name, new_name)

    flash(
        'drive_item_rename' if res else 'drive_item_rename_error',
        'notification-success' if res else 'notification-danger'
    )
    return redirect(url_for('drive.storage', drive=drive, path=path))

@drive.route('/duplicate/<drive>/<path:path>/')
@login_required
@check_drive
def duplicate(drive, path):
    base_path = 'shared' if drive == 'shared' else str(current_user.uuid)

    path = path.split('/')
    path, item_name = '/'.join(path[:-1]), path[-1]

    file_handling.duplicate(base_path, path, item_name)

    flash('drive_item_duplication', 'notification-success')
    return redirect(url_for('drive.storage', drive=drive, path=path))

@drive.route('/move/<drive>/', defaults={'path': ''}, methods=['POST'])
@drive.route('/move/<drive>/<path:path>/', methods=['POST'])
@login_required
@check_drive
def move(drive, path):
    base_path = 'shared' if drive == 'shared' else str(current_user.uuid)

    item_name = request.form.get('item-name')
    destination_folder = request.form.get('destination-folder')

    if item_name == destination_folder:
        flash('drive_item_move_same_folder', 'notification-danger')
    
    else:
        if destination_folder == '__parent__':
            destination_folder = '../'
        
        res = file_handling.move(base_path, path, item_name, destination_folder, str(current_user.uuid))
        flash(
            'drive_item_move' if res else 'drive_item_move_error',
            'notification-success' if res else 'notification-danger'
        )

    return redirect(url_for('drive.storage', drive=drive, path=path))

@drive.route('/download/<drive>', defaults={'path': ''})
@drive.route('/download/<drive>/<path:path>')
@login_required
@check_drive
def download(drive, path):
    base_path = 'shared' if drive == 'shared' else str(current_user.uuid)
    
    path = path.strip('/').split('/')
    path, name = '/'.join(path[:-1]), path[-1]

    res = file_handling.download(base_path, path, name)
    if res is None:
        flash('drive_item_download', 'notification-danger')
        return redirect(url_for('drive.storage', drive=drive, path=path))

    resp_file, download_name = res
    return send_file(resp_file, download_name=download_name)