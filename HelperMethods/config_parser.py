import configparser
import os
import time
from Config import global_var


class ReadProp:

    @staticmethod
    def get_config_data(ini_file, section, key):
        config = configparser.ConfigParser()
        file_path = os.path.join(global_var.CONFIG_PATH, ini_file)
        read_success = config.read(file_path)
        if read_success:
            return config.get(section, key, fallback="not_found")
        else:
            print("Failed to configuration file")

    @staticmethod
    def write_config_data(ini_file, section, changes):
        config = configparser.ConfigParser()
        file_path = os.path.join(global_var.CONFIG_PATH, ini_file)
        read_success = config.read(file_path)

        if not config.has_section(section):
            config.add_section(section)

        for key, value in changes.items():
            config.set(section, key, value)

        with open(file_path, 'w') as configfile:
            config.write(configfile)

        for key, value in changes.items():
            assert config.get(section, key) == value
