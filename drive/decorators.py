from functools import wraps
from flask import flash, redirect, url_for, request

def check_drive(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if request.view_args.get('drive') not in ('shared', 'my-drive'):
            flash('drive_path_not_found', 'notification-danger')
            return redirect(url_for('drive.index'))
        
        return func(*args, **kwargs)
    
    return decorated_function