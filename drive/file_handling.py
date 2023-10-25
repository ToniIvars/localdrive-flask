from pathlib import Path
from shutil import rmtree
from uuid import UUID

from .config import config

def create_user_directory(uuid: UUID) -> None:
    path_to_create = Path(config.localdrive_storage_path) / str(uuid)
    path_to_create.mkdir(exist_ok=True)

def list_dir(base_path:  str, path: str) -> None:
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

def delete(base_path: str, path: str, name: str) -> None:
    directory = Path(config.localdrive_storage_path) / base_path / path
    item_path = directory / name

    if item_path.exists():
        if item_path.is_dir():
            rmtree(item_path)

        else:
            item_path.unlink()

def rename(base_path: str, path: str, name: str, new_name: str) -> None:
    directory = Path(config.localdrive_storage_path) / base_path / path
    
    old_path = directory / name
    new_path = directory / new_name

    if old_path.exists():
        old_path.rename(new_path)