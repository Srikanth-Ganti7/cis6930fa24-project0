import os
import pytest
import sqlite3
from project0.main import fetch_incidents, extract_incidents, populate_db

# Test fetch_incidents
def test_fetch_incidents():
    # Test with a valid URL for fetching the incident PDF
    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
    pdf_path = fetch_incidents(url)
    
    # Check if the file was saved properly
    assert os.path.exists(pdf_path), "PDF file not saved."
    assert os.path.getsize(pdf_path) > 0, "PDF file is empty."

    # Clean up by removing the fetched file
    os.remove(pdf_path)

# Test extraction of incidents
def test_extract_incidents():
    # URL for the incident summary PDF
    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
    
    # Download the PDF and extract incidents
    pdf_file = fetch_incidents(url)
    incidents_df = None

    try:
        incidents_df = extract_incidents(pdf_file)
    except TypeError as e:
        pytest.fail(f"Extract incidents failed due to TypeError during extraction: {e}")

    # Ensure that incidents_df is valid
    assert incidents_df is not None, "extract_incidents returned None."
    assert not incidents_df.empty, "No incidents were extracted."

    # Clean up
    os.remove(pdf_file)

# Test populating the database
def test_populate_db():
    # URL for the incident summary PDF
    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
    
    # Download the PDF and extract incidents
    pdf_file = fetch_incidents(url)
    incidents_df = extract_incidents(pdf_file)
    
    # Create an in-memory database
    conn = sqlite3.connect(':memory:')

    # Create the table in the in-memory database
    conn.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT UNIQUE,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')
    
    try:
        populate_db(conn, incidents_df)
    except Exception as e:
        pytest.fail(f"populate_db failed with exception: {e}")

    # Check if the data was inserted properly
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents")
    count = cursor.fetchone()[0]

    assert count == len(incidents_df), "Data was not inserted properly into the database."

    # Clean up
    conn.close()
    os.remove(pdf_file)