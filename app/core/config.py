from pydantic import BaseSettings


class Settings(BaseSettings):

    app_title: str
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str

    class Config:
        env_file = '.env'


settings = Settings()
