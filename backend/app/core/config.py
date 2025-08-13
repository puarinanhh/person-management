from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = "mysql://root:123456@localhost:3306/dashboard?charset=utf8mb4"
    JWT_SECRET: str = "supersecret"

settings = Settings()