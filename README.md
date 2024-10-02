
# cis6930fa24 -- Project0

## Author

**Name**: Balasai Srikanth Ganti

**UFID** : 5251-6075

## Assignment Description 
This project is designed to download police department daily incident report PDFs, extract and process the relevant incident data such as date/time, incident number, location, nature, and ORI. The extracted data is stored in a SQLite database for querying and analysis.


## How to install

To set up the environment, use pipenv to install the dependencies.

```bash
pipenv install .
```

## How to run
Run the program using the following commands:

### Fetch data from the data:
```bash
pipenv run python project0/main.py --incidents <URL_of_incident_report_PDF>

```

### Example:
```bash
pipenv run python project0/main.py --incidents https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf
```

The script will download the PDF, extract incidents, store them in the database, and print a summary of the incidents by nature.

After the incident data has been populated into the database, the program will output the number of occurrences for each incident nature.

## Expected output

After running the main program with the provided PDF incident report, the following is the expected outputs:

```bash
Aid|2
Alarm|16
Area|7
Assignment|3
Assist|10
Burglary|1
....

```


## Functions

#### main.py
- **fetch_incidents(url)**: Downloads the PDF from the provided URL and saves it locally.
- **split_line_regex(line)**: Loads data from the specified local JSON file.
- **extract_data(data)**: Extracts date_time, incident number, location, nature, and incident ORI using regular expressions.
- **extract_incidents(df_file_path)**: Extracts incident data from the PDF using pypdf, splits the lines, and extracts relevant fields.
- **create_db()**: Creates the SQLite database and the incidents table if not already present.
- **populate_db(conn, incidents_df)**: Inserts the incidents from the DataFrame into the SQLite database.
- **query(conn)**: Queries the database for the count of each incident nature and prints the results.

#### Libraries used
- **pandas**: Used for creating and manipulating DataFrames.
- **sqlite3**: Used for interacting with the SQLite database.
- **Pypdf**: Used for reading and extracting text from PDF files.
- **urllib.request**: Used for making HTTP requests to download the PDF.
- **re**: Used for regular expressions to parse text data.
- **os**: Used for handling file paths and file removal.
- **logging**: Used for logging messages and errors.
- **argparse**: Used for handling command-line arguments.

## Database Development
The project uses SQLite as the database to store incident data. Data is inserted into the table from the extracted incidents. The incidents table is created with the following structure:

- incident_time (TEXT)
- incident_number (TEXT UNIQUE)
- incident_location (TEXT)
- nature (TEXT)
- incident_ori (TEXT)

## Testcases

To ensure the core functionalities of this project work as expected, several unit tests have been implemented using the pytest framework.


- **test_fetch_incidents()**: This test checks the functionality of the fetch_incidents() function by verifying if the incident report PDF is correctly downloaded from the provided URL.

- **test_create_db()**: This test verifies the functionality of the create_db() function by checking if the SQLite database is created and the incidents table exists.

- **test_populate_db()**: This test verifies the correct functioning of the populate_db() function. It checks whether the extracted incidents from the PDF file are successfully inserted into the SQLite database.


## How to run tests:
Make sure the following are installed in your environment:

1. **pipenv**: Used to manage the virtual environment.
2. **pytest**: Python testing framework.

To install all dependencies, run:

```bash
pipenv install

```

To run the testcases you go with the following command:

```bash
pipenv run python -m pytest -v
```



## Bugs and Assumptions:

1.  **Assumptions**: 

- The PDF structure remains consistent for correct parsing of the incident data.

- Each line in the PDF follows a known format with date_time, incident number, location, nature, and ORI.

2.  **Bugs**: 
- Handling of unexpected line formats may fail. Currently, lines that don't match the expected format are skipped.




