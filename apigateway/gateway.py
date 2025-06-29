import os
from fastapi import FastAPI
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

app = FastAPI()

