from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import BaseSettings, SettingsConfigDict
from typing import ClassVar


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: ClassVar[str] = "localhost"
    REDIS_PORT: ClassVar[int] = 6379
    REDIS_URL: str = "redis://localhost:6379/0"
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    # USE_CREDENTIALS: bool = True
    # VALIDATE_CERTS: bool = True
    FRONTEND_URL: ClassVar[str]="http://localhost:3000"
    DOMAIN: str
    TEMPLATE_FOLDER: ClassVar[str] = r"/home/ssa/Desktop/fastapi_homs_be/app/lib/templates"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
 

Config = Settings() 


# broker_url = Config.REDIS_URL
# result_backend = Config.REDIS_URL
# broker_connection_retry_on_startup = True

# /home/ssa/Desktop/fastapi_homs_be/app/lib/templates/welcome_email.html