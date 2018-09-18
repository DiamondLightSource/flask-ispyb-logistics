# For convenience import the main class here 
# So we just need to import ispyb_api.ISPyBManager
#from ispyb_manager import ISPyBManager
import os
from ConfigParser import ConfigParser
from ConfigParser import NoOptionError, NoSectionError

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL

db = SQLAlchemy()
Base = db.Model

def read_db_config(filename, section='ispyb_mysql_sp'):
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
    
        db_url = URL(drivername='mysql+pymysql',
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
    config_section = os.environ.get('ISPYB_CONFIG_SECTION', 'ispyb_mysql_sp')

    print("Reading database credentials from {} [{}] ".format(config_filename, config_section))

    db_url = read_db_config(config_filename)
    
    if db_url is None:
        db_url = 'mysql+pymysql://ispyb:integration@localhost:3306/ispyb'

        print("Config read failed, falling back to default db connection credentials")

    print("Database connection URL: {}".format(db_url))

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    db.init_app(app)
