import configparser
import os

import sys

DEFAULT_NAME = 'config'

DEFAULT = 'config'


# DEFAULT_PATH = os.path.join(HOME, DEFAULT)


def create_config(db_path='None', log_path='None', logging_level=1):
    """
    Creates a configuration file that describes the logger and database paths
    :param db_path: - path to database. If the argument was not passed, it takes the value 0
    :param log_path: - path to log file. If the argument was not passed, it takes the value 0
    :return - create config file:

    """
    config = configparser.ConfigParser()
    config.add_section("settings")
    config.set('settings', 'path_to_log', log_path)
    config.set('settings', 'path_to_db', db_path)
    config.set('settings', 'logging-level', logging_level)

    path = os.path.dirname(os.path.abspath(__file__))
    path = path[:-7]
    path = os.path.join(path, DEFAULT_NAME)
    check_tracker_folder(path)
    path = os.path.join(path, 'conf.ini')

    with open(path, 'w') as config_file:
        config.write(config_file)


def load_config():
    """
    Load configuration from config file. If there was no configuration file, it will be created
    :return config: console configuration with paths to db,log,etc.

    """
    config = configparser.ConfigParser()
    path = os.path.dirname(os.path.abspath(__file__))
    path = path[:-7]
    path = os.path.join(path, DEFAULT_NAME)

    if not os.path.exists(path):
        create_config()
    path = os.path.join(path, 'conf.ini')
    config.read(path)
    return config


def get_path_to_db():
    """
    Return path to database
    :return - path to database:

    """
    config = load_config()
    path_to_db = config.get('settings', 'path_to_db')
    if path_to_db == 'None':
        path = os.path.dirname(os.path.abspath(__file__))
        path = path[:-7]
        path_to_db = os.path.join(path, 'database.sqlite3')
    return path_to_db


def get_logging_level():
    """
    Returns the value of the specified logging level from configutation file
    :return: logging level

    """
    config = load_config()
    level = config.get('settings', 'logging-level')
    return level


def get_path_to_log():
    """
    Return path to logging files
    :return: path to logging files

    """
    config = load_config()
    path_to_log = config.get('settings', 'path_to_log')
    if path_to_log == 'None':
        path = os.path.dirname(os.path.abspath(__file__))
        path_to_log = path[:-7]
    return path_to_log


def check_tracker_folder(path):
    """
    Checks for a directory at the specified path. If the directory does not exist, it will be created
    :param path: path to check
    :return:

    """
    if not os.path.exists(path):
        f=open(path,'w')
        f.close()
        print("all clear")
        return 1
