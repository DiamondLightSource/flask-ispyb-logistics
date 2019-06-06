import logging
import logging.handlers

from flask import Flask
from flask import render_template

# TODO - move modules into their own packages and tidy naming conventions.
# from dewars.ebic import api as ebic_api
# from dewars.zone4 import api as zone4_api
# from dewars.zone6 import api as zone6_api
from stores.dewars import api as stores_api
from dewars.routes import api as dewars_api
from dewars.routes import beamlines
from dewars.routes import locations

import ispyb_api 

logger = logging.getLogger('ispyb-logistics')
handler = logging.handlers.RotatingFileHandler('logs/logistics.log', maxBytes=1000000, backupCount=5)
handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(message)s]"))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
# app.register_blueprint(ebic_api)
# app.register_blueprint(zone6_api)
# app.register_blueprint(zone4_api)
app.register_blueprint(stores_api)
app.register_blueprint(dewars_api)

# Initialise flask sqla
ispyb_api.init_app(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/zone6/")
def zone6():
    return render_template('vue-dewars.html', 
        api_zone='zone6',
        title='Zone6',
        rack_locations=locations.get('zone6'),
        beamline_locations=beamlines.get('zone6'))

@app.route("/zone4/")
def zone4():
    return render_template('vue-dewars.html', 
        api_zone='zone4',
        title='Zone4',
        rack_locations=locations.get('zone4'),
        beamline_locations=beamlines.get('zone4'))

@app.route("/ebic/")
def ebic():
    return render_template('vue-dewars.html', 
        api_zone='ebic',
        title='EBIC',
        rack_locations=locations.get('ebic'),
        beamline_locations=beamlines.get('ebic'))

if __name__ == '__main__':
    app.run(debug=True)
