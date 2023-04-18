# Coyote-Attacks-News

🚀 This program is designed to scrape news articles related to coyote attacks within a specified time period using the Newscatcher API. The program saves the extracted data into a SQLite database.

Note: The script requires an API key for [Newscatcher](https://rapidapi.com/newscatcher-api-newscatcher-api-default/api/newscatcher).

[![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.6-blue.svg)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/) 


## Requirements
- 🐍 [python>=3.6](https://www.python.org/downloads/)


## ⬇️ Installation

```bash
git clone https://github.com/Biodiversity-CatTracker2/Coyote-Attacks-News.git
cd Coyote-Attacks-News
```

```bash
pip install -r requirements.txt
```


## ⌨️ Usage

```
usage: main.py [-h] -d DB_NAME -s START_DATE -e END_DATE [--no-sleep]

options:
  -h, --help            show this help message and exit
  -d DB_NAME, --db-name DB_NAME
                        Name of the database file
  -s START_DATE, --start-date START_DATE
                        Search from this date
  -e END_DATE, --end-date END_DATE
                        Search until this date
  --no-sleep            No sleep
```


### Parse Articles
```bash
python main.py -d <DB_NAME> -s <START_DATE> -e <END_DATE>
```

### Run Datasette Instance
- First, rename and edit `run.sh.example` content.
```bash
mv run.sh.example run.sh
nano run.sh
```
- Then, run with:
```bash
bash run.sh
```

## 📕 Examples
```bash
python main.py -d db.sqlite3 -s '2023-04-02' -e '2023-04-17'
```
