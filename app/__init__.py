from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Aw_VYH5iDVDqpRW2gSAmQFJWLNWJU3cEOd0jtNkzMaM'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/leroy/Desktop/photogram/photogram.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER']='app/static/uploads/'

db = SQLAlchemy(app)
from app import api

