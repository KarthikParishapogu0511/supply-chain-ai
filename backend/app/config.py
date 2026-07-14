from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class Settings:
    APP_NAME = "Supply Chain Risk Intelligence API"
    APP_VERSION = "1.0.0"

    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        DATABASE_URL = "sqlite:///./supply_chain.db"

    DB_ECHO = os.getenv("DB_ECHO", "false").lower() in {"1", "true", "yes", "on"}


settings = Settings()