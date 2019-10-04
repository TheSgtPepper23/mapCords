from enum import Enum, auto


class Errors(Enum):
    '''Enumeration for especify errors'''
    NotFound = "The map doesn't exists"
    LocationNotFound = "This map doesn't have locations with that name"
    CantDelete = "It was not possible to delete the map"
    CantCreate = "Could not create the location"
    AlreadyExists = "There is already a map with that name"
    WrongValue = "Wrong value"
    AppError = "An error has ocurred."


class Messages(Enum):
    '''Enumeration for pre-defined success messages'''
    MapCreated = "Map created!"
    LocationCreated = "The location has been created"
    NoLocationsAsociated = "There are no locations registered on this map"
    NoLocationsFound = "There are no locations that match that word"
    MapDeleted = "The map has been deleted!"
    LocationDeleted = "The locations has been removed!"


def print_enum(error_enum):
    try:
        print(error_enum.value)
    except AttributeError:
        print(Errors.AppError.value)
