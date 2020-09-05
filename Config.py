# MedsNET Timetable Scraper
# Config support functions/classes
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020
"""
Configuration file creation

Reads and creates the configuration data required for changing vars, selecting steps, etc.
The default file is config.ini, it gets created when you first execute this script.
"""
import configparser
import os

global config
global configPath
global Settings


# Default configuration!
def first_launch():
    global config
    global configPath
    global Settings

    config = configparser.ConfigParser()

    configPath = 'config.ini'

    # Stages
    config['STAGES'] = {
        'Students': os.getenv('STAGE_STUDENTS', True),
        'Teachers': os.getenv('STAGE_TEACHERS', True),
        'Classrooms': os.getenv('STAGE_ROOMS', True)
    }

    # Browser settings
    config['BROWSER'] = {
        'Browser_Headless': os.getenv('BROWSER_HEADLESS', True),
        'Scrape_URL': os.getenv('BROWSER_URL', 'https://ogrestehnikums.edupage.org/timetable/'),
        'Close_After': os.getenv('BROWSER_CLOSE', True)
    }

    # Scraper settings
    config['SCRAPER'] = {
        'List_Name': os.getenv('SCRAPER_LIST_NAME', 'Saraksti'),
        'Student_Name': os.getenv('SCRAPER_STUDENT_NAME', 'Studenti'),
        'Teacher_Name': os.getenv('SCRAPER_TEACHER_NAME', 'Skolotaji'),
        'Room_Name': os.getenv('SCRAPER_ROOM_NAME', 'Telpas'),
        'Time_Export': os.getenv('SCRAPER_TIME_EXPORT', False)
    }

    # Database settings
    config['DATABASE'] = {
        'Used': os.getenv('MONGO_ENABLED', False),
        'IP': os.getenv("MONGO_IP", 'localhost'),
        'Port': os.getenv("MONGO_PORT", '27017'),
        'Database': os.getenv("MONGO_DATABASE", 'Stundas'),
        'User': os.getenv("MONGO_USER", 'User'),
        'Password': os.getenv("MONGO_PASSWORD", 'P@ssW0rd!'),
        'Table_Collection_Prefix': os.getenv("MONGO_COLLECTION_PREFIX", 'Tabulas_')
    }

    # File export settings
    config['FILE'] = {
        'Used': os.getenv("FILE_ENABLED", False),
        'Path': os.getenv("FILE_EXPORT_PATH", './Export/'),
        'Suffix': os.getenv("FILE_SUFFIX", '_data.json')
    }

    # Checks if a config file already exists or if running from docker, if not, creates a default one!
    if not config.read(configPath):
        print('No {} file found! Creating a default one!'.format(configPath))

        # Write a default config.ini
        with open(configPath, 'w') as configfile:
            config.write(configfile)

        # Check if running in a docker container or not
        if os.getenv("DOCKER_ENABLED", False):
            print('You are running in a docker container, settings should have been written from ENV automatically.')

        else:
            print('Please update the values as needed!')
            exit(1)

    # Converts configuration settings into an easily accessible class
    class Settings:
        """
        Main Settings class
        """

        class Stages:
            Students = config['STAGES'].getboolean('Students')
            Teachers = config['STAGES'].getboolean('Teachers')
            Classrooms = config['STAGES'].getboolean('Classrooms')

        class Browser:
            Headless = config['BROWSER'].getboolean('Browser_Headless')
            URL = config['BROWSER']['Scrape_URL']
            Close = config['BROWSER'].getboolean('Close_After')

        class Scraper:
            Student_Table_Name = config['SCRAPER']['Student_Name']
            Teacher_Table_Name = config['SCRAPER']['Teacher_Name']
            Room_Table_Name = config['SCRAPER']['Room_Name']
            List_Name = config['SCRAPER']['List_Name']
            Time_Export = config['SCRAPER'].getboolean('Time_Export')

        class Database:
            Enabled = config['DATABASE'].getboolean('Used')
            IP = config['DATABASE']['IP']
            Port = config['DATABASE']['Port']
            Database = config['DATABASE']['DATABASE']
            User = config['DATABASE']['User']
            Pass = config['DATABASE']['Password']
            Table_Prefix = config['DATABASE']['Table_Collection_Prefix']

        class File:
            Path = config['FILE']['Path']
            Enabled = config['FILE'].getboolean('Used')
            Suffix = config['FILE']['Suffix']
