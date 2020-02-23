# MedsNET Timetable Scraper
# Main Execution file
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020
import configparser
import Sorter
import Scraper
import API_Generate

print('----------------------------------------------------')
print('Timetable Scraping, Sorting and API creation script!')
print('Reinis Gunārs Mednis, Ikars Melnalksnis - 2020')
print('----------------------------------------------------')

'''
Configuration file creation

Reads and creates the configuration data required for changing vars, selecting steps, etc.
The default file is config.ini, it gets created when you first execute this script.
'''

config = configparser.ConfigParser()
configPath = 'config.ini'

# Default configuration!

# Execution steps!
config['STEPS'] = {
    'Scraper': 'True',
    'Sorter': 'True',
    'APIGenerate': 'True'
}

# Browser scraper settings
config['BROWSER'] = {
    'BrowserHeadless': 'True',
    'ScrapeURL': 'https://ogrestehnikums.edupage.org/timetable/view.php?num=12&class=-114'
}

# Checks if a config file already exists, if it doesn't, creates a default one!
if not config.read(configPath):
    print('No {} file found! Creating a default one!'.format(configPath))
    with open(configPath, 'w') as configfile:
        config.write(configfile)


class Settings:
    class Scraper:
        Headless = config['BROWSER']['BrowserHeadless']
        URL = config['BROWSER']['ScrapeURL']


'''
Data Scraping
'''

# Start web browser
Scraper.startBrowser(Settings.Scraper.URL)

# Scrape initial page
Scraped_Data = Scraper.scrapeStundas()

# Sort scraped data
Test = Sorter.DaySorter(Scraped_Data)

print(Test)

# Close browser cleanly
Scraper.closeBrowser()
