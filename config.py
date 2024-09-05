from dotenv import load_dotenv
import os

def config() -> dict:
    # Load configs from .env file
    load_dotenv(os.abspath(os.path.join(os.path.dirname(__file__), ".env")))

    return {
        "connection_params": {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "username": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "collation": "utf8mb4_unicode_ci",
            "autocommit": False,
            "csv_chuksize": 500 # Adjust as needed. Recommended 500 - 2500.
        },
        "databases": {
            # Your databases & tables go here!
        }
    }