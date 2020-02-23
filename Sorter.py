import json
from selenium.webdriver.common.by import By

def DaySorter(stundas):
    pirmdiena, otrdiena, tresdiena, ceturdiena, piekdiena = list(), list(), list(), list(), list()

    # Stundas objekts
    class stunda_object:
        def __init__(self, nosaukums, skolotajs, kabinets, x, y, group):
            self.nosaukums = nosaukums  # Subject name
            self.skolotajs = skolotajs  # Subject Teacher
            self.kabinets = kabinets  # Subject Room
            self.group = group  # Group (if multiple subjects are for different subgroups)
            self.x = x  # Object X coordinate
            self.y = y  # Object Y coordinate


    day_id = {
        420: pirmdiena,
        726: otrdiena,
        1032: tresdiena,
        1338: ceturdiena,
        1644: piekdiena
    }

    # Weird ypos gonna need a fix
    weird_ypos_bottom = [573, 879, 1185, 1491]
    single_lesson_length = 256.5

    print('Pulling lessons to objects!')
    for stunda in stundas:
        element_top = stunda.find_element(By.XPATH, './..')  # Gets the entire lesson block, not just the text!
        ypos = element_top.get_attribute('y')  # The y position of the lesson block!
        xpos = element_top.get_attribute('x')  # The x position of the lesson block!
        length = element_top.get_attribute('width')  # The width of the lesson block, used to calculate the time!
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

        current_day = day_id[int(ypos)]  # Finds the current day based on the subjects y position
        lesson_length = (
                    float(length) / single_lesson_length)  # Calculates how many 45 minute segments the lesson takes up!
        lesson_count = 0  # Sets the counting veriable

        while lesson_count < lesson_length:  # Appends those 45 minute lesson segments to a list
            lesson_xpos = float(
                xpos) + lesson_count  # Increments the xpos, so each segment get sorted after each other.
            current_day.append(
                stunda_object(subject, teacher, room, lesson_xpos, ypos, group))  # Appends the subject to the day
            lesson_count += 1  # Appends 1 to the loop/lesson counter

    print('Sorting lessons by day')
    # Iterates through each day and sorts items by their x coords
    for day in day_id:
        day_id[day].sort(key=lambda item: float(item.x))  # Takes x coordinate as the key to sort by

    print('Creating JSON objects/string!')

    print(day_id)
    print(json.dumps(day_id, default=lambda x: x.__dict__))

    print('Outputting data!')

    return json.dumps(day_id, default=lambda x: x.__dict__)
