from peewee import *
import lib.conf as config

db = SqliteDatabase(config.get_path_to_db())

class BaseModel(Model):
    class Meta:
        database = db
