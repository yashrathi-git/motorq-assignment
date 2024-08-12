from pymongo import MongoClient
from motorq.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from motorq.models import Base



engine = create_async_engine(
    settings.assemble_db_connection(),
    pool_pre_ping=True,
)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

mongo_client = MongoClient(settings.mongo_db_uri, connect=True)

mongo_database = mongo_client[settings.mongo_db_name]


motor_client = AsyncIOMotorClient(settings.mongo_db_uri)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
