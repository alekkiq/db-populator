from helpers.populate_database import populate_database
from helpers.mysql_helpers import create_database, db_connection
from config import config # Will work after setup.sh is ran.

# Create databases and tables for each database in the config file
if __name__ == "__main__":
    configs = config()
    connection_params = configs["connection_params"]

    try:
        print(f"Configs loaded:\n{configs}\n\n")
        for db_name, database in configs["databases"].items():
            db = db_connection(connection_params)
            cursor = db.cursor()
            create_database(cursor, db_name)
            
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
