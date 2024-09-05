import pandas as pd
import csv
import os

def get_file_path(filename: str) -> str:
    '''
    Returns the path of *filename* based on the directory of the file that called this function,
    searching through all subdirectories and parent directories.
    '''
    
    directory = os.path.dirname(os.path.abspath(__file__))
    
    while directory:
        for root, dirs, files in os.walk(directory):
            if filename in files:
                return os.path.join(root, filename)
        
        parent_directory = os.path.dirname(directory)
        if parent_directory == directory:
            break
        directory = parent_directory
    
    raise FileNotFoundError(f"{filename} not found in directory {directory} or any of its parent directories")

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
    
    df = pd.read_csv(csv_file, delimiter=",", header=1, encoding="utf-8")
    parsed_data = df.fillna(0) # replaces nan values with 0
    list_of_rows = [list(row) for row in parsed_data.values]
    
    # split the rows into reasonable chunks
    # this will be necessary since sql does not allow
    # queries of over 70000 lines
    
    # source: geeksforgeeks <3
    chunked_outcome = [list_of_rows[i * chunksize:(i + 1) * chunksize] for i in range((len(list_of_rows) + chunksize - 1) // chunksize)]
    
    return chunked_outcome

def quote_string_values(csv_file: str):
    '''
    Adds quotes to string values in *csv_file*
    '''
    # Read the content of the csv file
    with open(csv_file, mode="r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        rows = [row for row in reader]

    # Write the updated content back to the same file with quotes
    with open(csv_file, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in rows:
            writer.writerow(row)