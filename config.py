from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from secrates import databade_url
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = databade_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =  False

db = SQLAlchemy(app)
app.app_context().push()
