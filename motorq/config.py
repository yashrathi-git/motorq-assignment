from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()
class Settings(BaseSettings):

    mongo_db_uri: str = os.getenv("MONGO_DB_URI")
    mongo_db_name: str = os.getenv("MONGO_DB_NAME")

    def assemble_db_connection(self, sync: bool = False):
        scheme = "postgresql+asyncpg" if not sync else "postgresql"
        pg_db = f"{os.getenv('POSTGRES_DB') or ''}"
        path = PostgresDsn.build(
            scheme=scheme,
            username=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_SERVER"),
            path=pg_db,
        )
        print(path)
        return f"{path}"




settings = Settings()
