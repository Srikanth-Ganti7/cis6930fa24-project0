import re
import pandas as pd
import sqlite3
import os
import logging
#from PyPDF2 import PdfReader
from pypdf import PdfReader

import urllib.request

# Function to download the PDF
def fetch_incidents(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)

    # Check the response status and size
    #print(f"Response status: {response.status}")
    pdf_data = response.read()
    #print(f"Downloaded PDF size: {len(pdf_data)} bytes")

    # Save the file locally
    with open('../incident_report.pdf', 'wb') as f:
        f.write(pdf_data)

    return '../incident_report.pdf'

# Set up logging to overwrite on every new run
logging.basicConfig(filename='incident_parsing.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s', filemode='w')

# Split the line based on patterns
def split_line_regex(line):
    """
    Extracts fields from a line of text from the incident report.
    Assumes the line contains:
    - date_time
    - incident_number
    - location
    - nature
    - incident_ori
    """
    # Regular expression to capture date_time, incident_number, and incident_ori
    match = re.match(r'(\d+/\d+/\d+\s\d+:\d+)\s+(\S+)\s+(.*)\s+(\S+)$', line)
    
    if match:
        date_time = match.group(1)
        incident_number = match.group(2)
        incident_ori = match.group(4)
        
        # Everything between incident_number and incident_ori is 'location' and 'nature'
        middle_part = match.group(3)
        
        # Try to split 'middle_part' into 'location' and 'nature' (this is an assumption based on patterns)
        location_nature = middle_part.rsplit(' ', 1)
        if len(location_nature) == 2:
            location, nature = location_nature
        else:
            # In case it's not splitable, assign the entire middle_part as location and leave nature empty
            location = middle_part
            nature = ''
        
        # Log the fields extracted for debugging
        logging.info(f"Extracted fields: {date_time}, {incident_number}, {location}, {nature}, {incident_ori}")
        return [date_time, incident_number, location, nature, incident_ori]
    else:
        logging.info(f"Line didn't match pattern: {line}")
        return []

# Function to parse the PDF file and return a DataFrame
def extract_incidents(pdf_file_path):
    """
    Extract incidents from a PDF using PyPDF2 and return a DataFrame.
    """
    incidents = []
    reader = PdfReader(pdf_file_path)
    num_pages = len(reader.pages)
    
    logging.info(f"Reading PDF file: {pdf_file_path} with {num_pages} pages.")
    
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        text = page.extract_text()  # Extract the text from each page
        
        if text:
            lines = text.split('\n')
            #print(f"\n=== Page {page_num} Lines ===\n{lines}\n")  # Print raw lines for debugging
            
            for line_num, line in enumerate(lines):
                # Skip headers, junk lines, or lines without sufficient data
                if "Incident Number" in line or "NORMAN POLICE" in line or not line.strip():
                    logging.info(f"Skipped header or junk line: {line}")
                    continue

                fields = split_line_regex(line)

                if len(fields) == 5:
                    incidents.append({
                        'date_time': fields[0],
                        'incident_number': fields[1],
                        'location': fields[2],
                        'nature': fields[3],
                        'incident_ori': fields[4]
                    })
                else:
                    logging.info(f"Skipped line (incomplete): {line}")

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(incidents, columns=['date_time', 'incident_number', 'location', 'nature', 'incident_ori'])
    
    logging.info(f"Extracted {len(df)} incidents.")
    
    # Print the DataFrame for debugging
    #print(df.head())
    
    return df

# Create SQLite Database
def create_db():
    db_path = os.path.abspath('../resources/normanpd.db')
    #print(f"Database path: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT UNIQUE,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')
    conn.commit()
    return conn

# Insert data into the database
def populate_db(conn, incidents_df):
    if incidents_df.empty:
        print("No incidents to insert, DataFrame is empty.")
        return

    cursor = conn.cursor()

    try:
        # Iterate through each row in the DataFrame
        for index, incident in incidents_df.iterrows():
            #print(f"Inserting: {incident.to_dict()}")
            cursor.execute('''
                INSERT OR IGNORE INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
                VALUES (?, ?, ?, ?, ?)
            ''', (incident['date_time'], incident['incident_number'], incident['location'], incident['nature'], incident['incident_ori']))
        conn.commit()
        #print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")

# Function to print all incidents from the database
def print_all_incidents(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents")
    rows = cursor.fetchall()
    if not rows:
        print("No incidents found in the database.")
    for row in rows:
        print(row)

# Function to print the status of incidents by nature
def query(conn):
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT nature, COUNT(*) as count
        FROM incidents
        GROUP BY nature
        ORDER BY nature ASC
    ''')
    
    rows = cursor.fetchall()
    
    # Print each nature and its count, formatted as 'Nature|Count'
    for row in rows:
        nature, count = row
        print(f"{nature}|{count}")

# Main function
def main(url):
    # Download the PDF file
    pdf_file = fetch_incidents(url)
    
    # Extract incident data from the PDF
    incidents_df = extract_incidents(pdf_file)
    
    # Create the database and insert the data
    conn = create_db()
    populate_db(conn, incidents_df)

    # Print the status of each nature of incidents
    #print("=== Status of Incidents by Nature ===")
    query(conn)
    
    # Print all inserted incidents
    # print("=== All Incidents in the Database ===")
    # print_all_incidents(conn)
    
    conn.close()

# Argument parser for command-line execution
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL.")
    
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
