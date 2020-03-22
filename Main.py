# MedsNET Timetable Scraper
# Main Execution file
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020
import configparser

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import Sorter
import Scraper
import Config
import Service_Connect

print('----------------------------------------------------')
print('Timetable Scraping, Sorting and API creation script!')
print('Reinis Gunārs Mednis, Ikars Melnalksnis - 2020')
print('----------------------------------------------------')

'''
Data Scraping
'''

# Generates the config file, if first launch
Config.FirstLaunch()

# Initialization
if Config.Settings.Database.Enabled:
    # Connects to the Database
    Database = Service_Connect.connect_to_mongo()
else:
    # Creates the directory structure required, deletes old data
    Service_Connect.json_initialize()

# Start web browser
Scraper.startBrowser(Config.Settings.Browser.URL)

# Scrape class list
ClassList = Scraper.scrapeList()

# Scrape classes
# Scraper.scrapeClasses(Config.Settings.Browser.URL)

# Scrape initial page
Scraped_Data = Scraper.scrapeStundas()

# Sort scraped data
Current_Lessons = Sorter.DaySorter(Scraped_Data)

# Depending on settings it will either export to database or json file
if Config.Settings.Database.Enabled:
    # Generates a DB data model from the returned data
    Database_model = Service_Connect.make_data_model(Current_Lessons[0], Current_Lessons[1])
    # Pass the modeled data to the DB
    Service_Connect.export_to_mongo(Database, 'Skoleni', Database_model)

    Service_Connect.export_to_mongo(Database, "Klases", ClassList[0])
else:
    # Exports lesson data to file
    Service_Connect.export_to_json(Current_Lessons)

print(Current_Lessons)

# Close browser cleanly, if selected
Scraper.closeBrowser()
