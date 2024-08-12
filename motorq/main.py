from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from motorq.db import mongo_database, create_tables
# from motorq.deps import get_db

from motorq.api import organization_router, vehicle_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb = mongo_database
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(organization_router)
app.include_router(vehicle_router)

