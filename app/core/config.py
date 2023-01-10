from pydantic import BaseSettings


class Settings(BaseSettings):

    app_title: str = 'Благотворительный проект QR-кот'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'very_secret_key_555'

    class Config:
        env_file = '.env'


settings = Settings()
