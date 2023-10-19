import datetime
from peewee import *
from app import database


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now())


class Post(BaseModel):
    user = ForeignKeyField(User, backref='messages')
    content = TextField()
    pub_date = DateTimeField()


def create_tables():
    with database:
        database.create_tables([User, Post])