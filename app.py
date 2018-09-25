import logging
import logging.handlers

from flask import Flask
from flask import render_template

# TODO - move modules into their own packages and tidy naming conventions.
from dewars.ebic import api as ebic_api
from dewars.zone6 import api as zone6_api 
from stores.dewars import api as stores_api

import ispyb_api 

logger = logging.getLogger('ispyb-logistics')
handler = logging.handlers.RotatingFileHandler('logs/logistics.log', maxBytes=1000000, backupCount=5)
handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(message)s]"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)
app.register_blueprint(ebic_api)
app.register_blueprint(zone6_api)
app.register_blueprint(stores_api)

# Initialise flask sqla
ispyb_api.init_app(app)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
