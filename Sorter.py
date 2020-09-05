# MedsNET Timetable Scraper
# Main Sorting Function
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020

import datetime
import json
import re

from selenium.webdriver.common.by import By

import Config


def time_adder(week, class_name, table_type):
    """
    Function for adding time data and breaks to lessons.
    Warning - This function is 100% OVT specific, it will most likely not work for any other!

    :param week: Sorted Week object
    :param class_name: Class name
    :param table_type: The type of table the week's been scraped from
    :return:
    """
    print('Exporting with baked-in time information!')

    with open('./timings.json') as file:
        time_data = json.load(file)

    break_times = time_data["break_lengths"]

    class lesson_break:
        def __init__(self, time_from, time_to, name):
            self.type = "starpbridis"
            self.time = {
                "from": time_from,
                "to": time_to
            }
            self.name = name

        def get_dict(self):
            return {
                "veids": self.type,
                "nosaukums": self.name,
                "laiks": self.time
            }

    def find_times(day, class_name):
        """
        Function to find the correct lesson times based off the name of the class

        :param day: Name of the day the times are for
        :param class_name: Name of the class the times are for
        :return: Lesson times for the required class
        """
        # Pull out the 2 Letter department name from the class name
        class_type = str(re.findall(r'([A-Z]+)', class_name)[0])

        lessons = 0

        for times in time_data["lesson_times"]:

            if class_type in times["classes"]:  # If the time object is for the class
                if str(day) in times["days"]:  # If the time object also matches the required day
                    lessons = times  # Return that time object

        if lessons == 0:  # If there is no time object for the class
            raise Exception('Lesson times exception', 'No lesson times for ' + class_type + '/' + str(day))

        return lessons

    for day, day_data in week.items():  # Iterate through all the days

        """ Add lesson times """
        if table_type == "class":
            # Student tables adhere strictly to the defined times

            times = find_times(day, class_name)

            for lesson in day_data:
                lesson_time_object = times["lessons"][int(lesson.index)]
                lesson.add_time(lesson_time_object["start"], lesson_time_object["end"])

        else:
            # Teacher and room tables pull lesson times from each lesson's time table

            for lesson in day_data:
                times_full = find_times(day, lesson.klase)
                times_lesson = times_full["lessons"][int(lesson.index)]
                lesson.add_time(times_lesson["start"], times_lesson["end"])

        """ Add breaks between lessons """
        for lesson in day_data:
            if not isinstance(lesson, lesson_break):  # If the selected object isn't a break
                next_lesson_index = day_data.index(lesson) + 1  # Calculate the index for the next lesson in the day
                if next_lesson_index < len(day_data):  # If the next lesson is in the day
                    next_lesson = day_data[next_lesson_index]  # Get the next lesson object

                    if next_lesson.index != lesson.index:
                        # If the current and next lessons have different indexes
                        # (usually when there's multiple groups the index stays the same)

                        break_start = lesson.time["to"]  # Get the break start time (this lessons end time)
                        break_end = next_lesson.time["from"]  # Get the break end time (the next lessons start time)

                        time_standard = '%H:%M'
                        break_length = datetime.datetime.strptime(break_end,
                                                                  time_standard) - datetime.datetime.strptime(
                            break_start, time_standard)
                        break_length = str(int(break_length.seconds / 60))

                        if break_length in break_times:  # Check if the break has a custom name
                            break_name = break_times[break_length]
                        else:  # Use the default provided name
                            break_name = break_times["default"]

                        day_data.insert(day_data.index(lesson) + 1,  # Insert the break object after the lesson
                                        lesson_break(break_start, break_end, break_name))

    return week


