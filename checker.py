# Process the commands for tracking entry
# Commands:
# contains              - trigger if the webpage contains the HTML element
# not_contains          - trigger if the webpage does not contains the HTML element
# contains_select=data  - trigger if the webpage element title contains the selected title
# price_decrease        - trigger if the price detected in the HTML element decreases or changes
# target_price=10.00    - trigger if the price is equal to or less than target_price

import re
import datetime

COMMANDS = ["contains", "not_contains", "price_decrease"]
DATA_COMMANDS = ["contains_select", "target_price"]


def clean_data(data):
    return data.strip()


def convert_price_to_float(text):
    text = text.replace(" ", "").replace(",", "").replace("$", "")
    price = re.findall("\d+.\d+", text)
    return float(price[0])


def contains(expected, result):
    return expected == result


def not_contains(expected, result):
    return expected != result


def contains_select(data, result):
    return data == result

def price_decrease(element_price, current_price):
    element_price = convert_price_to_float(element_price)
    current_price = convert_price_to_float(current_price)
    return element_price > current_price


def target_price(target, current):
    target = convert_price_to_float(target)
    current = convert_price_to_float(current)
    return target <= current


def valid_command(command):
    for expect_command in DATA_COMMANDS:
        if command.find(expect_command):
            return True
    return command in COMMANDS


def has_data(command):
    for expect_command in DATA_COMMANDS:
        if command.find(expect_command) != -1:
            return True
    return False


def extract_data(command):
    return command.split("=")


def status_check(track, command_result):
    if command_result and track["change_status"]:
        track["trigger"] = False
        return track
    elif command_result and not track["change_status"]:
        track["trigger"] = True
        track["change_status"] = True
        return track
    elif not command_result and track["change_status"]:
        track["trigger"] = False
        track["change_status"] = False
        return track
    elif not command_result and not track["change_status"]:
        track["trigger"] = False
        return track

def process_command(track):
    #t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if track["result"] is not None:
        track["result"] = clean_data(track["result"])

    if "change_status" not in track:
        track["change_status"] = False
    
    if "trigger" not in track:
        track["trigger"] = False

    if track["response_url"] != track["url"]:
        track["redirect"] = True
        return track
    else:
        track["redirect"] = False
        return track

    if valid_command(track["check"]):
        if has_data(track["check"]):
            command_data = extract_data(track["check"])
            #print("[" + t + "]", "\"" + track["title"] + "\"", "command:", track["check"],"expected:", command_data[0], "actual:", track["result"])
            command_result = globals()[command_data[0]](command_data[1], track["result"])
            return status_check(track, command_result)

        else:
            #print("[" + t + "]", "\"" + track["title"] + "\"", "command:", track["check"],"expected:", track["element_title"], "actual:", track["result"])
            command_result = globals()[track["check"]](track["element_title"], track["result"])
            return status_check(track, command_result)