from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_DIR: Path = Path(__file__).resolve().parent.parent.parent
    model_config = SettingsConfigDict(env_file=PROJECT_DIR / '.env')

    debug: bool = False
    db_user: str = 'user'
    db_password: str = 'password'
    db_host: str = 'localhost'
    db_port: str = '5432'
    db_name: str = 'db'
    db_type: str = 'sqlite'

    @property
    def db_url(self) -> str:
        if self.db_type == 'postgresql':
            return (
                f'{self.db_type}+asyncpg://{self.db_user}:{self.db_password}@'
                f'{self.db_host}:{self.db_port}/{self.db_name}'
            )
        return 'sqlite+aiosqlite:///../db.sqlite3'


settings = Settings()
