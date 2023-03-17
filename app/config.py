import os
import logging
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class DefaultConfig:
    """
    Required env variables for Render: TELEGRAM_TOKEN, WEBHOOK_URL, WEBAPP_HOST.
    Required env variables for Railway: TELEGRAM_TOKEN, WEBHOOK_URL.
    """
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
    MODE = os.environ.get("MODE", "")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    # Webhook settings
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")
    WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH", "")
    WEBAPP_HOST = os.environ.get("WEBAPP_HOST", "0.0.0.0")
    WEBAPP_PORT = int(os.environ.get("PORT", 5000))

    @staticmethod
    def init_logging():
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=DefaultConfig.LOG_LEVEL,
        )
