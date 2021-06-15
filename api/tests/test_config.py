from configparser import ConfigParser
from configparser import NoOptionError, NoSectionError
import sys

def test(filename):
    """
    Given a filename test that we can get the credentials
    """
    section = 'ispyb_dev'

    config = ConfigParser()
    config.read(filename)

    try:
        user = config.get(section, 'user')
        password = config.get(section, 'pw')
        host = config.get(section, 'host')
        port = config.getint(section, 'port')
        db = config.get(section, 'db')

        print("DATABASE URL = mysql+mysqlconnector://{}:{}@{}:{}/{}".format(user, password, host, port, db))
    except NoOptionError:
        print("Error retrieving values from config file {}".format(filename))
    except NoSectionError:
        print("Error the config file {} does not have {} section".format(filename, section))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'tests/test.cfg'
    # One that works...
    print("Testing read from config file: ", filename)
    test(filename)
    
