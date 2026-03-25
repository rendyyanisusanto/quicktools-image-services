from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_PORT: int = 8002
    MAX_FILE_SIZE_MB: int = 20
    STORAGE_INPUT_DIR: str = "storage/input"
    STORAGE_OUTPUT_DIR: str = "storage/output"

    class Config:
        env_file = ".env"

settings = Settings()
