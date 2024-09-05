from helpers.populate_database import populate_database
from config import config # Will work after setup.sh is ran.

# Create databases and tables for each database in the config file
if __name__ == "__main__":
    configs = config()

    try:
        print(f"Configs loaded:\n{configs}\n\n")
        for db_name, database in configs["databases"].items():
            for table_name, table in database["tables"].items():
                populate_database(
                    db_name = db_name, 
                    data_file = table["data_file"], 
                    file_type = configs["data_format"],
                    data_types = table["data_types"], 
                    table_name = table_name
                )
    except Exception as error:
        print(f"An error occurred while trying to populate the database.\nError:\n{error}")
