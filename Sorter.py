# MedsNET Timetable Scraper
# Main Sorting Function
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020

from selenium.webdriver.common.by import By


def day_sorter(scraped_data, class_list, teacher_list, room_list):
    # Initialize the list objects
    pirmdiena, otrdiena, tresdiena, ceturdiena, piekdiena = list(), list(), list(), list(), list()

    # Main lesson class/object structure
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
            # Returns data in a simple dict format
            return {
                'nosaukums': self.nosaukums,
                'skolotajs': self.skolotajs,
                'kabinets': self.kabinets,
                'group': self.group,
                'index': self.index
            }

    # Main week object, holds all day lists
    week = {
        "Pirmdiena": pirmdiena,
        "Otrdiena": otrdiena,
        "Trešdiena": tresdiena,
        "Ceturtdiena": ceturdiena,
        "Piektdiena": piekdiena
    }

    # Used for sorting lessons into days based off their ypos values
    day_id = {
        420: pirmdiena,
        726: otrdiena,
        1032: tresdiena,
        1338: ceturdiena,
        1644: piekdiena
    }

    # Ypos values for multi-group lesson bottom elements
    multigroup_ypos_bottom = [573, 879, 1185, 1491, 1797]

    # Length of a single lesson segment (Used for dividing them into standard size chunks)
    single_lesson_length = 256.5

    first_lecture_xpos = 345.0  # Needed to determine if first lectures columnar position really is 0

    class_name = scraped_data[1][0]

    print('Converting raw data to lesson objects...')
    for stunda in scraped_data[0]:
        element_top = stunda.find_element(By.XPATH, './..')  # Gets the entire lesson block, not just the text!

        ypos = element_top.get_attribute('y')  # The y position of the lesson block!
        xpos = element_top.get_attribute('x')  # The x position of the lesson block!
        length = element_top.get_attribute('width')  # The width of the lesson block, used to calculate the time!
        data = stunda.get_property('innerHTML').splitlines()  # The text... split by /n

        # Multiple group names, used for finding the group field.
        groups = ["1.grupa", "2.grupa"]

        # Defaults for the fields
        teacher, room, group, subject = "", "", "", ""

        # Matches the field content to the field type
        for field in data:
            # If the field is in the teacher list, it's a teacher field
            if field in teacher_list:
                teacher = field

            # If the field is in the room list, it's a room field
            elif field in room_list:
                room = field

            # If the field is in the group list, it's a group field
            elif field in groups:
                group = field

            # If none of the above match, it's a subject field
            else:
                subject = field

        # Normalize y coordinates
        # Used for multiple group day sorting, if the ypos is one of the bottom group elements
        if float(ypos) in multigroup_ypos_bottom:
            # Sets the ypos to the day it belongs in
            ypos = list(day_id)[multigroup_ypos_bottom.index(int(ypos))]

        # Add subject object to list
        current_day = day_id[int(ypos)]  # Finds the current day based on the subjects y position

        lesson_length = (
                float(length) / single_lesson_length)  # Calculates how many 45 minute segments the lesson takes up!
        lesson_count = 0  # Sets the counting variable

        while lesson_count < lesson_length:  # Appends those 45 minute lesson segments to a list
            # If its second half of the lesson add single lesson length
            lesson_xpos = float(xpos) + lesson_count * single_lesson_length

            current_day.append(
                stunda_object(subject, teacher, room, lesson_xpos, ypos, group))  # Appends the subject to the day
            lesson_count += 1  # Appends 1 to the loop/lesson counter

    print('Sorting lessons by day...')

    # Iterates through each day and sorts items by their x coords
    for day in week:
        week[day].sort(key=lambda item: float(item.x))  # Takes x coordinate as the key to sort by

        for lesson in week[day]:
            # First lesson of the day
            if week[day].index(lesson) == 0:
                # Sets the actual index/columnar position in table
                lesson.index = (float(lesson.x) - float(first_lecture_xpos)) / single_lesson_length
            else:
                # Last lesson object
                last_lesson = week[day][week[day].index(lesson) - 1]

                # Calculating how many lectures are in between last and current lesson + last lesson index
                lesson.index = ((lesson.x - last_lesson.x) / single_lesson_length) + last_lesson.index

    print('Sorting complete!')

    return week, class_name
