# Python MariaDB database populator from CSV

## Table of Contents
1. [About](#about)
2. [Features](#features)
3. [System requirements](#requirements)
4. [Getting started](#getting-started)
5. [TO-DOS](#to-dos)

## About
A quite simple database populator built with Python. Works with **MariaDB** databases.

## Features
- Supports bulk data insertion from CSV files.
- Capable of creating & populating multiple databases on one execution.
- Configurable chunk size for data insertion.
- Proper error handling.

## Requirements

**Python** >= v. 3.12.x <br>
**MariaDB** >= v. 11.5

And the following external Python packages:

**pandas** <br>
**mysql-connector-python**

**Note**: These packages will be installed if you follow the Getting started guide.

## Getting started

1. Copy the entire repository into your local instance.
2. Run this command to download the needed packages:

    ```bash
    pip install mysql-connector-python pandas
    ```
3. Put your ready **CSV** (.csv) file(s) in the ```data/``` directory. Each csv file should represent a single MySQL table.
4. Setup your configurations:
    - Create an ```.env``` file in the project root based on ```.env.example``` and add your proper database connection values.
    - Add your database(s) and table(s) to the ```config.py``` file like so:
    
        ```python
        ...
        "databases": { # <-- Already in the base config
            "your_database_name": {
                "tables": {
                    "your_table_name": {
                        "data_file": "table_data_file.csv",
                        "data_types": {
                            # A key represents a CSV column name
                            # and the value is the proper data
                            # type for MySQL
                            "csv_column": "valid_mysql_data_type"

                            # For example:
                            "id": "INT PRIMARY KEY",
                            "name": "VARCHAR(255)",
                            ... # and so on.
                        }
                    }
                }
            }
        }
        ```

        **FYI**: the program runs through each database in ```"databases"``` and creates that database. It then loops through the ```"tables"``` and creates the tables under the database and finally populates that table with the data in ```"data_file"```
5. Run the ```main.py``` file and the database(s) should be set to go!

## TO-DOS
- A shell script that would automatically fill the proper values to ```config.py``` based on user input.
- Allow for other data types, like json.
