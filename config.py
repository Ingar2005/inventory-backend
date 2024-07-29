from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://app:123@localhost/inventory"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =  False

db = SQLAlchemy(app)
app.app_context().push()
