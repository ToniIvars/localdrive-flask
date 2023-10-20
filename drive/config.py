from dotenv import load_dotenv
load_dotenv()

from envclasses import EnvClassMeta

class Config(metaclass=EnvClassMeta):
    localdrive_secret_key: str
    localdrive_sqlalchemy_database_uri: str
    localdrive_storage_path: str

    def to_flask_config(self):
        return {k.upper().lstrip('LOCALDRIVE_'): v for k, v in self.__dict__.items()}

config = Config()