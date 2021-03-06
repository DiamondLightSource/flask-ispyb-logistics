import logging
import logging.handlers

from flask import Flask
from flask import render_template
from flask import send_file

# Simplified this down to two modules stores and dewar-zones
from stores.dewars import api as stores_api
from dewars.routes import api as dewars_api
from dewars.routes import beamlines
from dewars.routes import locations

import ispyb_api

logger = logging.getLogger('ispyb-logistics')
handler = logging.handlers.RotatingFileHandler('logs/logistics.log', maxBytes=10000000, backupCount=5)
handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(message)s]"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__, static_folder="client/dist/static", static_url_path='/static')

app.register_blueprint(stores_api)
app.register_blueprint(dewars_api)

# Initialise flask sqla
ispyb_api.init_app(app)

# Allocate the routes for each 'app'
@app.route("/")
def index():
    return send_file('client/dist/index.html')

@app.route("/stores/")
def stores_page():
    return send_file('client/dist/stores.html')

@app.route("/ebic/")
def ebic_page():
    return send_file('client/dist/ebic.html')

@app.route("/zone4/")
def zone4_page():
    return send_file('client/dist/zone4.html')

@app.route("/zone6/")
def zone6_page():
    return send_file('client/dist/zone6.html')


if __name__ == '__main__':
    app.run(debug=True)
