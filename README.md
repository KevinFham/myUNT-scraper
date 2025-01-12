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
  python3 scripts/scraper.py -t "2024 Fall" -x 1 -y 7 CSCE EENG BMEN MEEN MTSE  
  ```

### `htmlparser.py`

- Parse `.html` files within `./course` and populate `ENG_course_catalog_database.csv`

  ```sh
  python3 scripts/htmlparser.py
  ```

### `schedulepacker.py`

- Pack courses in the `.csv` into usable `class_schedules.npz` and `room_bookings.npz` files

  ```sh
  python3 scripts/schedulepacker.py
  ```

### `heatmap.py` or `roombookingview.py` to view analytics

- Run `./auto_mapping.sh` to save relevant plots to directories

  ```sh
  bash auto_mapping.sh

  ## or ##

  python3 scripts/heatmap.py CSCE EENG
  python3 scripts/roombookingview.py B242
  ```
