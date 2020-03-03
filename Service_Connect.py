# MedsNET Timetable Scraper
# API Generator / DB Connector
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020

from pymongo import MongoClient
import datetime
import Config
import json

'''
This script contains the functions necessary for generating and exporting a JSON API response to file, or 
exporting it to a MongoDB document for later use with an frontend application or for web API generation.
'''

'''
Database Export Functions
'''


# Function, to connect to the MongoDB Database
def export_to_mongo(collection_name, data):
    #  TODO: Possibly seperate this into multiple functions!
    settings = Config.Settings  # Makes the settings object easier to use
    client = MongoClient(
        settings.Database.IP,  # The Mongo server ip, pulled from config
        username=settings.Database.User,  # The Mongo user, also from config
        password=settings.Database.Pass,  # The Auth password
        authSource=settings.Database.Database,  # The database used for auth
        authMechanism='SCRAM-SHA-256'  # The auth mechanism, should possibly make it configurable
    )
    database = client[settings.Database.Database]  # Gets the database, in which to write from the config file
    collection = database[collection_name]  # Gets the current collection from the DB

    # TODO: Fix this hacky mess, instead of converting to JSON than dropping that in, we should find a way to do that
    #  directly!

    object_json = json.dumps(data, default=lambda x: x.__repr__, ensure_ascii=False,
                             indent=4)  # Converts to json corectly
    object_json = json.loads(object_json)  # Reads the json string

    # Sample data model
    db_data = {
        "class": "3DT-1",  # TODO: Make this dynamic!
        "updated": datetime.datetime.now(),  # Gets the update time dynamically.
        "lessons": object_json  # The actual week lesson object!
    }

    collection.insert_one(db_data)  # Places the created object into the database!


'''
File Export Functions
'''


# Function, that exports the JSON response to a file
# TODO: Make it actually export to file, not just print!
def ExportToFile(object):
    object_json = json.dumps(object, default=lambda x: x.__repr__, ensure_ascii=False, indent=4)
    print(object_json)


'''
Other export options
'''
# Function, that prints the response in console
# Should be used for development only!