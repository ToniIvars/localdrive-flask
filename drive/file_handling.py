from pathlib import Path
from uuid import UUID

from .config import config

def create_user_directory(uuid: UUID) -> None:
    path_to_create = Path(config.localdrive_storage_path) / str(uuid)
    path_to_create.mkdir(exist_ok=True)