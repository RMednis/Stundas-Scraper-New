# MedsNET Timetable Scraper
# Scrapin ain't no big deal
# Reinis 2020

import simplejson as simplejson
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Enter the URL of the site
url = 'https://ogrestehnikums.edupage.org/timetable/view.php?num=12&class=-114'
# url = 'https://ogrestehnikums.edupage.org/timetable/view.php?num=12&class=-80' # broken url

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

stundas = browser.find_elements_by_xpath(
    "//div[contains(@class, 'print-sheet')]//*[name()='svg']//*[name()='g']//*[name()='rect']//*[name()='title']")

print('Sorting elements by day!')

pirmdiena, otrdiena, tresdiena, ceturdiena, piekdiena = list(), list(), list(), list(), list()


# Stundas objekts
class stunda_object:
    def __init__(self, nosaukums, skolotajs, kabinets, x, y, group):
        self.nosaukums = nosaukums
        self.skolotajs = skolotajs
        self.kabinets = kabinets
        self.group = group
        self.x = x
        self.y = y
        self.length = 0

    def addLength(self, len):
        if len == 0:
            self.length = -1  # FULL DAY
        elif len < 0 and abs(len) % 2 == 0:
            self.length = 2.0  # Last hour of the day is 2 hours long
        elif len < 0 and abs(len) % 2 != 0:
            self.length = 1.0  # Last hour of the day is 1 hour long
        else:
            self.length = len  # Last hour of the day is length long


day_id = {
    420: pirmdiena,
    726: otrdiena,
    1032: tresdiena,
    1338: ceturdiena,
    1644: piekdiena
}

day_name = {
    420: "Pirmdiena",
    726: "Otrdiena",
    1032: "Tresdiena",
    1338: "Ceturtdiena",
    1644: "Piektdiena"
}
# Weird ypos gonna need a fix
weird_ypos = [573, 879, 1185, 1491]
one_hour_length = 256.5

for stunda in stundas:
    element_top = stunda.find_element(By.XPATH, './..')
    ypos = element_top.get_attribute('y')
    xpos = element_top.get_attribute('x')
    length = element_top.get_attribute('width')
    data = stunda.get_property('innerHTML').splitlines()

    # TODO: FIX THIS: https://ogrestehnikums.edupage.org/timetable/view.php?num=12&class=-80 WEIRD HOURS
    # TEMP FIX!
    if not float(ypos) in weird_ypos:
        # If theres no teacher field its probably full day
        if len(data) != 3:
            subject = data[0]
            room = data[1]
            teacher = ""
            group = "" # group is 1. index of data
        else:
            subject = data[0]
            room = data[1]
            teacher = data[2]
            group = ""

        # Add subject object to list
        day_id[int(ypos)].append(stunda_object(subject, teacher, room, xpos, ypos, ""))

# Iterates through each day and sorts items by their x coords
for day in day_id:
    day_id[day].sort(key=lambda item: float(item.x))  # Takes x coordinate as the key

    # Adds subject length
    for item in day_id[day]:
        # Adds length to previous item 3AM NO IDEA HOW THIS SH1T WORKS(-1 = Fullday; 1.0 = 1 hour; 2.0 = 2 hours)
        day_id[day][day_id[day].index(item) - 1].addLength(
            (float(item.x) - float(day_id[day][day_id[day].index(item) - 1].x)) / one_hour_length)

json_data = '{"Server": {},"Dienas": {'


# Function that returns json array element in string
def pievienot_stundu(subject, teacher, room, length):
    return '{"Prieksmets":"' + subject + '","Skolotajs":"' + teacher + '","Telpa":"' + room + '","Ilgums":"' + str(length) + '"}'


# Index to keep track of each
temp_index = 0
for day in day_id:
    # Add start of each subject array
    json_data += '"' + day_name[day] + '": ['

    # Iterate through subjects
    for stunda in day_id[day]:

        # Add to temp index(At the start so we dont have to subtract 1 from day_id array)
        temp_index += 1

        # Add each subject to current json string using pievienot_stundu function
        json_data += pievienot_stundu(stunda.nosaukums, stunda.skolotajs, stunda.kabinets, stunda.length)

        # If its not the last subject, then add a comma to seperate array elements
        if len(day_id[day]) != temp_index:
            json_data += ','

    # Reset index
    temp_index = 0

    # If its not the last day add end of array
    if day != 1644:
        json_data += '],'

    # Else add end of json file
    else:
        json_data += ']}}'

# Output the file
with open("output.json", "w") as output_file:
    output_file.write(simplejson.dumps(simplejson.loads(json_data), indent=4))
    output_file.close()
