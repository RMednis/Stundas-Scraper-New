# MedsNET Timetable Scraper
# Main Execution file
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020
import configparser
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

# Start web browser
Scraper.startBrowser(Config.Settings.Browser.URL)

# Scrape initial page
Scraped_Data = Scraper.scrapeStundas()

# Sort scraped data
Current_Lessons = Sorter.DaySorter(Scraped_Data)

# TODO: Use selector in settings to see, which export method to use!
# Service_Connect.export_to_mongo('Skoleni', Current_Lessons)
print(Current_Lessons)

# Close browser cleanly, if selected
Scraper.closeBrowser()
