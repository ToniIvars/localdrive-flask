from pathlib import Path

from .config import config

def create_user_directory(username: str) -> None:
    path_to_create = Path(config.localdrive_storage_path) / username
    path_to_create.mkdir(exist_ok=True)