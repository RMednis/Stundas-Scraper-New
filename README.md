# Stundas Scraper

Scrapes lesson data and times from the [OVT Edupage](https://ogrestehnikums.edupage.org) based timetables, exports this 
to a MongoDB server or static JSON.

## About
Stundas Scraper is a web scraper, that automatically pulls data from OVT's Edupage based time tables, sorts them, and
converts them into easily usable objects, that are used for a multitude of tasks.  

This project, although initially meant for OVT timetables, should technically work for other timetable types without too
many issues. The main issues might be in `Sorter.py`, since it contains hard coded values for object positions.

#### Some additional points:

- All lessons are split into segments. In the case of OVT these segments are 45 minutes long. 
- The exported data does not calculate or approximate breaks between lesson segments. This should be done on the 
front-end apps.
- The scripts can both - export to a MongoDB database server, or generate static JSON output files, this can be set
in the configuration file generated on first start.


## Getting Started

This project is built on Python 3.7, and uses the Selenium browser automation suite for scraping.

Currently only Firefox is supported, chromium support should be possible, but is currently not a priority.

Python versions from 3.5 to 3.8 are fully supported.

### Prerequisites
Your system needs to have Python 3.5 (or newer), [Firefox](https://www.mozilla.org/en-US/firefox/new/) and [Geckodriver](https://github.com/mozilla/geckodriver/releases) installed. 
Geckodriver also needs to accessible in the system path on both Windows and Linux.

We support exporting timetables/class lists to [Mongodb](https://www.mongodb.com) or static JSON, the configuration for that can
be found in the `config.ini` that gets generated on first start.  
 

#### Ubuntu 19.04 / 19.10
Install firefox: 
```
sudo apt install firefox 
```

Download and extract [geckodriver](https://github.com/mozilla/geckodriver/releases/latest) for linux: 
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz 
tar -xvzf geckodriver-v0.26.0-linux64.tar.gz
chmod +x geckodriver
```
Move geckodriver to `/usr/local/bin` to make it accessible in the system PATH for python
```
mv geckodriver /usr/local/bin
```

### Installing


#### Installing manually
Clone the repository
```
git clone https://github.com/RMednis/Stundas-Scraper-New
```
Install the required packages from `requirements.txt`
```
pip3 install -r requirements.txt
```
Run `Main.py` to generate a default `config.ini` file, or rename the existing `config.sample` to `config.ini`  
```
python3 Main.py
```

Edit the settings in `config.ini` to match your needs. (At least the *scrape_url* section)

Run `Main.py` to scrape tables.
#### Docker

In development...

## ToDo
- [x] Single Timetable Scraping.
- [x] Lesson sorting by time/day.
- [x] Multiple Timetable Scraping.
- [x] Database connection.
- [x] Export data to database.
- [X] Export data to JSON files.
- [x] Handling of empty lessons.
- [x] Handling of multiple lessons at once (Multi-Group).
- [x] Lesson time calculation.
- [x] Export Group List.
- [x] Export Room List.
- [x] Export Teacher List.
- [x] Support for teacher tables.
- [x] Support for room tables.
- [x] Support for new timetable viewer.

## Authors

* **Reinis Gunārs Mednis** - *Initial Work, Scraping/Sorting, Database Connections, List exports* - [RMednis](https://github.com/RMednis)
* **Ikars Melnalksnis** - *Initial Work, Scraping/Sorting, JSON Response creation, List exports* - [Lyx52](https://github.com/Lyx52)

## License

Licensed under the MIT License, Copyright © Reinis Gunārs Mednis, Ikars Melnalksnis 2020

For more information, check ``LICENSE.md``


