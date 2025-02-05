import asyncio
import logging
from datetime import datetime
from functools import lru_cache

from mongoengine import connect
from pydantic_settings import BaseSettings

loop = asyncio.get_event_loop()

class Settings(BaseSettings):
    DATABASE_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_BUCKET_NAME: str

    class Config:
        env_file = ".env.dev"

@lru_cache()
def get_settings():
    return Settings()

async def initiate_database():
    client = connect(host=Settings().DATABASE_URL)
    return client

# Configure logging
logging.basicConfig(
    filename=f'logs/log_{datetime.now().strftime("%Y-%m-%d")}.log',
    level=logging.INFO,  # Set the logging level according to your needs
    format="%(levelname)s - %(message)s - Line %(lineno)d - %(asctime)s",
)

# Define a logger for your FastAPI app
logger = logging.getLogger(__name__)
