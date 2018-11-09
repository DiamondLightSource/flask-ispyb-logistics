# ISPyB Logistics (Dewar Management)

## Setup
Create a virtualenv then install dependencies with pip
    $ pip install -r requirements.txt

## Configuration
There is an example run script in the ./scripts directory which shows how to configure the app

### SynchWeb URL (for updating history)
    export SYNCHWEB_HOST=<SynchWeb address: e.g. https://ispyb.diamond.ac.uk/ >

### ISPyB Database config
    export ISPYB_CONFIG_FILE=<path to credentials file>  
    export ISPYB_CONFIG_SECTION=<section name in file (e.g. ispyb_prod)>  

Format of the .cfg file is as specified by ispyb-python-api  
Example in tests/test.cfg

### Flask config
    export FLASK_APP=app.py
    export FLASK_ENV=development | production

## Running
    $ flask run --host <ip addr> --port <port>

## Security
There is no application level authentication here
It's designed to work with nginx to control access 

## Model Generation
This app uses a fraction of the ISPyB database tables
If core tables have changed (Dewar, DewarTransportHistory, BLSession, Proposal, Person, Shipping etc.) the models file might need to be re-generated.

To update the models within the ispyb_api package run:
    $ python -m scripts/generate_models

This will create a './scripts/automodels.py' file

The script output will show if the file differs from ispyb_api/models.py

If it does, integrate changes or copy the ./scripts/automodels.py file across to the ispyb_api/models.py
