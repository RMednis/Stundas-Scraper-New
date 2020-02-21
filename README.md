# Stundas Scraper

Scrapes lesson data and times from the [OVT Edupage](https://ogrestehnikums.edupage.org) based timetables, creates a JSON REST API for use with other frontend apps.

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
- [ ] API Response **(Partial)**
- [ ] Handling of empty lessons
- [ ] Handling of multiple lessons at once **(Partial)**
- [ ] Lesson time calculation
- [ ] API Group Listing

## Authors

* **Reinis Gunārs Mednis** - *Initial Work, Scraping, API* - [RMednis](https://github.com/RMednis)
* **Ikars Melnalksnis** - *Initial Work, Sorting, API* - [Lyx52](https://github.com/Lyx52)

## License

*To Be Determined*


