from ConfigParser import ConfigParser
from ConfigParser import NoOptionError, NoSectionError

def test(filename):
    """
    Given a filename test that we can get the login data
    """
    section = 'ispyb_mysql_sp'

    config = ConfigParser()
    config.read(filename)

    try:
        user = config.get(section, 'user')
        password = config.get(section, 'pw')
        host = config.get(section, 'host')
        port = config.getint(section, 'port')
        db = config.get(section, 'db')

        print("mysql://{}:{}@{}:{}/{}".format(user, password, host, port, db))
    except NoOptionError:
        print("Error retrieving values from config file {}".format(filename))
    except NoSectionError:
        print("Error the config file {} does not have {} section".format(filename, section))


if __name__ == "__main__":
    # One that works...
    test('tests/test.cfg')

    # One that doesnt...
    test('tests/test_not_exists.cfg')
    