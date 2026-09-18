from os import environ

from dotenv import load_dotenv

load_dotenv()

MONGO_URI = environ["MONGO_URI"]
DB_NAME = environ["DB_NAME"]
DEFAULT_BUCKET = {"size": 10, "rps": 1, "tokens": 10}
