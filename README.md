# Stundas Scraper

Scrapes lesson data and times from the [OVT Edupage](https://ogrestehnikums.edupage.org) based timetables, exports this 
to a MongoDB server.

## About
Stundas Scraper is a web scraper, that automatically pulls data from OVT's Edupage based time tables, sorts them, and
converts them into easily usable objects, that are used for a multitude of tasks.  

This project is based with the specific formatting of the OVT timetables in mind. `Scraper.py` should work with most 
timetable formats, but `Sorter.py` has hard coded values, that are only meant for OVT's specific timetable formatting.

#### Some additional points:

- All lessons are split into 45 minute segments. This is done to make all lessons standard, this also counts on the fact
that no lesson is shorter than 45 minutes.
- The exported data does not calculate or approximate breaks between 45 minute lessons. This should be done on the 
front-end apps.
- The scripts can both - export to a MongoDB database server, or generate a static JSON output file, this can be set
in the configuration file generated on first start.


## Getting Started

This project is based on Python 3.7, and uses the Selenium browser automation suite for scraping.
Currently only Firefox is supported, but support for chromium shouldn't bee too hard to do.

### Prerequisites
Your system needs to have Python 3.5 (or newer), [Firefox](https://www.mozilla.org/en-US/firefox/new/) and [Geckodriver](https://github.com/mozilla/geckodriver/releases) installed. 
Geckodriver also needs to accessible in the system path on both Windows and Linux.

#### Ubuntu 19.04
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
Run *Main.py* to generate a default configuration file  
```
python3 Main.py
```
#### Docker

In development...

## ToDo
- [x] Single Timetable Scraping
- [x] Lesson sorting by time/day
- [ ] Multiple Timetable Scraping
- [x] Database connection
- [ ] Export data to database **(Partial)**
- [X] Export data to JSON files.
- [x] Handling of empty lessons
- [ ] Handling of multiple lessons at once **(Partial)**
- [x] Lesson time calculation
- [ ] Export Group Listing
- [ ] Support for teacher tables
- [ ] Support for room tables
- [x] Support for new timetable viewer

## Authors

* **Reinis Gunārs Mednis** - *Initial Work, Scraping, Database Connections* - [RMednis](https://github.com/RMednis)
* **Ikars Melnalksnis** - *Initial Work, Sorting, JSON Response creation* - [Lyx52](https://github.com/Lyx52)

## License

*To Be Determined*


