# MedsNET Timetable Scraper
# API Generator / DB Connector
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020
"""
This script contains the functions necessary for generating and exporting a JSON API response to file, or
exporting it to a MongoDB document for later use with an frontend application or for web API generation.
"""

import datetime
import json
import os
import shutil

from pymongo import MongoClient

import Config

'''
Utility functions
'''


def make_data_model(lesson_data, class_name):
    """
    Makes a data model from sorter data object

    :param lesson_data: Week object
    :param class_name: Name of the scraped class
    :return:
    """

    now = datetime.datetime.now()  # Get the current time
    now = str(now.replace(microsecond=0).isoformat())  # Drop microseconds, covert to ISO 8601

    return {
        "name": class_name,  # Returns the class/room/teacher name
        "updated": now,  # The update time, formatted to ISO8601
        "lessons": json.loads(json.dumps(lesson_data, default=lambda x: x.get_dict()))  # Dump/load data to json
    }


# Function that prints current collection, mainly for debugging
def print_db(collection):
    for x in collection.find():
        print(x)


'''
Database Export Functions
'''


def connect_to_mongo():
    """
    Connects to MongoDB

    :return: Database object!
    """
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
    """
    Drops a collection from the database!

    :param database: Database to drop from
    :param collection_name: Name of the collection to drop
    """
    database.drop_collection(collection_name)  # Deletes previous db collection


# Export the data to a mongodb collection
def export_to_mongo(database, collection_name, data):
    """
    Export data to a mongoDB database!

    :param database: Database to export to
    :param collection_name: Name of the collection to export to
    :param data: Data to export
    """
    collection = database[collection_name]  # Gets the current collection from the DB

    if type(data) is list:
        collection.insert_many(data)
    else:
        collection.insert_one(data)


def list_export(object_list, name, database):
    """
    Exports a dropdown list object to MongoDB

    :param object_list: List to export
    :param name: Name of the list
    :param database: Database to export to!
    """

    now = datetime.datetime.now()  # Get the current time
    now = str(now.replace(microsecond=0).isoformat())  # Drop microseconds, covert to ISO 8601

    data_list = {
        "name": name,
        "updated": now,
        "list": object_list
    }

    export_to_mongo(database, Config.Settings.Scraper.List_Name, data_list)


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
