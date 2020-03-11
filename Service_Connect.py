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
Utility functions
'''


# Function that makes a data model from sorter data object
def make_data_model(data, class_name):
    return {
                "updated": str(datetime.datetime.now()),  # Gets the update time dynamically.
                "lessons": json.loads(json.dumps(data, default=lambda x: x.get_dict())),    # Dump/load data to json
                "class": class_name
           }


# Function that prints current collection, mainly for debugging
def print_db(collection):
    for x in collection.find():
        print(x)


'''
Database Export Functions
'''


# Function, to connect to the MongoDB Database
def export_to_mongo(collection_name, data):
    #  TODO: Possibly seperate this into multiple functions!
    settings = Config.Settings  # Makes the settings object easier to use
    class_name = data['class']

    client = MongoClient(
        settings.Database.IP,  # The Mongo server ip, pulled from config
        username=settings.Database.User,  # The Mongo user, also from config
        password=settings.Database.Pass,  # The Auth password
        authSource=settings.Database.Database,  # The database used for auth
        authMechanism='SCRAM-SHA-256'  # The auth mechanism, should possibly make it configurable
    )
    database = client[settings.Database.Database]  # Gets the database, in which to write from the config file

    database.drop_collection(collection_name)  # Deletes previous db collection
    collection = database[collection_name]  # Gets the current collection from the DB

    collection.insert_one(make_data_model(data, class_name))  # Insert db template

    print_db(collection)
    # TODO: Fix this hacky mess, instead of converting to JSON than dropping that in, we should find a way to do that
    #  directly!


'''
File Export Functions
'''


# Function, that exports the JSON response to a file
def export_to_json(data):
    # Creates a template and saves it to a file
    json.dump(make_data_model(data, data['class']), open(data['class'] + '_data.json', 'w'), ensure_ascii=False, indent=4)


'''
Other export options
'''
# Function, that prints the response in console
# Should be used for development only!
