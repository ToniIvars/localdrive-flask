from pathlib import Path
from uuid import UUID

from .config import config

def create_user_directory(uuid: UUID) -> None:
    path_to_create = Path(config.localdrive_storage_path) / str(uuid)
    path_to_create.mkdir(exist_ok=True)

def list_dir(uuid:  str, path: str) -> None:
    directory = Path(config.localdrive_storage_path) / uuid / path

    if not directory.exists():
        return

    content = []
    for item in directory.iterdir():
        content.append({
            'name': item.name,
            'type': 'folder' if item.is_dir() else 'file',
        })

    return content