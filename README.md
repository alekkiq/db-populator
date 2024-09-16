# Python MariaDB database populator

## Table of Contents
1. [About](#about)
2. [Features](#features)
3. [System requirements](#requirements)
4. [Getting started](#getting-started)
5. [Data format examples](#data-examples)
6. [TO-DOS](#to-dos)

## About
A quite simple database populator built with Python. Works with **MariaDB** databases.

***IMPORTANT***: This script is ***NOT*** suited for production use, as it is ***NOT*** designed to have a safe way of storing database credidentials! DO NOT USE IT IN PRODUCTION APP!

## Features
- Supports bulk data insertion from the 3 common data file formats.
- Capable of creating & populating multiple databases on one execution.
- Configurable chunk size for data insertion.
- Proper error handling.
- Easy to setup via a shell script.

## Requirements

- **Python** >= v. 3.12.x
- **MariaDB** >= v. 11.5

And the following external Python packages:

- **pandas**
- **mysql-connector-python**
- **xmltodict** (for handling XML files)

**Note**: These packages will be installed if you follow the Getting started guide.

## Getting started

1. Copy the entire repository into your local instance.
2. Run the setup script in Git Bash or any similar command line interface (Windows CMD wont work by default!) from the root of the project with:

    ```bash
    sh setup.sh
    ```
3. Run this command to download the needed python packages:

    ```bash
    pip install mysql-connector-python pandas xmltodict
    ```
4. Put your ready data file(s) in the ```data/``` directory. Each file should represent a *single* MySQL table. See [data format examples](#data-examples) for the programs "norm" of each data format.
5. Define the databases-part of your configurations:
    - Add your database(s) and table(s) to the ```config.py``` file like so:
    
        ```python
        ...
        "databases": { # <-- This level is already in the base config
            "your_database_name": {
                "tables": {
                    "your_table_name": {
                        "data_file": "table_data_file.csv",
                        "data_types": {
                            # A key represents a table column name
                            # and the value is the proper data
                            # type for MySQL.

                            # IMPORTANT: Make sure the keys are the same as 
                            # in your data file!
                            "column_name": "valid_mysql_data_type"

                            # For example:
                            "id": "INT PRIMARY KEY",
                            "name": "VARCHAR(255)",
                            ... # and so on.
                        },
                        # To declare table relationships, 
                        # use the following structure:
                        "relationships": {
                            {
                                "reference_table": "referenced_table_name",
                                "reference_column": "referenced_column_name",
                                "foreign_key": "foreign_key_in_table",
                                "constraint_name": "your_constraint_name"
                            },
                            ...
                            # You can set up multiple relationships
                            # to a table in this manner.
                        }
                    }
                }
            }
        }
        ```

        **FYI**: the program runs through each database in ```"databases"``` and creates that database. It then loops through the ```"tables"``` and creates the tables under the database and finally populates that table with the data in ```"data_file"```
6. Run the ```main.py``` file and the database(s) should be set to go!

## Data examples

Since the script supports CSV, JSON and XML data formats, there are some "guidelines" on each of them (mainly XML).

- **CSV EXAMPLE**:

    ```csv
    "id","firstname","lastname","email","phone_number","description"
    "1","John","Doe","john.doe@localhost","1234567890","My name is John Doe! I'm a software engineer."
    "2","Jane","Doe","jane.doe@localhost","0987654321",
    ```

- **JSON EXAMPLE**:

    ```json
    [
        {
            "id": 1,
            "firstname": "John",
            "lastname": "Doe",
            "email": "john.doe@localhost",
            "phone_number": "1234567890",
            "description": "My name is John Doe! I'm a software engineer."
        },
        {
            "id": 2,
            "firstname": "Jane",
            "lastname": "Doe",
            "email": "jane.doe@localhost",
            "phone_number": "0987654321",
            "description": ""
        }
    ]
    ```

- **XML EXAMPLE**:

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>

    <people>                <!-- <- Database name -->
        <person>            <!-- <- Table name -->
            <id>1</id>
            <firstname>John</firstname>
            <lastname>Doe</lastname>
            <email>john.doe@localhost</email>
            <phone_number>1234567890</phone_number>
            <description>My name is John Doe! I'm a software engineer.</description>
        </person>
        <person>
            <id>2</id>
            <firstname>Jane</firstname>
            <lastname>Doe</lastname>
            <email>jane.doe@localhost</email>
            <phone_number>0987654321</phone_number>
            <description></description>
        </person>
    </people>
    ```

## TO-DOS
- Add support for table relationships.
