from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from routes.home import Home
from routes.login import Login

app = Flask(__name__)
app.secret_key = 'mysecretkey'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://bdi:pepe1234@localhost/Binance"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


SQLAlchemy(app)

app.register_blueprint(Home)
app.register_blueprint(Login)


