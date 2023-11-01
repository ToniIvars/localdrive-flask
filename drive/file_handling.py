import os
import shutil
from io import BytesIO
from pathlib import Path
from uuid import UUID
from zipfile import ZipFile

from .config import config

def create_user_directory(uuid: UUID) -> None:
    path_to_create = Path(config.localdrive_storage_path) / str(uuid)
    path_to_create.mkdir(exist_ok=True)

def list_dir(base_path:  str, path: str) -> None | list:
    directory = Path(config.localdrive_storage_path) / base_path / path

    if not directory.exists():
        return

    content = []
    for item in directory.iterdir():
        content.append({
            'name': item.name,
            'type': 'folder' if item.is_dir() else 'file',
        })
    
    content.sort(key=lambda d: (['folder', 'file'].index(d['type']), d['name']))
    return content

def save_file(base_path: str, f, name: str, path: str) -> None:
    directory = Path(config.localdrive_storage_path) / base_path / path
    file_path = directory / name
    f.save(str(file_path))

def create_dir(base_path: str, path: str, name: str) -> bool:
    directory = Path(config.localdrive_storage_path) / base_path / path
    dir_path = directory / name
    if dir_path.exists():
        return False
    
    dir_path.mkdir()
    return True

def delete(base_path: str, path: str, name: str) -> bool:
    directory = Path(config.localdrive_storage_path) / base_path / path
    item_path = directory / name

    if not item_path.exists():
        return False
    
    if item_path.is_dir():
        shutil.rmtree(item_path)

    else:
        item_path.unlink()

    return True 

def rename(base_path: str, path: str, name: str, new_name: str) -> bool:
    directory = Path(config.localdrive_storage_path) / base_path / path
    
    old_path = directory / name
    new_path = directory / new_name

    if not old_path.exists() or new_path.exists():
        return False
    
    old_path.rename(new_path)
    return True

def duplicate(base_path: str, path: str, name: str) -> None:
    directory = Path(config.localdrive_storage_path) / base_path / path
    item_name = directory / name

    i = 1
    while True:
        duplicate_name = directory / f'{name} ({i})'
        if not duplicate_name.exists():
            copy_func = shutil.copytree if item_name.is_dir() else shutil.copy2
            copy_func(item_name, duplicate_name)
            return
        
        i += 1

def move(base_path: str, path: str, name: str, destination_folder: str, uuid: str) -> bool:
    directory = Path(config.localdrive_storage_path) / base_path / path
    
    item_name = directory / name
    if destination_folder == 'shared':
        dest_path = Path(config.localdrive_storage_path) / 'shared' / name
    
    elif destination_folder == 'my-drive':
        dest_path = Path(config.localdrive_storage_path) / uuid / name

    else:
        dest_path = directory / destination_folder / name

    if not dest_path.parent.exists() or dest_path.exists():
        return False
    
    shutil.move(item_name, dest_path)
    return True

def zip_dir(path: Path) -> BytesIO:
    zip_file = BytesIO()

    with ZipFile(zip_file, 'w') as buffer:
        for root, _, files in os.walk(path):
            for f in files:
                buffer.write(os.path.join(root, f), arcname=f'{root.replace(str(path), path.name)}/{f}')
    
    zip_file.seek(0)
    return zip_file

def download(base_path: str, path: str, name: str) -> tuple[str | BytesIO, str] | None:
    directory = Path(config.localdrive_storage_path) / base_path / path
    item_name = directory / name

    if not item_name.exists():
        return
    
    if item_name.is_file():
        return item_name, name
    
    return zip_dir(item_name), f'{name}.zip'