from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
import os
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import  sessionmaker

user  = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
database_name = os.environ.get("DB_NAME")
print(f"mysql://{user}:{password}@{host}:3306/{database_name}")
engine = create_engine(
    f"mysql://{user}:{password}@{host}:3306/{database_name}",
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"]=f"mysql://{user}:{password}@{host}:3306/{database_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Enable connection pooling
app.config['SQLALCHEMY_POOL_SIZE'] = 20  # Adjust as needed
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20  # Adjust as needed
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
db= SQLAlchemy(app)

app.app_context().push()
