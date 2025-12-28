import configparser
import os
from Config import global_var
from Config.crypto_helper import CryptoHelper


class ReadProp:

    @staticmethod
    def get_config_data(ini_file, section, key, decrypt=False):
        config = configparser.ConfigParser()
        file_path = os.path.join(global_var.CONFIG_PATH, ini_file)
        read_success = config.read(file_path)

        if not read_success:
            print("Failed to read configuration file")
            return "not_found"

        value = config.get(section, key, fallback="not_found")

        if decrypt:
            return CryptoHelper.decrypt(value)

        return value

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
