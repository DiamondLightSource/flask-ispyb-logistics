import os
from configparser import ConfigParser
from configparser import NoOptionError, NoSectionError

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL

db = SQLAlchemy()
Base = db.Model

def read_db_config(filename, section):
    """
    Try to get db connection info from file
    """
    # [ispyb_mysql_sp]
    # user = ispyb
    # pw = integration
    # host = localhost
    # port = 3306
    # db = ispyb

    db_url = None

    try:
        config = ConfigParser()
        config.read(filename)

        db_url = URL.create(drivername='mysql+mysqlconnector',
                     username=config.get(section, 'user'),
                     password=config.get(section, 'pw'),
                     host=config.get(section, 'host'),
                     port=config.get(section, 'port'),
                     database=config.get(section, 'db'))
    except NoOptionError:
        print("Error retrieving values from config file {}".format(filename))
    except NoSectionError:
        print("Error the config file {} does not exist, or have the {} section".format(filename, section))

    return db_url


def init_app(app):
    """
    Initialise the database connection and flask-sqlalchemy
    """
    config_filename = os.environ.get('ISPYB_CONFIG_FILE', 'tests/test.cfg')
    config_section = os.environ.get('ISPYB_CONFIG_SECTION', 'ispyb_dev')

    print("Reading database credentials from {} [{}] ".format(config_filename, config_section))

    db_url = read_db_config(config_filename, config_section)

    if db_url is None:
        db_url = 'mysql+mysqlconnector://ispyb:integration@localhost:3306/ispyb'

        print("Config read failed, falling back to default db connection credentials")

    print("Database connection URL: {}".format(db_url))

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
