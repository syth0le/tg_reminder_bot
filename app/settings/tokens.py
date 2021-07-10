import os

from dotenv import load_dotenv

load_dotenv(override=True)

API_TOKEN = os.getenv("API_TOKEN")
ACCESS_ID = os.getenv("ACCESS_ID")
