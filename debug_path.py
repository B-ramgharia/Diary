import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'diary.db')
print(f"Computed BASEDID: {basedir}")
print(f"Computed DB PATH: {db_path}")
print(f"File exists: {os.path.exists(db_path)}")
if os.path.exists(db_path):
    print(f"File size: {os.path.getsize(db_path)} bytes")
