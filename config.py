from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)
database_url = os.enviro.get("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = databade_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =  False

db = SQLAlchemy(app)
app.app_context().push()
