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

# Toggle if browser is headless or not


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
        checked_element = (By.XPATH, "//div[contains(@class, 'print-nobreak')]/div")
    else:  # Old viewer checked element
        checked_element = (By.XPATH, '//*[@id="ttonline_printpreview"]/div')

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
    global browser
    new_viewer = Config.Settings.Scraper.UseNewMethod  # Check if new viewer enabled in settings

    print('Locating and parsing SVG elements!')
    # Check if the new/testing version of the timetable viewer is being used.
    if new_viewer:  # Use the XPATH for the new version viewer
        path = "//div[contains(@class, 'print-nobreak')]/div//*[name()='svg']//*[name()='g']//*[name()='rect']//*[name()='title']"

    else:  # Use the XPATH for the old version viewer
        path = "//div[contains(@class, 'print-sheet')]//*[name()='svg']//*[name()='g']//*[name()='rect']//*[name()='title']"

    stundas = browser.find_elements_by_xpath(path)

    return stundas


def scrapeClasses():
    # Get document from link and make a html tree out of it
    response = requests.get('https://ogrestehnikums.edupage.org/timetable/view.php?num=16&class=-71')
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
            output_json[str(row['name'])] = 'https://ogrestehnikums.edupage.org/timetable/view.php?num=16&class=' + row['id']

        # Outputs file to a json file
        json.dump(output_json, open('classes.json', 'w'), indent=4, ensure_ascii=False)
    else:
        print("Scraping failed with status code: " + response.status_code)


def closeBrowser():
    global browser

    if Config.Settings.Browser.Close:
        print('Closing browser!')
        browser.quit()
    else:
        print('Keeping browser open for development!')
