from peewee import Model, PostgresqlDatabase
import os

database_url = os.environ.get("DATABASE_URL", "default_database")

if database_url == "test_database":
    database = PostgresqlDatabase("chitter_test", host="localhost")
else:
    database = PostgresqlDatabase("chitter", host="localhost")


class BaseModel(Model):
    class Meta:
        database = database