def day_sorter(scraped_data, class_list, teacher_list, room_list):
    """
    :param scraped_data: Scraped page object
    :param class_list: Classroom dropdown list
    :param teacher_list: Teacher dropdown list
    :param room_list: Room dropdown list
    :return: [0] - Sorted week dict,
    [1] - The name of the scraped class/room/teacher
    """

    """
    Initialize objects 
    """
    # Initialize the dropdown_list objects
    pirmdiena, otrdiena, tresdiena, ceturdiena, piekdiena, sestdiena, svetdiena = list(), list(), list(), list(), list(), list(), list()

    # Main lesson class/object structure
    class stunda_object:
        def __init__(self, nosaukums, skolotajs, kabinets, klase, x, y, group):
            self.nosaukums = nosaukums  # Subject name
            self.skolotajs = skolotajs  # Subject Teacher
            self.kabinets = kabinets  # Subject Room
            self.klase = klase
            self.group = group  # Group (if multiple subjects are for different subgroups)
            self.x = x  # Object X coordinate
            self.y = y  # Object Y coordinate
            self.time = {
                "from": 0,
                "to": 0
            }
            self.index = 0  # Index to determine lectures columnar position

        def add_time(self, time_from, time_to):
            self.time = {
                "from": time_from,
                "to": time_to
            }

        def get_dict(self):
            if Config.Settings.Scraper.Time_Export:
                return {
                    'veids': "stunda",
                    'laiks': self.time,
                    'nosaukums': self.nosaukums,
                    'skolotajs': self.skolotajs,
                    'kabinets': self.kabinets,
                    'klase': self.klase,
                    'group': self.group,
                }
            else:
                return {
                    'nosaukums': self.nosaukums,
                    'skolotajs': self.skolotajs,
                    'kabinets': self.kabinets,
                    'klase': self.klase,
                    'group': self.group,
                    'index': self.index,
                }

    # Main week object, holds all day lists
    week = {
        "Pirmdiena": pirmdiena,
        "Otrdiena": otrdiena,
        "Trešdiena": tresdiena,
        "Ceturtdiena": ceturdiena,
        "Piektdiena": piekdiena,
        "Sestdiena": sestdiena,
        "Svētdiena": svetdiena
    }

    """
    Changeable variables
    """
    # Used for sorting lessons into days based off their ypos values
    day_id = {
        # Regular Week y positions and days
        420: pirmdiena,
        726: otrdiena,
        1032: tresdiena,
        1338: ceturdiena,
        1644: piekdiena,

        # Multi-Group Lesson Bottom Elements
        573: pirmdiena,
        879: otrdiena,
        1185: tresdiena,
        1491: ceturdiena,
        1797: piekdiena,
        1567.5: sestdiena,

        # Full Week y positions and days
        # TODO: Add support for all full week days!
        1440: piekdiena,
        1695: sestdiena
    }

    # Length of a single lesson segment (Used for dividing them into standard size chunks)
    single_lesson_length = 256.5

    first_lecture_xpos = 345.0  # Needed to determine if first lectures columnar position really is 0

    """
    Scraping the class name
    """
    class_name = scraped_data["name"][0]

    if "Teacher " in class_name:  # If the field contains the text 'Teacher'
        class_name = class_name.split("Teacher ")[1]  # Use only the Name (ignoring the Teacher part)

    # Find the type of timetable we have
    if class_name in teacher_list:
        table_type = "teacher"
    elif class_name in class_list:
        table_type = "class"
    else:
        table_type = "room"

    print('Converting raw data to lesson objects...')

    """
    Scrape and sort data into field types
    """
    for stunda in scraped_data["stundas"]:

        """
        Initialize variables
        """
        # Multiple group names, used for finding the group field.
        groups = ["1.grupa", "2.grupa"]

        # Defaults for the fields
        teacher, room, group, subject, students = "", "", "", "", ""

        """
        Scrape data from table
        """
        element_top = stunda.find_element(By.XPATH, './..')  # Gets the entire lesson block, not just the text!

        ypos = element_top.get_attribute('y')  # The y position of the lesson block!
        xpos = element_top.get_attribute('x')  # The x position of the lesson block!
        length = element_top.get_attribute('width')  # The width of the lesson block, used to calculate the time!
        data = stunda.get_property('innerHTML').splitlines()  # The text... split by /n

        """
        Sort text into appropriate fields
        """
        # Matches the field content to the field type
        for field in data:

            # Strip whitespace
            field.strip()

            # Set full text object to the current field object
            full_field = field

            # If the field contains a / we split it and only match the first part!
            if "/" in field:
                field = field.split("/")[0]

            # If the field is in the class list, it's a teacher field
            if field in class_list:
                students = full_field

            # If the field is in the Teacher list, it's a teacher field.
            elif field in teacher_list:
                teacher = full_field

            # If the field is in the room list, it's a room field
            elif field in room_list:
                room = full_field

            # If the field is in the group list, it's a group field
            elif field in groups:
                group = full_field

            # If none of the above match, it's a subject field
            else:
                subject = full_field

        """
        Sort lesson into appropriate day, split into lesson segments
        """
        current_day = day_id[float(ypos)]  # Finds the current day based on the subjects y position

        lesson_length = (
                float(length) / single_lesson_length)  # Calculates how many lesson segments the lesson takes up!
        lesson_count = 0  # Sets the counting variable

        while lesson_count < lesson_length:  # Appends those 45 minute lesson segments to a dropdown_list
            # If its second half of the lesson add single lesson length
            lesson_xpos = float(xpos) + lesson_count * single_lesson_length

            current_day.append(
                stunda_object(subject, teacher, room, students, lesson_xpos, ypos,
                              group))  # Appends the subject to the day
            lesson_count += 1  # Appends 1 to the loop/lesson counter

    """
    Sort lessons in days by their x coordinates
    """
    total_lessons = 0  # Counting variable

    for day in week:
        week[day].sort(key=lambda item: float(item.x))  # Takes x coordinate as the key to sort by

        total_lessons += len(week[day])

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

    """
    Add time data and breaks if the option is selected
    """
    if Config.Settings.Scraper.Time_Export:
        week = time_adder(week, class_name, table_type)

    print('Sorted {} lessons!'.format(total_lessons))

    return {
        "week": week,
        "total": total_lessons,
        "name": class_name,
        "date": scraped_data["date"]
    }
