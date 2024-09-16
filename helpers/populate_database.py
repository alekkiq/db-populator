# The DB action file

# Data type helpers:
import mysql.connector.cursor
from .csv_helpers import get_csv_headers, get_csv_data
from .json_helpers import get_json_headers, get_json_data
from .xml_helpers import get_xml_data

# Other helpers & config
from .get_file_path import get_file_path
from .mysql_helpers import *
from config import config # Will work after setup.sh is ran.

def populate_database(connection: mysql.connector.connection.MySQLConnection, db_name: str, data_file: str, data_types: dict, table_name: str, file_type: str = "csv"):
    '''
    Fills the given database name with data in the *data_file* CSV file.
    '''
    configs = config()

    success = False

    try:
        cursor = connection.cursor()

        file_path = get_file_path(data_file)
        data_chunksize = configs["chunksize"]
        
        # to the correct actions based on the file type
        if file_path != "": # file was found
            match file_type:
                case "csv":
                    data = get_csv_data(csv_file = file_path, chunksize = data_chunksize)
                case "json":
                    data = get_json_data(json_file = file_path, chunksize = data_chunksize)
                case "xml":
                    data = get_xml_data(xml_file = file_path, database_name = db_name, table_name = table_name, chunksize = data_chunksize)
                case _:
                    data = []
        else:
            data = []
        
        # Get the column names from the config file
        column_names = configs["databases"][db_name]["tables"][table_name]["data_types"].keys()
        
        # create the table with the correct column names / data types
        table_created = create_table(cursor, table_name, column_names, data_types)
        table_relationships = configs["databases"][db_name]["tables"][table_name].get("relationships", None)
        
        data_inserted = insert_data_to_table(connection, table_name, data, column_names)
        
        # set up the foreign key relationships
        relationships_setup = {}

        if table_relationships:
            for relationship in table_relationships:
                relationships_setup = setup_table_relationship(cursor, table_name, relationship["foreign_key"], relationship["reference_table"], relationship["reference_column"], relationship.get("constraint_name", None))

        success = True
    except Exception as error:
        success = False
        print(f"An error occurred while trying to populate the database.\nError:\n{error}")
    finally:
        cursor.close()

        # check for errors in each action
        errors = check_errors({
            "table_created": table_created,
            "data_inserted": data_inserted,
            "relationships_setup": relationships_setup,
        })

        return {
            "success": success,
            "error_count": errors,
        }
    
def check_errors(results: dict):
    '''
    Checks the results of the database setup and returns a boolean indicating if there were any errors.
    '''
    errors = 0
    for result in results.values():
        if result is None or result == {}: continue
        if not result["success"]:
            errors += 1
    return errors
