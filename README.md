# masip-ph-data-scraping
- MASIP Infrastructure Projects data scraping

### NEDA - ODA Data Cleaning
- We extracted the 'List of Active Loans' Annex table from yearly reports spanning 2010 to 2022. All raw data was stored in Google Spreadsheets for further processing.
- To ensure data consistency, we performed the following cleaning tasks:
    - Standardized headers across all datasets.
    - Transformed date strings into a consistent format (`MMM(M)-DD-YYYY`).
    - Merged cleaned data from each year into a single, comprehensive data file.

### Environmental Impact Assessments Data Scraping
- Project Identification:
    - We utilized NEDA-ODA data to manually identify infrastructure projects with significant loan amounts.
- Data Collection:
    - For each identified infrastructure project, we manually gathered available data and information and stored it in a spreadsheet format for further analysis and organization.
- Project Details:
    - In-depth information for each infrastructure project can be located in the "detailed_project_sheet" column.
    - We utilized the ABBYY Table OCR Tool to extract relevant tables from the "detailed_project_sheet" and convert them into a structured data format.
- Documentation of Detailed Data Sheet Organization:
    - General Source Information (`EIS` Tab):
        - The `EIS` tab contains general information regarding the source of the data.
    - Project Location Data (`Geoloc` Tab):
        - The `Geoloc` tab provides relevant location data associated with the projects. You can find additional tabs with corresponding table names mentioned in the `Geoloc` tab for further location-specific details.
    - Environmental Monitoring/Impact Data (`Observations` Tab):
        - The `Observations` tab contains data related to environmental monitoring or impact.

### Environmental Monitoring Reports Data Scraping
