import json

def get_json_headers(json_file: str) -> list:
    '''
    Reads the header row of a json file and returns the values as a list
    '''
    with open(json_file, mode="r", encoding="utf-8") as file:
        data = json.load(file)[0] # get the keys from the first object
        return list(data.keys())
    
def get_json_data(json_file: str, chunksize: int = 500) -> list:
    '''
    Returns json data without the header row as a list of chunks
    '''
    with open(json_file, mode="r", encoding="utf-8") as file:
        data = json.load(file)
        list_of_rows = [list(row.values()) for row in data]
        
        # split the rows into reasonable chunks
        chunked_outcome = [list_of_rows[i * chunksize:(i + 1) * chunksize] for i in range((len(list_of_rows) + chunksize - 1) // chunksize)]
        
        return chunked_outcome