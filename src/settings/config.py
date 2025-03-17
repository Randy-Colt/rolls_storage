from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_DIR: Path = Path(__file__).resolve().parent.parent.parent
    model_config = SettingsConfigDict(env_file=PROJECT_DIR / 'example.env')

    debug: bool = False
    postgres_user: str = 'user'
    postgres_password: str = 'password'
    db_host: str = 'localhost'
    db_port: str = '5432'
    postgres_db: str = 'db'
    sqlite: bool = True

    @property
    def db_url(self) -> str:
        if self.sqlite:
            return 'sqlite+aiosqlite:///../db.sqlite3'
        return (
                f'postgresql+asyncpg://{self.postgres_user}:'
                f'{self.posthres_password}@{self.db_host}:{self.db_port}'
                f'/{self.postgres_db}'
            )


settings = Settings()
