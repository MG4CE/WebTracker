# Process the commands for tracking entry
# Commands:
# contains              - trigger if the webpage contains the HTML element
# not_contains          - trigger if the webpage does not contains the HTML element
# contains_select=data  - trigger if the webpage element title contains the selected title
# price_decrease        - trigger if the price detected in the HTML element decreases or changes
# target_price=10.00    - trigger if the price is equal to or less than target_price

import mailer
import parse
import re

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


class CommandProcessor:

    def __init__(self, track_entry, result, email_info):
        self.track_info = track_entry
        if result is not None:
            self.data = clean_data(result)
        else:
            self.data = result

        self.email_info = email_info

        self.command = self.track_info[parse.TRACK_PARAMS.index("check")]

        if valid_command(self.command):
            if has_data(self.command):
                command_data = extract_data(self.command)
                print(self.command, self.data)
                result = globals()[command_data[0]](command_data[1], self.data)
                if result:
                    mailer.send_email(email_info[0], email_info[1], email_info[2],
                                      self.message_format(self.track_info[parse.TRACK_PARAMS.index("message_header")]),
                                      self.message_format(self.track_info[parse.TRACK_PARAMS.index("message_body")]))
            else:
                print(self.command, self.data, "expected:", self.track_info[parse.TRACK_PARAMS.index("element_title")])
                result = globals()[self.command](self.track_info[parse.TRACK_PARAMS.index("element_title")], self.data)
                if result:
                    mailer.send_email(email_info[0], email_info[1], email_info[2],
                                      self.message_format(self.track_info[parse.TRACK_PARAMS.index("message_header")]),
                                      self.message_format(self.track_info[parse.TRACK_PARAMS.index("message_body")]))


    def message_format(self, message):
        message = message.replace("$url", self.track_info[parse.TRACK_PARAMS.index("url")])
        message = message.replace("$title", self.track_info[parse.TRACK_PARAMS.index("title")])
        if self.command.find("price") != -1 and not None:
            message = message.replace("$price", "$"+convert_price_to_float(self.data))
        return message

