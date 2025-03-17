from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_DIR: Path = Path(__file__).resolve().parent.parent.parent
    model_config = SettingsConfigDict(env_file=PROJECT_DIR / 'example.env')

    debug: bool = False
    directory: str = './'
    db_name: str = 'db.sqlite3'
    db_url: str = f'sqlite+aiosqlite:///{directory}{db_name}'


settings = Settings()
