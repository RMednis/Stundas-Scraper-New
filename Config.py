# MedsNET Timetable Scraper
# Config support functions/classes
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020
"""
Configuration file creation

Reads and creates the configuration data required for changing vars, selecting steps, etc.
The default file is config.ini, it gets created when you first execute this script.
"""
import configparser

global config
global configPath
global Settings


# Default configuration!
def FirstLaunch():
    global config
    global configPath
    global Settings

    config = configparser.ConfigParser()

    configPath = 'config.ini'

    # Stages
    config['STAGES'] = {
        'Students': 'True',
        'Teachers': 'True',
        'Classrooms': 'True'
    }

    # Browser settings
    config['BROWSER'] = {
        'Browser_Headless': 'True',
        'Scrape_URL': 'https://ogrestehnikums.edupage.org/timetable/',
        'Close_After': 'True'
    }

    # Scraper settings
    config['SCRAPER'] = {
        'New_Viewer': 'False',
        'List_Name': 'Saraksti',
        'Student_Name': 'Studenti',
        'Teacher_Name': 'Skolotaji',
        'Room_Name': 'Telpas'
    }

    # Database settings
    config['DATABASE'] = {
        'Used': 'False',
        'IP': 'localhost',
        'Port': '27017',
        'Database': 'Stundas',
        'User': 'User',
        'Password': 'P@ssW0rd!',
        'Table_Collection_Prefix': 'Tabulas_'
    }

    # File export settings
    config['FILE'] = {
        'Used': 'False',
        'Path': './Export/',
        'Suffix': '_data.json'
    }

    # Checks if a config file already exists, if it doesn't, creates a default one!
    if not config.read(configPath):
        print('No {} file found! Creating a default one!'.format(configPath))
        print('Please update the values as needed!')
        with open(configPath, 'w') as configfile:
            config.write(configfile)
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
            Use_New_Method = config['SCRAPER'].getboolean('New_Viewer')
            Student_Table_Name = config['SCRAPER']['Student_Name']
            Teacher_Table_Name = config['SCRAPER']['Teacher_Name']
            Room_Table_Name = config['SCRAPER']['Room_Name']
            List_Name = config['SCRAPER']['List_Name']

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
