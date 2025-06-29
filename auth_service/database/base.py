from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from typing import Annotated
from fastapi.params import Depends
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_async_engine(DATABASE_URL,echo=True)

new_session = async_sessionmaker(engine,expire_on_commit= False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession,Depends(get_session)]