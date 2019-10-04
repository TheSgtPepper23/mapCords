from peewee import SqliteDatabase, CharField, IntegerField, ForeignKeyField, Model, DateField
from datetime import datetime

coordinates_db = SqliteDatabase('./coordinates.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64,
    'foreign_keys': 1,
    'ignore_check_constraints': 0, })


class _BaseModel(Model):
    class Meta:
        database = coordinates_db


class Map(_BaseModel):
    name = CharField(max_length=255, unique=True)
    creation = DateField('%Y-%m-%d', default=datetime.now)


class Location(_BaseModel):
    name = CharField(max_length=255)
    x_val = IntegerField()
    y_val = IntegerField()
    z_val = IntegerField()
    owner_map = ForeignKeyField(Map, backref="locations", on_delete="CASCADE")

    def __str__(self):
        return f"{self.id}) {self.name}: {self.x_val}, {self.y_val}, {self.z_val}"


def create_ifnot_exist():
    coordinates_db.connect()
    if not coordinates_db.table_exists(Map) and not coordinates_db.table_exists(Location):
        coordinates_db.create_tables([Map, Location])
    coordinates_db.close()
