import mysql.connector
import pandas as pd
import numpy as np

def db_connection(connection_params: dict = {...}):
    '''
    Established a connection to a MySQL (mariadb) database with given parameters and returns the connection
    '''
    db = mysql.connector.connect(
        host = connection_params["host"],
        user = connection_params["username"],
        password = connection_params["password"], # top tier, hiring applications accepted
        collation = connection_params["collation"], # fixes some weeeird issues with mysql connector
        autocommit = connection_params["autocommit"],
    )

    return db

def create_database(cursor: mysql.connector.cursor.MySQLCursor, database_name: str, drop_existing: bool = False):
    '''
    Creates an empty database and sets it as the active database
    '''
    print(f"Creating database '{database_name}'...")
    
    try:
        if drop_existing:
            cursor.execute(f"DROP DATABASE IF EXISTS {database_name};")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};"),
        cursor.execute(f"ALTER DATABASE {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"), # very important!
        cursor.execute(f"USE {database_name};")
        
        print(f"Successfully created database {database_name}\n")
    except Exception as error:
        print(f"An error occurred while creating database '{database_name}'.\nError:\n{error}")

def create_table(connection: mysql.connector.cursor.MySQLCursor, table_name: str, column_names: list = [], column_data_types: dict = {}):
    '''
    Creates a table in the *connection* database with the given column names and data types
    '''
    print(f"Creating table '{table_name}'...")
    
    create_table_statement = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    
    for column in column_names:
        column_definition = f"{column} {column_data_types.get(column, 'VARCHAR(255)')},\n"
        create_table_statement += column_definition
        
    try:
        connection.execute(create_table_statement.rstrip(",\n") + "\n);")
        
        print(f"Successfully created table '{table_name}'\n")
    except Exception as error:
        print(f"An error occurred while trying to create table '{table_name}'\nError:\n{error}")
        
def insert_data_to_table(connection: mysql.connector.cursor.MySQLCursor, table_name: str, data: list, column_names: list):
    '''
    Inserts data into the given database table in sized chunks. The function expects, that the connection is already connected to a database
    '''
    print(f"Populating '{table_name}'...")

    if not data or len(data[0]) == 0:
        print(f"No data to insert into table '{table_name}'\n Continuing...\n")
        return
    
    column_names_stringified = ",".join(column_names)
    placeholders = ",".join("%s" for _ in column_names)
    insert_data_statement = f"INSERT INTO {table_name} ({column_names_stringified}) VALUES \n"
    
    try:
        for chunk in data:
            chunk_values = []
            placeholders_list = []
            
            for row in chunk:
                row = [convert_data_type(item) for item in row]
                placeholders_list.append(f"({placeholders})")
                chunk_values.extend(row)
                
            final_statement = insert_data_statement + ",".join(placeholders_list)
            
            connection.execute(final_statement, chunk_values)
        
        print(f"Successfully populated table '{table_name}'\n")
    except mysql.connector.Error as error:
        print(f"An error occurred while trying to populate table '{table_name}'\nError:\n{format(error)}")

def setup_table_relationship(connection: mysql.connector.cursor.MySQLCursor, table_name: str, foreign_key: str, reference_table: str, reference_column: str, constraint_name: str = None):
    '''
    Sets up a foreign key relationship between the given table and the reference table
    '''
    print(f"Setting up foreign key relationship for table '{table_name}'...")
    
    if constraint_name is None:
        constraint_name = f"fk_{table_name}_{foreign_key}_{reference_table}_{reference_column}"
    
    try:
        # Check if the referenced column exists and is indexed
        connection.execute(f"SHOW INDEX FROM {reference_table} WHERE Column_name = '{reference_column}';")
        index_result = connection.fetchall()
        
        if not index_result:
            print(f"Referenced column '{reference_column}' in table '{reference_table}' is not indexed. Creating index...")
            connection.execute(f"CREATE INDEX idx_{reference_column} ON {reference_table}({reference_column});")
            print(f"Index on column '{reference_column}' in table '{reference_table}' created successfully.")

        # Check if the data types match
        connection.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{foreign_key}';")
        foreign_key_column = connection.fetchone()
        connection.execute(f"SHOW COLUMNS FROM {reference_table} LIKE '{reference_column}';")
        reference_column_info = connection.fetchone()

        if foreign_key_column[1] != reference_column_info[1]:
            print(f"Data type mismatch between '{foreign_key}' in '{table_name}' and '{reference_column}' in '{reference_table}'. Adjusting data type...")
            connection.execute(f"ALTER TABLE {table_name} MODIFY {foreign_key} {reference_column_info[1]};")
            print(f"Data type of column '{foreign_key}' in table '{table_name}' adjusted to match '{reference_column}' in '{reference_table}'.")

        # Add the foreign key constraint
        connection.execute(f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} FOREIGN KEY ({foreign_key}) REFERENCES {reference_table}({reference_column});")
        
        print(f"Successfully set up foreign key relationship for table '{table_name}'\n")
    except mysql.connector.Error as error:
        print(f"An error occurred while trying to set up foreign key relationship for table '{table_name}'\nError:\n{format(error)}")

def convert_data_type(item):
    '''
    Converts numpy data types to native Python data types.
    '''
    if isinstance(item, (np.int64, np.int32)):
        return int(item)
    elif isinstance(item, (np.float64, np.float32)):
        return float(item)
    elif pd.isna(item):
        return None
    return item

def insert_data_from_csv(connection: mysql.connector.cursor.MySQLCursor, table_name: str, csv_file_path: str, chunk_size: int = 1000):
    '''
    Reads data from a CSV file and inserts it into the given database table in sized chunks.
    '''
    df = pd.read_csv(csv_file_path)
    column_names = df.columns.tolist()
    data = df.values.tolist()
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    insert_data_to_table(connection, table_name, chunks, column_names)