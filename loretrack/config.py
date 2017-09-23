import ConfigParser
import os


def get_section_name():
    """
    Returns name of the section in the config file.
    """
    return 'Loretrack'


def get_option(option, option_type='str'):
    """
    Grabs the value of the option from the config file and returns it in the
    format requested.
    """

    option_value = config.get(get_section_name(), option)
    if option_type == 'str':
        return option_value
    elif option_type == 'str_list':
        return option_value.split(',')
    elif option_type == 'int_list':
        return map(int, option_value.split(','))


def check_config_file():
    """
    Check if the config file exists, exits otherwise.
    """
    if not os.path.isfile(CONFIG_FILE):
        print 'Config file not found. Exiting...'
        exit()


class Flask_config():
    """
    Stores the configuration for flask.
    """

    WTF_CSRF_ENABLED = True
    SECRET_KEY = get_option('SECRET_KEY')

    basedir = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]


LORETRACK_DIR = os.path.abspath(os.path.join(os.getenv("HOME"), '.loretrack/'))
CONFIG_FILE = os.path.join(LORETRACK_DIR, 'config.cfg')
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)
