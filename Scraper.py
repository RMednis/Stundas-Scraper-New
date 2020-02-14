# MedsNET Timetable Scraper
# Scrapin ain't no big deal
# Reinis 2020

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

# Enter the URL of the site
url = 'https://ogrestehnikums.edupage.org/timetable/view.php?num=7&class=-114'

# Toggle if browser is headless or not
headless_check = False

print('MedsNET Timetable Scraper! - WIP')
opts = Options()

print('Headless: ', headless_check)
print('URL:      ', url)
opts.headless = headless_check

print('Launching browser...')
browser = Firefox(options=opts)

print('Navigating to ', url)
browser.get(url)

try:
    print('Waiting for page JS to load...')
    WebDriverWait(browser, 6).until(EC.presence_of_element_located((By.ID, 'ttonline_printpreview')))
    print('JS Loaded!')

except TimeoutException:
    print("Failed - Timeout loading main page!")
    exit(100)


print('Locating and parsing SVG elements!')

stundas = browser.find_elements_by_xpath("//div[contains(@class, 'print-sheet')]//*[name()='svg']//*[name()='g']//*[name()='rect']//*[name()='title']")


print('Sorting elements by day!')

pirmdiena, otrdiena, tresdiena, ceturdiena, piekdiena = [], [], [], [], []

class Stunda_Object:
    nosaukums = ''
    skolotajs = ''
    kabinets = ''



day_id = {
        420: pirmdiena,
        726: otrdiena,
        1032: tresdiena,
        1338: ceturdiena,
        1644: piekdiena
    }



for stunda in stundas:
    element_top = stunda.find_element(By.XPATH, './..')
    ypos = element_top.get_attribute('y')
    xpos = element_top.get_attribute('x')
    length = element_top.get_attribute('width')
    data = stunda.get_property('innerHTML').splitlines()
    subject = data[0]
    teacher = data[1]
    room = data[2]

    print('--DEBUG')
    print('x:', xpos, ' y:', ypos, ' length:', length)
    print('Subject:', subject, 'Teacher:', teacher, 'Room:', room)


