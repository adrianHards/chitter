from peewee import Model, PostgresqlDatabase

database = PostgresqlDatabase("chitter", host="localhost")


class BaseModel(Model):
    class Meta:
        database = database
