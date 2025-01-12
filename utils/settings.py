import os
import logging
import bcrypt
from dotenv import load_dotenv

load_dotenv()

PG_DSL = {'dbname': os.environ.get('DB_NAME'), 'user': os.environ.get('DB_USER'),
          'password': os.environ.get('DB_PASSWORD'),
          'host': os.environ.get('DB_HOST'), 'port': os.environ.get('DB_PORT')}

APP_SALT = os.environ.get('APP_SALT')

format = "%(levelname)s  %(asctime)s:  %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

logger = logging.getLogger()


def hash_bcr(data: str) -> bytes:
    return bcrypt.hashpw(bytes(data, 'UTF-8'), bytes(APP_SALT, 'UTF-8'))
