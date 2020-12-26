# Parser process the input folder and extracts relevent information to run the application.
# Functionality: 
# - Open, read and close file.
# - filter out irrelevant information such as empty lines (\n) and comments (#) in file.
# - Ensure proper format of file.
# - Extract relevant information required to run the application i.e. tracking entries and emails. 

# TODO: 
# - log instead of printing errors and results

EMAIL_PARAMS = ["sender_email", "sender_email_password", "recipient_email"]
TRACK_PARAMS = ["title", "url", "check_interval", "class_list", "element_title", "check", "message_header", "message_body"]
TRACK_PARAMS_TYPE_LIST = ["class_list:,"]

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
    """
    Extracts the expected email parameter from a file into a list. 

    Parameters:
        filename(string): filename of target file.

    Returns:
        List: the expected input 
    """
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

def convert_listed_entries_to_list(track_list, index, separation_char):
    """
    Converts a given string in a list into a list based on given seperation character.

    Parameters:
        track_list(list): list containing tracking entry to edit. 
        index(int): index of target entry in track_list.
        separation_char(string): the character to seprate the string into list by.

    Returns:
        List: updated track_list.
    """
    track_list[index] = track_list[index].split(separation_char)
    return track_list

def extract_track_inputs(line_list):
    """
    Given a cleaned list of lines from file this function will extract each track 
    entry and validate that they follow the template given in TRACK_PARAMS.  

    Parameters:
        line_list(string): cleaned list of lines to be processed
    
    Returns:
        List: each tracking entry as list
    """
    list_inputs = []
    track_entry = []
    counter = 0

    for line in line_list:
        entry = line.split('=', 1)
        if entry[0] == TRACK_PARAMS[counter % len(TRACK_PARAMS)]:
            track_entry.append(entry[1])
            counter = counter + 1
            if counter % len(TRACK_PARAMS) == 0:
                for select in TRACK_PARAMS_TYPE_LIST:
                    select = select.split(":")
                    track_entry = convert_listed_entries_to_list(track_entry, TRACK_PARAMS.index(select[0]), select[1])
                list_inputs.append(track_entry)
                track_entry = []
        else:
            raise Exception("Unexpected track entry, make sure track entries follow template!")

    if counter % len(TRACK_PARAMS) != 0:
        raise Exception("Final track entry is incomplete!")

    return list_inputs 
