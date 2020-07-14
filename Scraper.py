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


def start_browser(url):
    """
    Starts the browser!

    :param url: Page url to navigate to
    """

    global browser
    opts = Options()
    headless_check = Config.Settings.Browser.Headless

    # Print current config to console for debugging
    print('Headless: ', headless_check)
    print('URL:      ', url)

    opts.headless = headless_check  # Sets headless state based off the headless_check setting

    # Sets which div will be checked to determine when the page has fully loaded depending on version
    checked_element = (By.XPATH, "//div[contains(@class, 'print-nobreak')]/div//*[name()='svg']")

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


def scrape_stundas():
    """
    Scrapes raw lesson objects from svg

    :return: dictionary containing stundas - lesson week, name - class name, date - table date
    """

    print('Locating and parsing SVG elements!')
    # Check if the new/testing version of the timetable viewer is being used.

    path_stundas = "//div[contains(@class, 'print-nobreak')]/div//*[name()='svg']//*[name()='g']//*[name()='rect']//*[name()='title']"
    path_class_name = "//div[contains(@class, 'print-nobreak')]//*[name()='svg']//*[name()='g']//*[name()='text' and @y='166.875']"
    path_table_date = "//div[contains(@class, 'print-nobreak')]//*[name()='svg']//*[name()='g']//*[name()='text' and @y='107.5']"

    # Find all the lesson objects in the svg
    stundas = browser.find_elements_by_xpath(path_stundas)

    # Find the class name in the svg
    class_name = browser.find_element(By.XPATH, path_class_name).get_property('innerHTML').splitlines()

    # Find the date the table applies to
    table_date = browser.find_element(By.XPATH, path_table_date).get_property('innerHTML')
    print(table_date)

    # Returns week lesson object, class name and table date
    return {
        "stundas": stundas,
        "name": class_name,
        "date": table_date
    }


def open_list(list_name):
    """
    Opens the dropdown list!

    :param list_name: Name of the list to open
    """
    global browser

    button_path = "//*[@id='skin_PageContent_2']/div/div/div/span[@title='{}']".format(list_name)

    # Find the selector button in the document
    selector_button = browser.find_element(By.XPATH, button_path)

    # Click on the class selector button, to load in the required dropdown elements for scraping.
    selector_button.click()


def scrape_list(list_name):
    """
    Scrapes the required dropdown list!

    :param list_name: Name of the dropdown list (From the UI!)
    :return: A list of all the objects in the dropdown list!
    """
    global browser

    # This XPATH works on both viewer types
    path = "//div[contains(@class, 'asc dropDown')]//ul[contains(@class, 'dropDownPanel asc-context-menu')]/li/a"

    print('Scraping {} dropdown list!'.format(list_name))

    # Open the required list, so it can be scraped
    open_list(list_name)

    list_items = browser.find_elements(By.XPATH, path)  # The drop down html elements
    names = list()  # List object to hold the dropdown text content

    # Loop through the elements and get their text content
    for item in list_items:
        name = item.get_attribute('innerHTML')  # Get list name text
        names.append(name)  # Append it to the text content to the names list

    return names


def open_table(list_name, class_name):
    """
    Opens a table based off the class name

    :param list_name: The dropdown, that the table resides in
    :param class_name: The name of the dropdown object
    """
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


def close_browser():
    """
    Closes the browser.
    """
    global browser

    # Check config to see, if it's necessary to close the browser or not.
    if Config.Settings.Browser.Close:
        print('Closing browser!')
        browser.quit()
    else:
        print('Keeping browser open for development!')
