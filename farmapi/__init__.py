from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from farmapi.farm.config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
ma = Marshmallow(app)

from farmapi.farm.views import farmapi
app.register_blueprint(farmapi)
db.create_all()
