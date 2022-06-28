from operator import index
import peewee
import json
from playhouse.pool import PooledMySQLDatabase
from datetime import date, datetime

db = PooledMySQLDatabase(
    'sakila',
    max_connections=8,
    stale_timeout=10,
    user='root'
)

class BaseModel(peewee.Model):

    class Meta:
        database = db

class Language(BaseModel):

    language_id = peewee.SmallIntegerField(primary_key=True)
    name = peewee.CharField(max_length=20)
    last_update = peewee.TimestampField()

    class Meta:
        db_table = 'language'

class Film(BaseModel):

    film_id = peewee.SmallIntegerField(primary_key=True)
    title = peewee.CharField(index=True)
    description = peewee.TextField(null=True)
    release_year = peewee.DateField(formats="%Y")

    language = peewee.ForeignKeyField(Language)
    length = peewee.SmallIntegerField()
    last_update = peewee.TimestampField()

    def json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))


    def to_dict(self):
        return {
            'film_id': self.film_id,
            'title': self.title,
            'description':  self.description,
            'release_year': self.release_year,
            'language': self.language.name,
            'length': self.length,
        }

    class Meta:
        db_table = 'film'
        