import pandas as pd
import csv

def get_csv_headers(csv_file: str) -> list:
    '''
    Reads the header row of a csv file and returns the values as a list
    '''
    return list(pd.read_csv(csv_file).columns)
    
def get_csv_data(csv_file: str, chunksize: int = 500) -> list:
    '''
    Returns csv data without the header row as a list of chunks
    '''
    # First we need to handle any missing quotes in a csv file
    # because missing quotes will cause issues with sql insert
    quote_string_values(csv_file)
    
    df = pd.read_csv(csv_file, delimiter=",", header=0, encoding="utf-8")
    parsed_data = df.fillna(0) # replaces nan values with 0
    list_of_rows = [list(row) for row in parsed_data.values]

    # split the rows into reasonable chunks
    chunked_outcome = [list_of_rows[i * chunksize:(i + 1) * chunksize] for i in range((len(list_of_rows) + chunksize - 1) // chunksize)]
    
    return chunked_outcome

def quote_string_values(csv_file: str):
    '''
    Adds quotes to string values in *csv_file* and ensures the number of items in each row matches the number of columns.
    '''
    # Read the content of the csv file
    with open(csv_file, mode="r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        rows = [row for row in reader]

    # Get the header row to determine the number of columns
    header = rows[0]
    num_columns = len(header)

    # Write the updated content back to the same file with quotes where necessary
    with open(csv_file, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_NOTNULL)
        writer.writerow(header)  # Write the header row first
        for row in rows[1:]:
            if len(row) != num_columns:
                row = fix_row(row, num_columns)
            modified_row = [quote_if_needed(item) for item in row]
            writer.writerow(modified_row)

def quote_if_needed(item: str) -> str:
    '''
    Quotes the item if it contains a comma and is not already quoted.
    '''
    if ',' in item and not (item.startswith('"') and item.endswith('"')):
        return f'"{item}"'
    return item

def fix_row(row: list, num_columns: int) -> list:
    '''
    Fixes the row by quoting fields that contain commas to ensure the number of items matches the number of columns.
    '''
    fixed_row = []
    current_item = ""
    for item in row:
        if len(fixed_row) < num_columns - 1:
            if ',' in item and not (item.startswith('"') and item.endswith('"')):
                if current_item:
                    current_item += f', {item}'
                else:
                    current_item = item
            else:
                if current_item:
                    fixed_row.append(current_item)
                    current_item = ""
                fixed_row.append(item)
        else:
            if current_item:
                current_item += f', {item}'
            else:
                current_item = item
    if current_item:
        fixed_row.append(current_item)
    return fixed_row