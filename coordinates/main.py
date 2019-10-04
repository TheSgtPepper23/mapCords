from queries import MapQueries, LocationQueries
from global_var import Errors, Messages, print_enum
from sys import argv
import argparse
from models import create_ifnot_exist


def initializa_parser():
    parser = argparse.ArgumentParser(prog="coordinates")
    parser.add_argument("map", metavar="MAP_NAME", type=str)
    mutually_exclusive = parser.add_mutually_exclusive_group()
    mutually_exclusive.add_argument(
        "-l", "--list", action="store_true",
        help="Lists all the locations in a map")
    mutually_exclusive.add_argument(
        "-f", "--find", help="Finds a location that contains KEYWORD",
        metavar="KEYWORD")
    mutually_exclusive.add_argument(
        "-n", "--new", nargs=4, metavar=("NAME", "X", "Y", "Z"),
        help="Adds a new location. Takes " +
        "the location name, and then X, Y and Z in that order")
    mutually_exclusive.add_argument(
        "-c", "--create", help="Creates a new map. There only can be a map with one name.",
        action="store_true")
    mutually_exclusive.add_argument(
        "-d", "--delete", const="-1", nargs="?", metavar="LOCATION_ID", type=int,
        help="This options deletes the map.If an id is specifated, deletes the location")

    return parser


if __name__ == "__main__":
    create_ifnot_exist()
    parser = initializa_parser()
    args = parser.parse_args()

    map_name = args.map
    map_queries = MapQueries(map_name)

    if args.list:
        result = map_queries.retrieve_locations()
        try:
            if len(result) == 0:
                print_enum(Messages.NoLocationsAsociated)
            else:
                for location in result:
                    print(location)
        except TypeError:  # Errors.NotFound is not iterable
            print_enum(result)

    elif args.create:
        print_enum(map_queries.create())
    elif args.find != None:
        result = map_queries.filter_locations(args.find)
        try:
            if len(result) == 0:
                print_enum(Messages.NoLocationsFound)
            else:
                for location in result:
                    print(location)
        except TypeError:
            print_enum(result)
    elif args.delete != None:
        if args.delete == -1:
            result = map_queries.delete()
            print_enum(result)
        else:
            location = LocationQueries.get_by_id(args.delete)
            try:
                loc_query = LocationQueries(
                    location.name, location.x_val,
                    location.y_val, location.z_val,
                    map_queries)
                loc_query.delete()
                print_enum(Messages.LocationDeleted)
            except AttributeError:
                print_enum(location)

    elif args.new != None:
        loc_name = args.new[0]
        details = list(map(lambda val: int(val), args.new[1:]))
        print(details)
        loc_query = LocationQueries(
            args.new[0], details[1], details[2], details[2], map_queries)
        result = loc_query.create()
        print_enum(result)

    else:
        info = map_queries.retrieve_info()
        try:
            print(f"Name: {info[0]}\nDate: {info[1]}\nLocations: {info[2]}")
        except TypeError:
            print_enum(info)
