import xmltodict # amazing library for parsing xml files

def xml_file_to_dict(file_path: str):
    with open(file_path, mode="r", encoding="utf-8") as file:
        dict_data = xmltodict.parse(file.read())
        return dict_data

def get_xml_data(xml_file: str, database_name: str, table_name: str, chunksize: int = 500) -> list:
    '''
    Returns xml data without the header row as a list of chunks
    '''
    
    data = xml_file_to_dict(xml_file)[database_name][table_name]
    list_of_rows = [list(row.values()) for row in data]
    
    # split the rows into reasonable chunks
    chunked_outcome = [list_of_rows[i * chunksize:(i + 1) * chunksize] for i in range((len(list_of_rows) + chunksize - 1) // chunksize)]
    
    return chunked_outcome
