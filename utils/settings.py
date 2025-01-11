import os
import logging
from dotenv import load_dotenv

load_dotenv()


PG_DSL = {'dbname': os.environ.get('DB_NAME'), 'user': os.environ.get('DB_USER'),
          'password': os.environ.get('DB_PASSWORD'),
          'host': os.environ.get('DB_HOST'), 'port': os.environ.get('DB_PORT')}



format = "%(levelname)s  %(asctime)s:  %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

logger = logging.getLogger()