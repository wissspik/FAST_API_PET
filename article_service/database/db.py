import os

import motor.motor_asyncio
from dotenv import load_dotenv
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]

