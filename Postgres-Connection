import psycopg2
from psycopg2 import sql
import os

# Configure your PostgreSQL connection parameters.
DB_NAME = os.getenv("DB_NAME", "yourdbname")
DB_USER = os.getenv("DB_USER", "yourdbuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "yourdbpassword")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_connection():
    """Establish and return a database connection."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def create_patient_table():
    """Create the patients table if it doesn't already exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS patients (
        id TEXT PRIMARY KEY,
        resource_type TEXT,
        patient_name TEXT,
        gender TEXT,
        birth_date DATE
    )
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()
        print("Patient table is ready.")
    except Exception as e:
        print("Error creating table:", e)

def insert_patient(patient_data):
    """
    Insert a patient record into the patients table.
    
    patient_data: a dict containing keys: id, resourceType, PatientName, gender, birthDate.
    """
    insert_query = """
        INSERT INTO patients (id, resource_type, patient_name, gender, birth_date)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE 
          SET resource_type = EXCLUDED.resource_type,
              patient_name = EXCLUDED.patient_name,
              gender = EXCLUDED.gender,
              birth_date = EXCLUDED.birth_date;
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Use tuple unpacking from the dictionary.
        cur.execute(
            insert_query,
            (
                patient_data.get("id"),
                patient_data.get("resourceType"),
                patient_data.get("PatientName"),
                patient_data.get("gender"),
                patient_data.get("birthDate"),
            )
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"Inserted/Updated patient record for ID: {patient_data.get('id')}")
    except Exception as e:
        print("Error inserting patient record:", e)
