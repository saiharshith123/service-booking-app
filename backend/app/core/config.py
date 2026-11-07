from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:admin@localhost:5432/service_booking"
    secret_key: str = "njdux_UGFjG07oZSmdl6r8EDg5c29rXtWS6BVHfpoBHKOGSJirGdhYJ5w4mSfVWQBE5t8BZJAkc2iR6awHNvYg"
    access_token_expire_minutes: int = 60
    frontend_origin: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
