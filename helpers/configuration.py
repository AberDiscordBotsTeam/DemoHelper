import configparser

with open("config.ini") as file:
    BOT_CONFIGURATION = configparser.RawConfigParser(allow_no_value=True)
    BOT_CONFIGURATION.read_string(file.read())
