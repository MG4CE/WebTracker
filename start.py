# Starting script, currently used to test out code

import parse
import mailer

file_list = parse.convert_file_to_list(parse.read_file("track.txt"))
file_list = parse.clean_list(file_list)
file_list = parse.extract_track_inputs(file_list)

for x in file_list:
    print(x)

print(file_list)

print(parse.extract_email_input("config.cfg"))