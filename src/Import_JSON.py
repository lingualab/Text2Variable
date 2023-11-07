import json

def read_json_file(file_name):
    """
    Reads a JSON file and returns its content as a Python dictionary.

    Args:
        file_name (str): The name of the JSON file to read.

    Returns:
        dict or None: The content of the JSON file as a dictionary, or None if there was an error.
        
    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: If any other error occurs during file reading.

    """
    try:
        # Try to open the file for reading with UTF-8 encoding
        with open(file_name, 'r', encoding='utf-8') as file:
            # Load the JSON content from the file into a Python dictionary
            content = json.load(file)
        return content
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print(f"The file {file_name} was not found.")
        return None
    except Exception as e:
        # Handle other exceptions (e.g., invalid JSON format)
        print(f"An error occurred while reading the file {file_name}: {str(e)}")
        return None

