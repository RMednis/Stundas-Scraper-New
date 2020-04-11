# MedsNET Timetable Scraper
# Main Scraper
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import Config

browser = Firefox


# Starts the browser
def start_browser(url):
    global browser
    opts = Options()
    headless_check = Config.Settings.Browser.Headless
    new_viewer = Config.Settings.Scraper.Use_New_Method

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
        print('SVG and JS loaded!')

    except TimeoutException:  # The page took too long to load!
        print("Failed - Timeout loading main page!")  # Error Message
        close_browser()  # Close the browser
        exit(100)  # Exit Gracefully


# Scrapes raw lesson objects from svg
def scrape_stundas():
    new_viewer = Config.Settings.Scraper.Use_New_Method  # Check if new viewer enabled in settings

    print('Locating and parsing SVG elements!')
    # Check if the new/testing version of the timetable viewer is being used.
    if new_viewer:  # Use the XPATH for the new version viewer
        path = "//div[contains(@class, 'print-nobreak')]/div//*[name()='svg']//*[name()='g']//*[name()='rect']//*[name()='title']"
        path_class_name = "//div[contains(@class, 'print-nobreak')]//*[name()='svg']//*[name()='g']//*[name()='text' and @y='166.875']"
    else:  # Use the XPATH for the old version viewer
        path = "//div[contains(@class, 'print-sheet')]//*[name()='svg']//*[name()='g']//*[name()='rect']//*[name()='title']"
        path_class_name = "//div[contains(@class, 'print-sheet')]//*[name()='svg']//*[name()='g']//*[name()='text' and @y='166.875']"

    # Find all the lesson objects in the svg
    stundas = browser.find_elements_by_xpath(path)

    # Find the class name in the svg
    class_name = browser.find_element(By.XPATH, path_class_name).get_property('innerHTML').splitlines()

    # Returns both the class name and the dropdown_list of table objects.
    return [stundas, class_name]


# Opens the dropdown_list
def open_list(list_name):
    global browser
    new_viewer = Config.Settings.Scraper.Use_New_Method

    if new_viewer:  # Use the XPATH for the new version viewer
        button_path = "//div[@id='fitheight']//div/span[@title='{}']".format(list_name)
    else:  # Use the XPATH for the old version viewer
        button_path = "//div[contains(@class, 'asc-ribbon')]//div[contains(@class, 'left')]//span[text()='{}']".format(
            list_name)

    # Find the selector button in the document
    selector_button = browser.find_element(By.XPATH, button_path)

    # Click on the class selector button, to load in the required dropdown elements for scraping.
    selector_button.click()


# Scrapes the dropdown_list of people/classes/rooms from the page dropdown, so we know what
def scrape_list(list_name):
    global browser

    # This XPATH works on both viewer types
    path = "//div[contains(@class, 'asc dropDown')]//ul[contains(@class, 'dropDownPanel asc-context-menu')]/li/a"

    print('Scraping {} dropdown list!'.format(list_name))

    open_list(list_name)

    list_items = browser.find_elements(By.XPATH, path)  # The drop down html elements
    names = list()  # List object to hold the dropdown text content

    # Loop through the elements and get their text content
    for item in list_items:
        name = item.get_attribute('innerHTML')  # Get list name text
        names.append(name)  # Append it to the text content dropdown_list

    return names


# Opens a table based off the class name
def open_table(list_name, class_name):
    global browser
    # Open the classes dropdown
    open_list(list_name)

    # Find the necessary class in the dropdown
    current_class = browser.find_element(By.XPATH,
                                         "//div[contains(@class, 'asc dropDown')]//ul[contains(@class, 'dropDownPanel asc-context-menu')]/li//*[contains(text(), '{}')]".format(
                                             class_name))

    # Scroll the necessary class into view, so we can click on it
    browser.execute_script("arguments[0].scrollIntoView();", current_class)

    # Click on the selected class in the dropdown, to switch to it
    current_class.click()


# Closes the browser
def close_browser():
    global browser

    # Check config to see, if it's necessary to close the browser or not.
    if Config.Settings.Browser.Close:
        print('Closing browser!')
        browser.quit()
    else:
        print('Keeping browser open for development!')
