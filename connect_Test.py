import oracledb

# Establish a connection to the Oracle database
connection = oracledb.connect(
    user="system",
    password="dborcl",
    dsn="localhost:1522/xe"
)
cursor = connection.cursor()

# Function to add a new doctor
def add_doctor(D_Id, Name, Department):
    try:
        d_id = int(D_Id)  # Convert D_Id to int
        dept = Department  # Keep Department as a string if necessary, or convert if needed
        
        cursor.execute("""
            INSERT INTO Doctors (D_Id, Name, Department)
            VALUES (:1, :2, :3)
        """, [d_id, Name, dept])
        
        connection.commit()
        return "Doctor added successfully."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

def add_patient(ID, Name, Contact_Number, Disease_Name, Department, Doctor_id, Treatment_Details): 
    try:
        # Convert inputs to required types and validate them
        try:
            patient_id = int(ID)  # Convert ID to int
            dept = int(Department)  # Convert Department to int
            doc_id = int(Doctor_id)  # Convert Doctor_id to int
        except ValueError:
            return "Patient ID, Department, and Doctor ID must be numeric values."

        # Ensure the contact number is valid (you can add more validation if needed)
        if len(Contact_Number) < 10:
            return "Please enter a valid contact number."

        # Execute the insert query
        cursor.execute("""
            INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Department, Doctor_id, Treatment_Details)
            VALUES (:1, :2, :3, :4, :5, :6, :7)
        """, [patient_id, Name, Contact_Number, Disease_Name, dept, doc_id, Treatment_Details])
        
        connection.commit()
        return "Patient added successfully."

    except oracledb.Error as error:
        return f"Error occurred: {error}"

# Function to check if patient ID already exists in the database
def check_patient_exists(patient_id):
    try:
        with connection.cursor() as cursor:
            query = "SELECT 1 FROM patients WHERE patient_id = :id"
            cursor.execute(query, id=patient_id)
            result = cursor.fetchone()
            return result is not None  # Returns True if patient exists, otherwise False
    except oracledb.DatabaseError as e:
        print(f"Error checking patient existence: {e}")  # Replace with logging if needed
        return False
    
# Function to edit doctor details
def edit_doctor_details(D_Id, Name=None, Department=None):
    try:
        updates = []
        params = {}

        if Name:
            updates.append("Name = :name")
            params["name"] = Name
        if Department:
            updates.append("Department = :department")
            params["department"] = Department

        if not updates:
            return "No updates specified."

        query = f"UPDATE Doctors SET {', '.join(updates)} WHERE D_Id = :d_id"
        params["d_id"] = D_Id
        cursor.execute(query, params)
        
        connection.commit()
        return "Doctor details updated successfully."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

# Function to delete a doctor
def delete_doctor(D_Id):
    try:
        d_id = int(D_Id)
        cursor.execute("DELETE FROM Doctors WHERE D_Id = :1", [d_id])
        
        connection.commit()
        return "Doctor deleted successfully."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

# Function to delete a patient
def delete_patient(ID):
    try:
        patient_id = int(ID)
        cursor.execute("DELETE FROM Patients WHERE ID = :1", [patient_id])
        
        connection.commit()
        return "Patient deleted successfully."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

def edit_patient_details(ID, field_name, new_value):
    try:
        valid_fields = {
            "Name": "Name",
            "Contact Number": "Contact_Number",
            "Disease Name": "Disease_Name",
            "Treatment Details": "Treatment_Details",
            "Department": "Department",
            "Doctor ID": "Doctor_id"
        }
        
        # Map user-friendly field name to database column name
        column_name = valid_fields.get(field_name)
        if not column_name:
            return "Invalid detail to edit specified."

        # Update query
        query = f"UPDATE Patients SET {column_name} = :new_value WHERE ID = :id"
        params = {"new_value": new_value, "id": int(ID)}
        
        # Execute the update
        cursor.execute(query, params)
        connection.commit()
        return "Patient details updated successfully."
    
    except oracledb.Error as error:
        return f"Error occurred: {error}"

def get_patient_data():
    """Fetch patient data from the database."""
    try:
        cursor = connection.cursor()  # Create a new cursor for this operation
        cursor.execute("""
            SELECT ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id 
            FROM Patients
        """)
        patient_data = cursor.fetchall()  # Fetching all patient data
    except oracledb.Error as error:
        print(f"Database error occurred: {error}")
        return []
    finally:
        cursor.close()  # Close the cursor after fetching data
    return patient_data

def get_doctor_data():
    """Fetch doctor data from the database."""
    try:
        cursor = connection.cursor()  # Create a new cursor for this operation
        cursor.execute("""
            SELECT D_ID, Name, Department
            FROM Doctors
        """)
        doctor_data = cursor.fetchall()  # Fetching all doctor data
    except oracledb.Error as error:
        print(f"Database error occurred: {error}")
        return []
    finally:
        cursor.close()  # Close the cursor after fetching data
    return doctor_data

