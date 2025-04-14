import time
import random
import json
import requests

from db import create_patient_table, insert_patient

# ---------------------------
# FHIR Data Fetching and Extraction Functions
# ---------------------------

FHIR_BASE_URL = "https://fhir.example.com"  # Replace with your actual FHIR server.
# For demonstration, we'll simulate patient IDs.
SIMULATED_PATIENT_IDS = ["patient-001", "patient-002", "patient-003"]

headers = {
    "Accept": "application/fhir+json",
    # "Authorization": "Bearer YOUR_ACCESS_TOKEN",  # Include if needed.
}

def fetch_patient_data(patient_id):
    """
    Simulate retrieving a Patient resource from the FHIR server.  
    In a real implementation, this makes an HTTP GET call.
    """
    # For simulation, we construct a fake FHIR Patient JSON.
    # You can uncomment the next lines to use an actual HTTP request if you have a FHIR server.
    # fhir_endpoint = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    # response = requests.get(fhir_endpoint, headers=headers)
    # response.raise_for_status()
    # return response.json()

    # Simulated FHIR Patient data
    simulated_data = {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{
            "family": f"Family{random.randint(1,99)}",
            "given": [f"Name{random.randint(1,99)}"]
        }],
        "gender": random.choice(["male", "female", "other"]),
        "birthDate": "1980-01-01"
    }
    return simulated_data

def parse_patient_data(fhir_data):
    """
    Parse key patient fields from the FHIR Patient resource.
    Returns a dictionary with:
    - id
    - resourceType
    - PatientName (concatenated given and family names)
    - gender
    - birthDate
    """
    extracted_data = {}
    
    extracted_data["id"] = fhir_data.get("id", "Unknown")
    extracted_data["resourceType"] = fhir_data.get("resourceType", "Unknown")
    
    names = fhir_data.get("name", [])
    if names:
        first_name_entry = names[0]
        family = first_name_entry.get("family", "")
        given = " ".join(first_name_entry.get("given", []))
        extracted_data["PatientName"] = f"{given} {family}".strip()
    else:
        extracted_data["PatientName"] = "Not Provided"
    
    extracted_data["gender"] = fhir_data.get("gender", "Not Provided")
    extracted_data["birthDate"] = fhir_data.get("birthDate", "Not Provided")
    
    return extracted_data

# ---------------------------
# Simulated Streaming Functionality
# ---------------------------
def simulated_fhir_stream():
    """
    Simulate a stream of FHIR Patient data.
    In a real system, this could be reading from a message broker or an event queue.
    """
    while True:
        # Randomly select a patient id from the simulated list.
        patient_id = random.choice(SIMULATED_PATIENT_IDS)
        # Fetch and yield a simulated FHIR Patient record.
        yield fetch_patient_data(patient_id)
        
        # Simulate random intervals for message arrival.
        time.sleep(random.uniform(1, 3))

def main():
    # Ensure that the patients table exists.
    create_patient_table()
    
    print("Starting FHIR streaming application. Press Ctrl+C to stop.")
    
    try:
        # Iterate over the simulated FHIR stream.
        for fhir_data in simulated_fhir_stream():
            # Extraction Phase: Parse the FHIR Patient data.
            patient_info = parse_patient_data(fhir_data)
            
            # Load Phase: Insert or update the patient record in PostgreSQL.
            insert_patient(patient_info)
            
            # Optionally print out the processed data.
            print("Processed Patient:", patient_info)
    except KeyboardInterrupt:
        print("Streaming application stopped.")

if __name__ == "__main__":
    main()
