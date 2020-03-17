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

# Start web browser
Scraper.startBrowser(Config.Settings.Browser.URL)

SelectorButton = Scraper.browser.find_element(By.XPATH, "//div[contains(@class, 'asc-ribbon')]//div[contains(@class, "
                                                        "'left')]//span[text()='Classes']")

# Click on class selector
# Open selection list
SelectorButton.click()
SelectionItems = Scraper.browser.find_elements_by_xpath("//div[contains(@class, 'asc dropDown')]"
                                                       "//ul[contains(@class, 'dropDownPanel asc-context-menu')]/li/a")
print(len(SelectionItems))
for item in SelectionItems:
    print(item.get_attribute('innerHTML'))

# Scrape classes
Scraper.scrapeClasses()

# Scrape initial page
Scraped_Data = Scraper.scrapeStundas()

# Sort scraped data
Current_Lessons = Sorter.DaySorter(Scraped_Data)

# Depending on settings it will either export to database or json file
if Config.Settings.Database.Enabled:
    Service_Connect.export_to_mongo('Skoleni', Current_Lessons)
else:
    Service_Connect.export_to_json(Current_Lessons)

print(Current_Lessons)

# Close browser cleanly, if selected
Scraper.closeBrowser()
