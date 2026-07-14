from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Settings:
    APP_NAME = "Supply Chain Risk Intelligence API"
    APP_VERSION = "1.0.0"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./supply_chain.db"
    )

settings = Settings()