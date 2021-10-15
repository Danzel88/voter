from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8002
    database_url: str = "postgresql:///votes"
    jwt_secret: str = "VVarz11XLJZ89pECv74NJb6WDi9Z5j13d2xSiwmWB_Q"
    jwt_expires_s = 3600
    jwt_algorithms = "HS256"

setting = Settings()
