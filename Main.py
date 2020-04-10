# MedsNET Timetable Scraper
# Main Execution file
# Reinis Gunārs Mednis / Ikars Melnalksnis 2020
import Config
import Scraper
import Service_Connect
import Sorter

print('----------------------------------------------------')
print('Timetable Scraping, Sorting and Exporting scripts!')
print('   Reinis Gunārs Mednis, Ikars Melnalksnis - 2020')
print('----------------------------------------------------')

# Generates the config file, if there is none
Config.FirstLaunch()

# Start web browser
Scraper.start_browser(Config.Settings.Browser.URL)

"""
List Scraping
"""

# Scrape class list
ClassList = Scraper.scrape_list('Classes')

# Scrape teacher list
TeacherList = Scraper.scrape_list('Teachers')

# Scrape classroom list
RoomList = Scraper.scrape_list('Classrooms')

"""
File/Database initialization
"""

if Config.Settings.Database.Enabled:
    # Connects to the Database
    Database = Service_Connect.connect_to_mongo()

    # Drop previous collections
    Service_Connect.drop_collection(Database, "Tabulas_Skoleni")
    Service_Connect.drop_collection(Database, "Saraksti")

    # Export class list to database table
    print('Exporting Class list to database...')

    Service_Connect.list_export(RoomList, 'Telpas', Database)
    Service_Connect.list_export(TeacherList, 'Skolotaji', Database)
    Service_Connect.list_export(ClassList, 'Kursi', Database)

if Config.Settings.File.Enabled:
    # Creates the directory structure required, deletes old data
    Service_Connect.json_initialize()

    # Exports class list to a classes.json file
    Service_Connect.list_to_json(ClassList)

"""
Lesson scraping / Exporting
"""

for class_name in ClassList:

    print(' - - - Scraping {} lessons - - - '.format(class_name))
    # Open the table
    Scraper.open_table(class_name)

    # Scrape initial page
    Scraped_Data = Scraper.scrape_stundas()

    # Sort scraped data
    # [0] - Timetable data object, [1] - Timetable Class name
    Current_Lessons = Sorter.day_sorter(Scraped_Data, ClassList, TeacherList, RoomList)

    # Export to db, if selected
    if Config.Settings.Database.Enabled:
        # Generates a DB data model from the returned data and the class name
        Database_model = Service_Connect.make_data_model(Current_Lessons[0], Current_Lessons[1])

        # Pass the modeled data to the DB
        print('Exporting timetable data to database...')
        Service_Connect.export_to_mongo(Database, 'Tabulas_Skoleni', Database_model)

    # Export to file, if selected
    if Config.Settings.File.Enabled:
        # Exports lesson data and class name to file.
        Service_Connect.lessons_to_json(Current_Lessons[0], Current_Lessons[1])

# Close browser cleanly, if selected
Scraper.close_browser()
