# The DB action file

# Data type helpers:
from .csv_helpers import get_csv_headers, get_csv_data
from .json_helpers import get_json_headers, get_json_data
from .xml_helpers import get_xml_data

# Other helpers & config
from .get_file_path import get_file_path
from .mysql_helpers import *
from config import config # Will work after setup.sh is ran.

def populate_database(db_name: str, data_file: str, data_types: dict, table_name: str, file_type: str = "csv"):
    '''
    Fills the given database name with data in the *data_file* CSV file.
    '''
    configs = config()
    
    # get the database configuration from a config file
    connection_params = configs["connection_params"]
    
    try:
        # initialize the connection and create the database
        db = db_connection(connection_params)
        cursor = db.cursor()
        create_database(cursor, db_name)
        
        file_path = get_file_path(data_file)
        data_chunksize = configs["chunksize"]
        
        # to the correct actions based on the file type
        match file_type:
            case "csv":
                data = get_csv_data(csv_file = file_path, chunksize = data_chunksize)
            case "json":
                data = get_json_data(json_file = file_path, chunksize = data_chunksize)
            case "xml":
                data = get_xml_data(xml_file = file_path, database_name = db_name, table_name = table_name, chunksize = data_chunksize)
            case _:
                print(f"File type '{file_type}' not supported (yet)")
                return False
        
        # Get the column names from the config file
        column_names = configs["databases"][db_name]["tables"][table_name]["data_types"].keys()
        
        # create the table with the correct column names / data types
        create_table(cursor, table_name, column_names, data_types)
        
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