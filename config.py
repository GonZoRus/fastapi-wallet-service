import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

required_env = {'DB_USER': DB_USER,
                'DB_PASSWORD': DB_PASSWORD,
                'DB_HOST': DB_HOST,
                'DB_PORT': DB_PORT,
                'DB_NAME': DB_NAME
                }

for env_key, env_value in required_env.items():
	if env_value is None:
		logger.critical(f'Не задана переменная окружения: {env_key}')
		raise RuntimeError(f"Не задана переменная окружения: {env_key}")
