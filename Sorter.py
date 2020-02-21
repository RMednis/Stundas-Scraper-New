import json
from selenium.webdriver.common.by import By

def DaySorter(stundas):
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
                if self.group == "2.grupa":
                    self.length = 2.0  # TEMP FIX NEED TO LOOK INTO IT
                else:
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

    # Weird ypos gonna need a fix
    weird_ypos_bottom = [573, 879, 1185, 1491]
    one_hour_length = 256.5

    print('Pulling lessons to objects!')
    for stunda in stundas:
        element_top = stunda.find_element(By.XPATH, './..')  # Gets the entire lesson block, not just the text!
        ypos = element_top.get_attribute('y')  # The y position of the lesson block!
        xpos = element_top.get_attribute('x')  # The x possition of the lesson block!
        length = element_top.get_attribute('width')  # The width of the lession block, used to calculate the time!
        data = stunda.get_property('innerHTML').splitlines()  # The text... split by /n

        # TODO: FIX THIS: https://ogrestehnikums.edupage.org/timetable/view.php?num=12&class=-80 WEIRD HOURS
        # TEMP FIX!
        if len(data) == 4:
            if float(ypos) in weird_ypos_bottom:  # If theres no teacher field its probably full day
                ypos = list(day_id)[weird_ypos_bottom.index(int(ypos))]

            subject = data[0]
            group = data[1]
            teacher = data[2]
            room = data[3]

        elif len(data) != 3:
            subject = data[0]
            room = data[1]
            teacher = ""
            group = ""
        else:
            subject = data[0]
            room = data[1]
            teacher = data[2]
            group = ""

        # Add subject object to list
        day_id[int(ypos)].append(stunda_object(subject, teacher, room, xpos, ypos, group))

    print('Sorting lessons by day')
    # Iterates through each day and sorts items by their x coords
    for day in day_id:
        day_id[day].sort(key=lambda item: float(item.x))  # Takes x coordinate as the key

        # Adds subject length
        for item in day_id[day]:
            # Adds length to previous item 3AM NO IDEA HOW THIS SH1T WORKS(-1 = Fullday; 1.0 = 1 hour; 2.0 = 2 hours)
            day_id[day][day_id[day].index(item) - 1].addLength(
                (float(item.x) - float(day_id[day][day_id[day].index(item) - 1].x)) / one_hour_length)

    print('Creating JSON objects/string!')

    print(day_id)
    print(json.dumps(day_id, default=lambda x: x.__dict__))

    print('Outputting data!')

    return json.dumps(day_id, default=lambda x: x.__dict__)
