from models import Map, Location
import unittest
from peewee import DoesNotExist, IntegrityError
from datetime import datetime
from global_var import Errors, Messages


class MapQueries:
    '''Contains the methods to interact with the database'''

    def __init__(self, name):
        self.name = name

    def get_map_db(self):
        '''Return a database object with the name of the 
        map or raises an error if it doesn't exist.'''
        try:
            return Map.get(Map.name == self.name)
        except DoesNotExist:
            raise DoesNotExist

    def create(self):
        '''Creates a new map in the database. If Ok return True. 
        If the name alreadyexists returns Errors.AlreadyExists'''
        try:
            mapa = Map.create(name=self.name)
            return Messages.MapCreated
        except IntegrityError:
            return Errors.AlreadyExists

    def delete(self):
        '''Deletes the map from the database. Returns a Message.
        MapDeleted if success and Errors.NoFound otherwhise'''
        try:
            mapa = self.get_map_db()
            mapa.delete_instance(recursive=True)
            return Messages.MapDeleted
        except DoesNotExist:
            return Errors.NotFound

    def retrieve_info(self):
        '''Gives back info about the map: It's name, 
        date of cration and number of locations in that order.'''
        try:
            mapa = self.get_map_db()
            return (mapa.name, mapa.creation, len(mapa.locations))
        except DoesNotExist:
            return Errors.NotFound

    def retrieve_locations(self):
        '''Returns all the locations related to the map. 
        It could be an empty list.
        If the map doesn't exists it returns Errors.NotFound'''
        try:
            mapa = self.get_map_db()
            return mapa.locations
        except DoesNotExist:
            return Errors.NotFound

    def filter_locations(self, keyword):
        '''Return all the locations related to the map that 
        contain the keyword. It can be an empty list. 
        If the map doesn't exist returns Errors.NotFound
        keyword: str'''
        try:
            mapa = self.get_map_db()
            return Location.select().where(Location.name.contains(
                keyword) and Location.owner_map == mapa)
        except DoesNotExist:
            return Errors.NotFound


class LocationQueries:
    def __init__(self, name, pos_x, pos_y, pos_z, mapa):
        '''
        Creates a new instance of LocationQueries and validate 
        the fields. If one of the fields is not the correct 
        type it'll raise an exception.
        name : str,
        pos_x, pos_y, pos_z : int,
        mapa : MapQueries
        '''
        for el in [pos_x, pos_y, pos_z]:
            if type(el) != int:
                raise TypeError
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        try:
            self.mapa = mapa.get_map_db()
        except IntegrityError:
            raise IntegrityError

    @classmethod
    def get_by_id(cls, id):
        try:
            return Location.get(Location.id == id)
        except DoesNotExist:
            return Errors.LocationNotFound

    def create(self):
        '''Creates a new location object in the database. 
        If success returns Messages.LocationCreated, if not
        returns Error.CantCreate'''
        try:
            Location.create(
                name=self.name,
                x_val=self.pos_x,
                y_val=self.pos_y,
                z_val=self.pos_z,
                owner_map=self.mapa)
            return Messages.LocationCreated
        except:
            return Errors.CantCreate

    def get_location_db(self):
        try:
            return Location.get(Location.name ==
                                self.name and Location.owner_map == self.mapa)
        except DoesNotExist:
            raise DoesNotExist

    def delete(self):
        try:
            self.get_location_db().delete_instance()
            return Messages.LocationDeleted
        except DoesNotExist:
            return Errors.NotFound


class Test(unittest.TestCase):

    def setUp(self):
        self.map_query = MapQueries("TestMAP")
        self.map_query_created = Map.create(name="LocationMap")
        self.loc_query_created = Location.create(
            name="location1",
            x_val=503,
            y_val=64,
            z_val=40,
            owner_map=self.map_query_created)

    def test_a_create_map(self):
        self.assertEqual(self.map_query.create(), Messages.MapCreated)
        self.assertEqual(self.map_query.create(), Errors.AlreadyExists)

    def test_b_create_location(self):
        self.loc_query = LocationQueries(
            "Calabozo", 192, 24, -1255, self.map_query)
        self.assertEqual(self.loc_query.create(), Messages.LocationCreated)

    def test_c_retrieve_map(self):
        not_exists = MapQueries("Mapa1")
        self.assertEqual(not_exists.retrieve_info(), Errors.NotFound)
        self.assertEqual(self.map_query.retrieve_info()[0], "TestMAP")

    def test_d_retrieve_map_location(self):
        mapa = MapQueries("LocationMap")
        loc = mapa.retrieve_locations()
        self.assertEqual(loc[0], self.loc_query_created)

    def test_e_filter_locations(self):
        lista = self.map_query.filter_locations("Cal")
        self.assertEqual(lista[0].name, "Calabozo")

    def test_y_delete_location(self):
        loc_query = LocationQueries(
            "Calabozo 2", 192, 24, -1255, self.map_query)
        loc_query.create()
        self.assertEqual(loc_query.delete(), Messages.LocationDeleted)

    def test_z_delete_map(self):
        # It has the z in the name in order to run it at the end
        self.assertEqual(self.map_query.delete(), Messages.MapDeleted)
        not_exists = MapQueries("NonExistant")
        self.assertEqual(not_exists.delete(), Errors.NotFound)

    def tearDown(self):
        self.map_query_created.delete_instance(recursive=True)


if __name__ == "__main__":
    #Map.get(Map.name == "LocationMap").delete_instance(recursive=True)
    # print(len(Map.select()))
    unittest.main()
