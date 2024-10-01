import os
import pytest
import sqlite3

from project0.main import fetch_incidents, create_db, populate_db, extract_incidents

# Test fetch_incidents
def test_fetch_incidents():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
    pdf_path_1 = fetch_incidents(url)
    
    # Check if the file was saved properly
    assert os.path.exists(pdf_path_1)
    assert os.path.getsize(pdf_path_1) > 0
    #os.remove(pdf_path)  # Cleanup the file after the test

def test_create_db():
    # Create the database
    conn = create_db()

    # Check if the connection is open
    assert conn is not None

    # Verify that the table 'incidents' exists
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    result = cursor.fetchone()

    # Ensure the table is created
    assert result is not None
    assert result[0] == 'incidents'

    # Close the connection
    conn.close()

    # Clean up the database file if needed
    #os.remove('resources/normanpd.db')

def test_populate_db():
    # URL for the incident summary PDF
    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
    
    # Download the PDF and extract incidents
    pdf_file = fetch_incidents(url)
    incidents_df = extract_incidents(pdf_file)

    # Create the database and insert incidents
    conn = create_db()
    populate_db(conn, incidents_df)

    # Check if the data has been inserted correctly
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents")
    count = cursor.fetchone()[0]

    # Ensure that some data has been inserted
    assert count > 0

    # Clean up
    conn.close()







