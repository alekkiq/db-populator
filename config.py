from dotenv import load_dotenv
import os

def config() -> dict:
    # Load configs from .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

    return {
        "connection_params": {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "username": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "collation": "utf8mb4_unicode_ci",
            "autocommit": False,
        },
        "chunksize": 500, # The number of rows inserted simultaneously in the DB
        "data_format": "json", # "csv" | "json" | "xml"
        "databases": {
            # Your databases & tables go here!
            "countries": {
                "tables": {
                    "country": {
                        "data_file": "countries.json",
                        "data_types": {
                            "id": "INT PRIMARY KEY",
                            "code": "VARCHAR(2)",
                            "name": "VARCHAR(255)",
                            "continent": "VARCHAR(2)",
                            "wikipedia_link": "VARCHAR(255)",
                            "keywords": "VARCHAR(255)"
                        }
                    }
                }
            }
        }
    }