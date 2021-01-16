# Parse processes the input folder and extracts relevent information to run the application.
# Functionality: 
# - Open, read and close file.
# - filter out irrelevant information such as empty lines (\n) and comments (#) in file.
# - Ensure proper format of file.
# - Extract relevant information required to run the application i.e. tracking entries and emails. 

# TODO: 
# - add logging
# - add error checking
# - update docstrings
# - Wrap in a class to improve usability 

CONFIG_PARAMS = ["sender_email", "sender_email_password", "recipient_email", "timeout"]
TRACK_PARAMS = ["title", "url", "selector", "element_title", "check", "message_header", "message_body", "timer"]
TRACK_PARAMS_TYPE_LIST = []


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


def extract_config_input(filename):
    """
    Extracts the expected email parameter from a file into a list. 

    Parameters:
        filename(string): filename of target file.

    Returns:
        List: the expected input 
    """
    file = read_file(filename)
    line_list = convert_file_to_list(file)

    email_inputs = {}

    for line in line_list:
        split_line = line.split('=', 1)

        if split_line[0] not in CONFIG_PARAMS:
            raise Exception(
                "Entry " + split_line[0] + " in " + filename + " is unknown! only " + str(CONFIG_PARAMS) + " are allowed!")
        else:
            if split_line[1].strip() == "\n" or split_line[1].strip() == "":
                raise Exception("Entry " + split_line[0] + " in " + filename + " is empty!")
            email_inputs[split_line[0]] = split_line[1].replace("\n", "")

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
    track_entry = {}
    counter = 0

    for line in line_list:
        entry = line.split('=', 1)
        if entry[0] == TRACK_PARAMS[counter % len(TRACK_PARAMS)]:
            track_entry[entry[0]] = entry[1]
            counter = counter + 1
            if counter % len(TRACK_PARAMS) == 0:
                for select in TRACK_PARAMS_TYPE_LIST:
                    select = select.split(":")
                    track_entry = convert_listed_entries_to_list(track_entry, TRACK_PARAMS.index(select[0]), select[1])
                list_inputs.append(track_entry)
                track_entry = {}
        else:
            raise Exception("Unexpected track entry, make sure track entries follow template!")

    if counter % len(TRACK_PARAMS) != 0:
        raise Exception("Final track entry is incomplete!")

    return list_inputs


def message_format(track, message):
    message = message.replace("$url", track["url"])
    message = message.replace("$title", track["title"])
    return message