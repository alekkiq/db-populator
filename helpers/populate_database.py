# The main file# import all helper functions
from .csv_helpers import *
from .mysql_helpers import *
from config import config

configs = config()

def populate_database(db_name: str, data_file: str, data_types: dict, table_name: str):
    '''
    Fills the given database name with data in the *data_file* CSV file.
    '''
    # get the database configuration from a config file
    connection_params = configs["connection_params"]
    
    try:
        # initialize the connection and create the database
        db = db_connection(connection_params)
        cursor = db.cursor()
        create_database(cursor, db_name)
        
        # get the necessary things from the csv
        file_path = get_file_path(data_file)
        column_names = get_csv_headers(file_path)
        
        # create the table with the correct column names / data types
        create_table(cursor, table_name, column_names, data_types)
        
        # continue to inserting the data itself.
        data_chunksize = configs["chunksize"]
        data = get_csv_data(file_path, data_chunksize)
        insert_data_to_table(cursor, table_name, data, column_names)
        db.commit()
        
        # close the cursor & the database when ready
        cursor.close()
        db.close()

        print("Database setup successfully!")
        return True
    except Exception as error:
        print(f"An error occurred while trying to populate the database.\nError:\n{error}")
        return False