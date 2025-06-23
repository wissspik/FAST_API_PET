import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from pytest_asyncio import pytest_asyncio
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_async_engine(TEST_DATABASE_URL,echo=True)

new_session = async_sessionmaker(engine,expire_on_commit= False)

@pytest_asyncio.fixture
async def get_session():
    async with new_session() as session:
        yield session
