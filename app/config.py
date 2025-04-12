from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    db_url: str
    secret_key: str
    base_url: str
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    model_config = SettingsConfigDict(env_file=".env")
    allowed_origins: str

settings = Settings()
