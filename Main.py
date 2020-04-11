# MedsNET Timetable Scraper
# Main Execution file
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020
import datetime

import Config
import Scraper
import Service_Connect
import Sorter

print('------------------Stundas-Scraper-------------------')
print('Timetable Scraping, Sorting and Exporting scripts!')
print('   Reinis Gunārs Mednis, Ikars Melnalksnis - 2020')
print('----------------------------------------------------')

start_time = datetime.datetime.now()
print('Start Time:', start_time)
# Generates the config file, if there is none
Config.FirstLaunch()

Settings = Config.Settings

# Start web browser
Scraper.start_browser(Config.Settings.Browser.URL)

"""
List Scraping
"""

# Scrape class dropdown_list
ClassList = Scraper.scrape_list('Classes')

# Scrape teacher dropdown_list
TeacherList = Scraper.scrape_list('Teachers')

# Scrape classroom dropdown_list
RoomList = Scraper.scrape_list('Classrooms')

"""
File/Database initialization
"""

if Config.Settings.Database.Enabled:
    # Connects to the Database
    Database = Service_Connect.connect_to_mongo()

    # Export class dropdown_list to database table
    print('Exporting Class dropdown list to database...')
    Service_Connect.drop_collection(Database, Settings.Scraper.List_Name)

    Service_Connect.list_export(RoomList, Settings.Scraper.Student_Table_Name, Database)
    Service_Connect.list_export(TeacherList, Settings.Scraper.Teacher_Table_Name, Database)
    Service_Connect.list_export(ClassList, Settings.Scraper.Teacher_Table_Name, Database)

if Settings.File.Enabled:
    # Creates the directory structure required, deletes old data
    Service_Connect.json_initialize()

    # Exports class dropdown_list to a classes.json file
    Service_Connect.list_to_json(ClassList, "Kursi")
    Service_Connect.list_to_json(TeacherList, "Skolotaji")
    Service_Connect.list_to_json(RoomList, "Telpas")

"""
Lesson scraping / Exporting function
"""


def export_all_tables(name, name_list, collection):
    print('- - - Scraping {} tables! - - - '.format(name))

    Service_Connect.drop_collection(Database, collection)

    for table_name in name_list:

        print(' - - - Scraping {} lessons - - - '.format(table_name))
        # Open the table
        Scraper.open_table(name, table_name)

        # Scrape initial page
        scraped_data = Scraper.scrape_stundas()

        # Sort scraped data
        # [0] - Timetable data object, [1] - Timetable Class name
        current_lessons = Sorter.day_sorter(scraped_data, ClassList, TeacherList, RoomList)

        # Export to db, if selected
        if Settings.Database.Enabled:
            # Generates a DB data model from the returned data and the class name
            database_model = Service_Connect.make_data_model(current_lessons[0], current_lessons[1])

            # Pass the modeled data to the DB
            print('Exporting timetable data to database...')
            Service_Connect.export_to_mongo(Database, collection, database_model)

        # Export to file, if selected
        if Settings.File.Enabled:
            # Exports lesson data and class name to file.
            Service_Connect.lessons_to_json(current_lessons[0], current_lessons[1])


'''
Main function calls
'''
if Settings.Stages.Students:
    export_all_tables("Classes", ClassList, Settings.Database.Table_Prefix + Settings.Scraper.Student_Table_Name)
if Settings.Stages.Teachers:
    export_all_tables("Teachers", TeacherList, Settings.Database.Table_Prefix + Settings.Scraper.Teacher_Table_Name)
if Settings.Stages.Classrooms:
    export_all_tables("Classrooms", RoomList, Settings.Database.Table_Prefix + Settings.Scraper.Room_Table_Name)

print("- - - Scraping complete! :) - - - ")

# Time taken calculation
end_time = datetime.datetime.now()
print("Scraping finished:", end_time)
print("Scraping took:", end_time - start_time)

# Close browser cleanly, if selected
Scraper.close_browser()
print("- - - Goodbye! - - -")
