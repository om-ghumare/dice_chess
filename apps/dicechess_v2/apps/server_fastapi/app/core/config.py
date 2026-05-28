from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "dicechess-server"
    app_version: str = "0.1.0"
    jwt_secret: str = "dev-only-change-me"
    enable_google_auth: bool = True


settings = Settings()
