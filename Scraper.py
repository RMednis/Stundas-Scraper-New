# MedsNET Timetable Scraper
# Scraper
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020


from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time


# url = 'https://ogrestehnikums.edupage.org/timetable/view.php?num=12&class=-80  # Weird cell link

browser = 0

# Toggle if browser is headless or not

def startBrowser(url):
    global browser
    opts = Options()
    headless_check = False

    print('Headless: ', headless_check)
    print('URL:      ', url)
    opts.headless = headless_check  # Sets headless state based off the headless_check setting

    print('Launching browser...')
    browser = Firefox(options=opts)  # Launches the browser with options set above

    print('Navigating to ', url)
    browser.get(url)  # Opens the url set above

    # Wait for the page to load or timeout!
    try:
        print('Waiting for page JS to load...')
        WebDriverWait(browser, 6).until(EC.presence_of_element_located((By.ID, 'ttonline_printpreview')))
        print('JS Loaded!')

    except TimeoutException:
        print("Failed - Timeout loading main page!")  # Error Message
        exit(100)  # Exit Gracefully


def scrapeStundas():
    global browser
    print('Locating and parsing SVG elements!')

    stundas = browser.find_elements_by_xpath(
        "//div[contains(@class, 'print-sheet')]//*[name()='svg']//*[name()='g']//*[name()='rect']//*[name()='title']")

    return stundas


def closeBrowser():
    global browser

    print('Closing browser!')
    browser.quit()
