from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8002
    database_url: str = "postgresql:///votes"
    salt: str = "7836a9d681642faa5dfff6bcef5809ad3338eb35220b475942e76cf551c091df"


setting = Settings()
