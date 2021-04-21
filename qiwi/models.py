from peewee import *


db = SqliteDatabase('qiwi.db')


class Base(Model):
    class Meta:
        database = db


class Payment(Base):
    txId = IntegerField(unique=True)


db.connect()
db.create_tables([Payment])
