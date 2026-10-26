import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        if not self.secret_key:
            raise ValueError("SECRET_KEY is not set")
        if not self.database_url:
            raise ValueError("DATABASE_URL is not set")


settings = Settings()    