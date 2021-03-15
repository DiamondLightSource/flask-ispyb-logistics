import os
import filecmp
from subprocess import call
import os, sys
# Set root dir as home of the python path - so we can find api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import ispyb_api

current_file = './api/ispyb_api/models.py'
outfile = "./scripts/automodels.py"
tmpfile = "/tmp/automodels.py"

config_filename = os.environ.get('ISPYB_CONFIG_FILE', 'api/tests/test.cfg')
config_section = os.environ.get('ISPYB_CONFIG_SECTION', 'ispyb_dev')

print("Reading database credentials from {} [{}] ".format(config_filename, config_section))

db_url = ispyb_api.read_db_config(config_filename, config_section)

print(db_url)

call(["sqlacodegen", "{}".format(db_url), "--tables", "DewarTransportHistory", "--outfile", tmpfile])

call("sed s'/Base = declarative_base()/from . import Base/' {} | sed '/metadata = Base.metadata/d' > {}".format(tmpfile, outfile), shell=True)

#
# Test if newly generated file is different to current models file
#
result = filecmp.cmp(current_file, outfile)

if result:
    print("INFO: Auto Generated file is the same as the current models file")
else:
    print("WARNING: Auto Generated file is different from the current models file")

