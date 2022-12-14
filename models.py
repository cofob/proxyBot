from peewee import *
import pickle
from time import time


db = SqliteDatabase('database.db')


class Base(Model):
    class Meta:
        database = db


class Setting(Base):
    name = CharField()
    value = BlobField()

    def get_by_name(self, name):
        m = self.get(name=name)
        return pickle.loads(m.value)


class User(Base):
    user_id = IntegerField(unique=True)
    firstname = CharField()
    lastname = CharField(null=True)
    username = CharField(null=True)
    register_timestamp = IntegerField(default=time)
    balance = FloatField(default=0)
    subscription = IntegerField(default=0)
    action = CharField(null=True)
    data = BlobField(null=True)
    lang = CharField(default='ru')
    token = TextField(null=True)


class Tariff(Base):
    name = CharField(unique=True)
    description = TextField()
    add_time = IntegerField()
    price = IntegerField()


db.connect()
db.create_tables([Setting, User, Tariff])
