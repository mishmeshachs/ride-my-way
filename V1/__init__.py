# __init__.py

from flask import Flask


# instantiate the app
app = Flask(__name__, instance_relative_config=True)

# set config
app.config.from_object('config.BaseConfig')


from V1.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)
from V1.ride.views import ride_blueprint
app.register_blueprint(ride_blueprint)
