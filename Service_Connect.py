# MedsNET Timetable Scraper
# API Generator / DB Connector
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020

import datetime
import json
import os
import shutil

from pymongo import MongoClient

import Config

'''
This script contains the functions necessary for generating and exporting a JSON API response to file, or 
exporting it to a MongoDB document for later use with an frontend application or for web API generation.
'''

'''
Utility functions
'''


# Function that makes a data model from sorter data object
def make_data_model(lesson_data, class_name):
    return {
        "class": class_name,  # Returns the class name
        "updated": str(datetime.datetime.now()),  # Gets the update time dynamically.
        "lessons": json.loads(json.dumps(lesson_data, default=lambda x: x.get_dict()))  # Dump/load data to json
    }


def list_export(object_list, name, database):
    data_list = {
        "name": name,
        "updated": str(datetime.datetime.now()),
        "dropdown_list": object_list
    }

    export_to_mongo(database, "Saraksti", data_list)


# Function that prints current collection, mainly for debugging
def print_db(collection):
    for x in collection.find():
        print(x)


'''
Database Export Functions
'''


# Function, to connect to the MongoDB Database
def connect_to_mongo():
    settings = Config.Settings  # Makes the settings object easier to use

    client = MongoClient(
        settings.Database.IP,  # The Mongo server ip, pulled from config
        username=settings.Database.User,  # The Mongo user, also from config
        password=settings.Database.Pass,  # The Auth password
        authSource=settings.Database.Database,  # The database used for auth
        authMechanism='SCRAM-SHA-256'  # The auth mechanism, should possibly make it configurable
    )
    database = client[settings.Database.Database]  # Gets the database, in which to write from the config file

    return database  # Returns database to caller function


# Drop collection
def drop_collection(database, collection_name):
    database.drop_collection(collection_name)  # Deletes previous db collection


# Export the data to a mongodb collection
def export_to_mongo(database, collection_name, data):
    collection = database[collection_name]  # Gets the current collection from the DB

    if type(data) is list:
        collection.insert_many(data)
    else:
        collection.insert_one(data)


'''
File Export Functions
'''


# Function, that exports the JSON response to a file
def lessons_to_json(lesson_data, class_name):
    # Generates a file path by taking the class name, appending a suffix and placing it in the designated folder.
    file = open(Config.Settings.File.Path + class_name + Config.Settings.File.Suffix, 'w')

    # Creates a template and saves it to a file
    json.dump(make_data_model(lesson_data, class_name), file, ensure_ascii=False, indent=4)


def list_to_json(dropdown_list, name):
    # Generates a file path by taking the class name, appending a suffix and placing it in the designated folder.
    file = open(Config.Settings.File.Path + name + '.json', 'w')

    # Creates a template and saves it to a file
    json.dump(dropdown_list, file, ensure_ascii=False, indent=4)


def json_initialize():
    folder = Config.Settings.File.Path

    if os.path.isdir(folder):
        print("Removing old data directory!")
        shutil.rmtree(folder)

    try:
        print("Creating new directory in ", folder)
        os.mkdir(folder)
    except OSError:
        print("Could not create directory in ", folder)
    else:
        print("Path Created Successfully!")


'''
Other export options
'''
# Function, that prints the response in console
# Should be used for development only!
