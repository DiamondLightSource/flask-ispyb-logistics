import logging
import logging.handlers

from flask import Flask
from flask import render_template
from flask import send_file

# Import routes modules
from api.beamlines.routes import api as beamlines_api
from api.containers.routes import api as containers_api
from api.stores.routes import api as stores_api
from api.dewars.routes import api as dewars_api

from api import ispyb_api

logger = logging.getLogger('ispyb-logistics')
handler = logging.handlers.RotatingFileHandler('logs/logistics.log', maxBytes=10000000, backupCount=5)
handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(message)s]"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__, static_folder="client/dist/static", static_url_path='/static')

app.register_blueprint(stores_api)
app.register_blueprint(dewars_api)
app.register_blueprint(containers_api)
app.register_blueprint(beamlines_api)

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

@app.route("/lab14/")
def lab14_page():
    return send_file('client/dist/lab14.html')


if __name__ == '__main__':
    app.run(debug=True)
