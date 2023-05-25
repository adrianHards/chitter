from peewee import ForeignKeyField, TextField, DateTimeField
from lib.base_model import BaseModel
from lib.user import User


class Message(BaseModel):
    user = ForeignKeyField(User, backref="messages")
    content = TextField()
    pub_date = DateTimeField()
