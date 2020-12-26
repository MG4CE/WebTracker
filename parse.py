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
    line_list = [line for line in line_list if line != "\n" and not line.strip().startswith("#", 0)]
    line_list = [line.replace("\n", "") for line in line_list]
    return line_list

def extract_email_input(filename):
    file = read_file(filename)
    line_list = convert_file_to_list(file)

    email_inputs = []

    for line in line_list:
        split_line = line.split('=', 1)

        if  split_line[0] not in EMAIL_PARAMS:
            raise Exception("Entry " + split_line[0] + " in " + filename + " is unknown! only " + EMAIL_PARAMS + " are allowed!")
        else:
            if split_line[1].strip() == "\n" or split_line[1].strip() == "":
                raise Exception("Entry " + split_line[0] + " in " + filename + " is empty!")
            email_inputs.append(split_line[1].replace("\n", ""))

    return email_inputs

def extract_track_inputs(line_list):
    list_inputs = []
    track_entry = []
    counter = 0

    for line in line_list:
        entry = line.split('=', 1)
        if entry[0] == TRACK_PARAMS[counter % len(TRACK_PARAMS)]:
            track_entry.append(entry[1])
            counter = counter + 1
            if counter % len(TRACK_PARAMS) == 0:
                list_inputs.append(track_entry)
                track_entry = []
        else:
            raise Exception("Unexpected track entry, make sure track entries follow template!")

    if counter % len(TRACK_PARAMS) != 0:
        raise Exception("edge case!")

    return list_inputs 

def process_track_input(track_list):
    return []

if __name__ == "__main__":
    file_list = convert_file_to_list(read_file("track.txt"))
    file_list = clean_list(file_list)
    for x in extract_track_inputs(file_list):
        print(x)
    print(extract_email_input("config.cfg"))
