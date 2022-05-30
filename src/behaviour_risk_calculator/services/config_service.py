import os
import json


class ConfigService:
    """Service to handle configuration"""

    def __init__(self, config_name: str):
        """Loads configuration"""
        self.__config = self.__load_config(config_name)

    def __load_config(self, config_name) -> dict:
        """Loads configuration file and returns it as dictionary"""
        with open(config_name, 'r', encoding='utf-8') as file:
            config = json.load(file)
            return config

    def __get_config_member(self, key_path: str):
        """Finds given element by key_path in __config after spliting the key_path for each eleme"""
        split_path = key_path.split(':')
        temp_config = self.__config

        for key in split_path:
            temp_config = temp_config.get(key)

        return temp_config

    def get_value(self, property_path: str):
        """Returns value from configuration file. Use membered path for specification - i.e. Logs.Path > return Path value inside Logs object"""
        value = self.__get_config_member(property_path)
        return value