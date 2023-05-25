from peewee import ForeignKeyField
from lib.base_model import BaseModel
from lib.user import User


class Relationship(BaseModel):
    from_user = ForeignKeyField(User, backref="relationships")
    to_user = ForeignKeyField(User, backref="related_to")

    class Meta:
        indexes = ((("from_user", "to_user"), True),)
