#!/bin/bash
export ISPYB_CONFIG_FILE=tests/test.cfg
export ISPYB_CONFIG_SECTION=ispyb_dev

export FLASK_APP=app.py
export FLASK_ENV=development

export SYNCHWEB_HOST=https://192.168.33.10
export SYNCHWEB_SSL=0

flask run
