#!/bin/bash

# Info
echo "Thanks for choosing this database populator."
echo
echo "The script is going to ask you a few configuration related questions."
echo
echo "Please note, that all of the values you give, can be later changed in config.py"
echo

# Ask the DB keys & file format
read -e -p "Database host [localhost]: " -i "localhost" DB_HOST
read -e -p "Database port [3306]: " -i "3306" DB_PORT
read -e -p "Database user (with write access) [root]: " -i "root" DB_USER
read -e -p "Database password [password]: " -s DB_PASSWORD
read -e -p "Drop matching databases on database creation? (True/False) [True]: " -i "True" DROP_EXISTING_DATABASES
read -e -p "Allow automatic database commits? (True/False) [False]: " -i "False" AUTOCOMMIT

# Data related questions
read -e -p "Data format of choice (csv/json/xml) [csv]: " -i "csv" DATA_FORMAT
read -e -p "Data chunksize; max amount of SQL inserts at once (recommended value 500 - 2500) [500]: " -i "500" CHUNKSIZE
echo

echo "Creating your configuration base..."

CONFIG_FILE="config.py"

cat <<EOL > $CONFIG_FILE
def config() -> dict:
    return {
        "connection_params": {
            "host": "$DB_HOST",
            "port": "$DB_PORT",
            "username": "$DB_USER",
            "password": "$DB_PASSWORD",
            "autocommit": $AUTOCOMMIT,
            "collation": "utf8mb4_unicode_ci",
        },
        "chunksize": $CHUNKSIZE,
        "data_format": "$DATA_FORMAT", # "csv" | "json" | "xml"
        "drop_existing_databases": $DROP_EXISTING_DATABASES,
        "databases": {
            # Your databases & tables go here!
        }
    }
EOL

echo "#############################################################"
echo
echo "Your configuration file (config.py) was successfully created!"
echo
echo "#############################################################"

# Self destruct
rm -- "$0"