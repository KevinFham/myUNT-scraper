# myUNT Scraper

Web scraper tool for visualizing and analyzing aggregated student schedule data on myUNT

### Dependencies

- Python 3.11

- Selenium v4.11 (Built In Chrome Driver)

  ```sh
  conda env create -f environment.yml
  ```

## Usage Instructions

### `scraper.py` 

- Log into myUNT and automate. This will save and update `.html` files within `./course` for parsing

  ```sh
  python3 scraper.py -t "2024 Fall" CSCE EENG BMEN MEEN MTSE 
  ```

### `htmlparser.py`

- Parse `.html` files within `./course` and populate `ENG_course_catalog_database.csv`

  ```sh
  python3 htmlparser.py
  ```

### `schedulepacker.py`

- Pack courses in the `.csv` into usable `class_schedules.npz` and `room_bookings.npz` files

  ```sh
  python3 schedulepacker.py
  ```

### `heatmap.py` or `roombookingview.py` to view analytics

- Run `./auto_mapping.sh` to save relevant plots to directories

  ```sh
  bash auto_mapping.sh

  ## or ##

  python3 heatmap.py CSCE EENG
  python3 roombookingview.py B242
  ```
