# MedsNET Timetable Scraper
# Scraper
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020

import requests, json
from lxml import html
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import Config

browser = 0


def startBrowser(url):
    global browser
    opts = Options()
    headless_check = Config.Settings.Browser.Headless
    new_viewer = Config.Settings.Scraper.UseNewMethod

    # Print current config to console for debugging
    print('Headless: ', headless_check)
    print('URL:      ', url)
    print('New Viewer:', new_viewer)

    opts.headless = headless_check  # Sets headless state based off the headless_check setting

    # Sets which div will be checked to determine when the page has fully loaded depending on version
    if new_viewer:  # New viewer checked element
        checked_element = (By.XPATH, "//div[contains(@class, 'print-nobreak')]/div//*[name()='svg']")
    else:  # Old viewer checked element
        checked_element = (By.XPATH, '//*[@id="ttonline_printpreview"]/div//*[name()="svg"]')

    print('Launching browser...')
    browser = Firefox(options=opts)  # Launches the browser with options set above

    print('Navigating to ', url)
    browser.get(url)  # Opens the url set above

    # Wait for the page to load or timeout!
    try:
        print('Waiting for page JS to load...')
        WebDriverWait(browser, 10).until(EC.presence_of_element_located(checked_element))  # Waits until element appears
        print('JS Loaded!')

    except TimeoutException:  # The page took too long to load!
        print("Failed - Timeout loading main page!")  # Error Message
        closeBrowser()
        exit(100)  # Exit Gracefully


def scrapeStundas():
    new_viewer = Config.Settings.Scraper.UseNewMethod  # Check if new viewer enabled in settings

    print('Locating and parsing SVG elements!')
    # Check if the new/testing version of the timetable viewer is being used.
    if new_viewer:  # Use the XPATH for the new version viewer
        path = "//div[contains(@class, 'print-nobreak')]/div//*[name()='svg']//*[name()='g']//*[name()='rect']//*[name()='title']"
        path_class_name = "//div[contains(@class, 'print-nobreak')]//*[name()='svg']//*[name()='g']//*[name()='text' and @y='166.875']"
    else:  # Use the XPATH for the old version viewer
        path = "//div[contains(@class, 'print-sheet')]//*[name()='svg']//*[name()='g']//*[name()='rect']//*[name()='title']"
        path_class_name = "//div[contains(@class, 'print-sheet')]//*[name()='svg']//*[name()='g']//*[name()='text' and @y='166.875']"

    stundas = browser.find_elements_by_xpath(path)
    class_name = browser.find_element(By.XPATH, path_class_name).get_property('innerHTML').splitlines()

    # Returns both the class name and the list of table objects.
    return [stundas, class_name]


# TODO: Rewrite this!
"""
def scrapeClasses(url):
    # Get document from link and make a html tree out of it
    response = requests.get(url)
    if response.status_code == 200:
        page_tree = html.fromstring(response.content)

        # Find all scripts and remove newline chars
        scripts = str(page_tree.xpath('//script[@type="text/javascript"]/text()')).replace('\\n', '')

        # Find the start/end of the required json file
        start = scripts.find('{"table":"classes"')
        end = scripts.find(',{"table":"subjects"')

        # Make the json from scripts char array
        found_json = json.loads(scripts[start:end].replace("\'", ""))

        # Dict that will hold scraped info from found_json
        output_json = {}

        for row in found_json['rows']:
            # Each class has link with its own id
            output_json[str(row['name'])] = 'https://ogrestehnikums.edupage.org/timetable/view.php?num=16&class=' + row[
                'id']

        # Outputs file to a json file
        json.dump(output_json, open('classes.json', 'w'), indent=4, ensure_ascii=False)
    else:
        print("Scraping failed with status code: " + response.status_code)
"""


# Scrapes the list of people/classes/rooms from the page dropdown, so we know what
def scrapeList():
    global browser
    new_viewer = Config.Settings.Scraper.UseNewMethod

    if new_viewer:  # Use the XPATH for the new version viewer
        path = "//div[contains(@class, 'asc dropDown')]//ul[contains(@class, 'dropDownPanel asc-context-menu')]/li/a"
        button_path = "//div[@id='fitheight']//div/span[@title='Classes']"
    else:  # Use the XPATH for the old version viewer
        path = "//div[contains(@class, 'asc dropDown')]//ul[contains(@class, 'dropDownPanel asc-context-menu')]/li/a"
        button_path = "//div[contains(@class, 'asc-ribbon')]//div[contains(@class, 'left')]//span[text()='Classes']"
    print('Scraping teacher/room/class list!')

    SelectorButton = browser.find_element(By.XPATH, button_path)

    # Click on class selector
    # Open selection list
    SelectorButton.click()

    ListItems = browser.find_elements(By.XPATH, path)
    names = list()

    for item in ListItems:
        name = {
            "name": item.get_attribute('innerHTML')
        }

        names.append(name)

    print(ListItems)
    return names, ListItems


def closeBrowser():
    global browser

    if Config.Settings.Browser.Close:
        print('Closing browser!')
        browser.quit()
    else:
        print('Keeping browser open for development!')
