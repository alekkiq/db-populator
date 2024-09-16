from helpers.populate_database import populate_database
from helpers.mysql_helpers import create_database, db_connection
from config import config # Will work after setup.sh is ran.

# Create databases and tables for each database in the config file
if __name__ == "__main__":
    configs = config()
    connection_params = configs["connection_params"]
    databases = configs["databases"]

    try:
        print(f"Configs loaded:\n{connection_params}\n\n")
        print(f"Databases to be created:\n{", ".join(databases.keys())}\n")
        for db_name, database in databases.items():
            db = db_connection(connection_params)
            cursor = db.cursor()
            create_database(cursor, db_name, True)
            
            for table_name, table in database["tables"].items():
                db_populated = populate_database(
                    cursor = cursor,
                    db_name = db_name, 
                    data_file = table["data_file"], 
                    file_type = configs["data_format"],
                    data_types = table["data_types"], 
                    table_name = table_name
                )
                db.commit()
            
            cursor.close()
            db.close()
            
            print(f"'{db_name}' setup completed with {db_populated['error_count']} errors.\n")
    except Exception as error:
        print(f"An error occurred while trying to populate the database. Error:\n{error}")
