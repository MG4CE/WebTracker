# Parser process the input folder and extracts relevent information to run the application.
# Functionality: 
# - Open, read and close file.
# - filter out irrelevant information such as empty lines (\n) and comments (#) in file.
# - Ensure proper format of file.
# - Extract relevant information required to run the application i.e. tracking entries and emails. 

EMAIL_PARAMS = ["sender_email", "sender_email_password", "recipient_email"]
TRACK_PARAMS = ["title", "url", "check_interval", "class_list", "element_title", "check", "message_header", "message_body"]

def read_file(dir):
    """
    Opens a file with given directory in read-only mode.

    Parameters:
        dir (string): the directory path of target file.
    
    Returns:
        File Object: the file object opened in read-only mode.
    """
    file = open(dir, "r")
    return file

def convert_file_to_list(file):
    """
    Converts a file object into a list of lines.

    Parameters:
        file (File Object): opened file.
    
    Returns:
        list: list of strings representing each line the file.
    """
    return file.readlines()

def close_file(file):
    """
    Closeses the given file.

    Parameters:
        file (File Object): opened file.
    """
    file.close()

def clean_list(line_list):
    """
    Filters out comments (denoted by lines starting with "#") and empty lines.

    Parameters:
        line_list (list): list contaning the each line of a file as a string entry.

    Returns:
        list: newly updated list of string.
    """
    line_list = [line for line in line_list if line is not "\n" and not line.strip().startswith("#", 0)]
    line_list = [line.replace("\n", "") for line in line_list]
    return line_list

def extract_email_input(line_list):
    return EMAIL_PARAMS

def extract_track_inputs(line_list):
    return TRACK_PARAMS

def process_track_input(track_list):
    return []

if __name__ == "__main__":
    file_list = convert_file_to_list(read_file("track.txt"))
    print(clean_list(file_list))
