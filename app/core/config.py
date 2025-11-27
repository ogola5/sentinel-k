from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str

    redis_host: str
    redis_port: int
    redis_user: str
    redis_password: str
    redis_use_ssl: bool  # add this

    app_secret_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
