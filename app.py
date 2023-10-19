from flask import Flask
from peewee import *


app = Flask(__name__)
app.config.from_object('config.Configuration')
database = SqliteDatabase('14.db')

