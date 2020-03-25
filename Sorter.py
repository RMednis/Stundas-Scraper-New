import json
from selenium.webdriver.common.by import By

def DaySorter(scraped_data, class_list, teacher_list, room_list):
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
            self.index = 0  # Index to determine lectures columnar position

        def get_dict(self):
            # Can be used to get the necessary information
            return {
                        'nosaukums': self.nosaukums,
                        'skolotajs': self.skolotajs,
                        'kabinets': self.kabinets,
                        'group': self.group,
                        'index': self.index
                   }
    week = {
        "Pirmdiena": pirmdiena,
        "Otrdiena": otrdiena,
        "Trešdiena": tresdiena,
        "Ceturtdiena": ceturdiena,
        "Piektdiena": piekdiena
    }

    day_id = {
        420: pirmdiena,
        726: otrdiena,
        1032: tresdiena,
        1338: ceturdiena,
        1644: piekdiena
    }

    # Weird ypos gonna need a fix
    multigroup_ypos_bottom = [573, 879, 1185, 1491, 1797]
    single_lesson_length = 256.5
    first_lecture_xpos = 345.0    # Needed to determine if first lectures columnar position really is 0

    class_name = scraped_data[1][0]
    print('Pulling lessons to objects!')
    for stunda in scraped_data[0]:
        element_top = stunda.find_element(By.XPATH, './..')  # Gets the entire lesson block, not just the text!

        ypos = element_top.get_attribute('y')  # The y position of the lesson block!
        xpos = element_top.get_attribute('x')  # The x position of the lesson block!
        length = element_top.get_attribute('width')  # The width of the lesson block, used to calculate the time!
        data = stunda.get_property('innerHTML').splitlines()  # The text... split by /n

        # Multple group names, used for finding the group field.
        groups = ["1.grupa", "2.grupa"]

        # Defaults for the fields
        teacher, room, group, subject = "", "", "", ""

        # Matches the field content to the field type
        for field in data:
            # If the field is in the teacher list, it's a teacher field
            if field in teacher_list[0]:
                teacher = field

            # If the field is in the room list, it's a room field
            elif field in room_list[0]:
                room = field

            # If the field is in the group list, it's a group field
            elif field in groups:
                group = field

            # If none of the above match, it's a subject field
            else:
                subject = field

        # Used for multiple group day sorting, if the ypos is one of the bottom group elements
        if float(ypos) in multigroup_ypos_bottom:
            # Sets the ypos to the day it belongs in
            ypos = list(day_id)[multigroup_ypos_bottom.index(int(ypos))]

        # Add subject object to list
        current_day = day_id[int(ypos)]  # Finds the current day based on the subjects y position

        lesson_length = (
                float(length) / single_lesson_length)  # Calculates how many 45 minute segments the lesson takes up!
        lesson_count = 0  # Sets the counting veriable

        while lesson_count < lesson_length:  # Appends those 45 minute lesson segments to a list
            # If its second half of the lesson add single lesson length
            lesson_xpos = float(xpos) + lesson_count * single_lesson_length

            current_day.append(
                stunda_object(subject, teacher, room, lesson_xpos, ypos, group))  # Appends the subject to the day
            lesson_count += 1  # Appends 1 to the loop/lesson counter

    print('Sorting lessons by day')
    # Iterates through each day and sorts items by their x coords
    for day in week:
        week[day].sort(key=lambda item: float(item.x))  # Takes x coordinate as the key to sort by

        for lecture in week[day]:
            # First lecture of the day
            if week[day].index(lecture) == 0:
                # Sets the actual index/columnar position in table
                lecture.index = (float(lecture.x) - float(first_lecture_xpos)) / single_lesson_length
            else:
                # Last lecture object
                last_lecture = week[day][week[day].index(lecture) - 1]

                # Calculating how many lectures are in between last and current lecture + last lecture index
                lecture.index = ((lecture.x - last_lecture.x) / single_lesson_length) + last_lecture.index
    print('Creating JSON objects/string!')

    print('Outputting data!')

    return week, class_name
