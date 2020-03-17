'''
Configuration file creation

Reads and creates the configuration data required for changing vars, selecting steps, etc.
The default file is config.ini, it gets created when you first execute this script.
'''
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
    # Execution steps!
    config['STEPS'] = {
        'Scraper': 'True',
        'Sorter': 'True',
        'APIGenerate': 'True'
    }

    # Browser scraper settings
    config['BROWSER'] = {
        'BrowserHeadless': 'True',
        'ScrapeURL': 'https://ogrestehnikums.edupage.org/timetable/',
        'CloseAfter': 'False'
    }

    config['SCRAPER'] = {
        'NewViewer': 'False',
        'ScrapeAllTables': 'False'
    }

    config['DATABASE'] = {
        'Used': 'False',
        'IP': 'localhost',
        'Port': '27017',
        'Database': 'Stundas',
        'User': 'User',
        'Password': 'P@ssW0rd!'
    }

    # Checks if a config file already exists, if it doesn't, creates a default one!
    if not config.read(configPath):
        print('No {} file found! Creating a default one!'.format(configPath))
        print('Please update the values as needed!')
        with open(configPath, 'w') as configfile:
            config.write(configfile)
        exit(1)

    class Settings:
        class Browser:
            Headless = config['BROWSER'].getboolean('BrowserHeadless')
            URL = config['BROWSER']['ScrapeURL']
            Close = config['BROWSER'].getboolean('CloseAfter')

        class Scraper:
            UseNewMethod = config['SCRAPER'].getboolean('NewViewer')
            Scrape_All = config['SCRAPER'].getboolean('ScrapeAllTables')

        class Database:
            Enabled = config['DATABASE'].getboolean('Used')
            IP = config['DATABASE']['IP']
            Port = config['DATABASE']['Port']
            Database = config['DATABASE']['DATABASE']
            User = config['DATABASE']['User']
            Pass = config['DATABASE']['Password']
