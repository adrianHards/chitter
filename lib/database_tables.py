from lib.base_model import database
from lib.user import User
from lib.relationship import Relationship
from lib.message import Message


def create_tables():
    with database:
        database.create_tables([User, Relationship, Message])
