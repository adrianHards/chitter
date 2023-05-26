from peewee import CharField, DateTimeField
from lib.base_model import BaseModel


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

    # Meta is known as an inner class or a nested class, to configure metadata about the outer class.
    # here we're telling peewee to change default name of table to users not user
    class Meta:
        db_table = "users"

    def following(self):
        from lib.relationship import Relationship

        return (
            User.select()
            .join(Relationship, on=Relationship.to_user)
            .where(Relationship.from_user == self)
            .order_by(User.username)
        )

    def followers(self):
        from lib.relationship import Relationship

        return (
            User.select()
            .join(Relationship, on=Relationship.from_user)
            .where(Relationship.to_user == self)
            .order_by(User.username)
        )

    def is_following(self, user):
        from lib.relationship import Relationship

        return (
            Relationship.select()
            .where((Relationship.from_user == self) & (Relationship.to_user == user))
            .exists()
        )
