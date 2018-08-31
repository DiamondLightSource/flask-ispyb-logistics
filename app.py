from flask import Flask

# TODO - move modules into their own packages and tidy naming conventions.
from ebic.dewars import api as ebic_api
from mx.dewars import api as mx_api 
from stores.dewars import api as stores_api

app = Flask(__name__)
app.register_blueprint(ebic_api)
app.register_blueprint(mx_api)
app.register_blueprint(stores_api)

if __name__ == '__main__':
    app.run(debug=True)
