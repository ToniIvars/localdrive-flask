from pathlib import Path
from os import environ

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / '.env')

CONFIG = {k.lstrip('LOCALDRIVE_'): v for k, v in environ.items() if k.startswith('LOCALDRIVE_')}