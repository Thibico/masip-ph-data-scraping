# masip-ph-data-scraping
- MASIP Infrastructure Projects data scraping

### NEDA - ODA Data Cleaning
- We took 'List of Active Loans' Annex table from yearly reports through 2010-2022.
- All the raw data was on Google Spreadsheets. We'll pull the raw data, clean it if needed and combine into one.
- To publish as Datasette, we'll add data into SQLite db file.

#### Tasks to do
- List down all spreadsheet urls inside a specific folder
- For each spreadsheet, loop all tabs and combine data
    -  Challenge : headers can be different.
- Should I added data to sqlite?
    - Then, create data model with SQLAlchemy. (check final headers)


### Scrape ADB Projects - philippines
