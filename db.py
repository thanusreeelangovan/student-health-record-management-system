import mysql.connector
from config import DB_CONFIG

# Connect to DB
db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

# Create table if not exists
def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS HealthRecords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Surname VARCHAR(255),
            Age INT,
            Gender VARCHAR(10),
            BloodType VARCHAR(10),
            Class VARCHAR(10),
            Section VARCHAR(10),
            Height FLOAT,
            Weight FLOAT,
            BMI FLOAT,
            BloodPressure VARCHAR(20),
            DOB DATE,
            RightEye VARCHAR(10),
            LeftEye VARCHAR(10)
        )
    """)
    db.commit()

# Insert record
def insert_record(record):
    cursor.execute("""
        INSERT INTO HealthRecords
        (Name, Surname, Age, Gender, BloodType, Class, Section,
        Height, Weight, BMI, BloodPressure, DOB,
        RightEye, LeftEye)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        record['Name'], record['Surname'], record['Age'], record['Gender'], record['BloodType'],
        record['Class'], record['Section'], record['Height'], record['Weight'], record['BMI'],
        record['BloodPressure'], record['DOB'], record['RightEye'],
        record['LeftEye']
    ))
    db.commit()

# Fetch all records
def fetch_all():
    cursor.execute("SELECT * FROM HealthRecords")
    return cursor.fetchall()

# Delete a record
def delete_record(name):
    cursor.execute("DELETE FROM HealthRecords WHERE Name=%s", (name,))
    db.commit()

# Search by name
def search_record(name):
    cursor.execute("SELECT * FROM HealthRecords WHERE Name=%s", (name,))
    return cursor.fetchone()

# Filter by class and section
def filter_records(class_name, section_name):
    cursor.execute("SELECT * FROM HealthRecords WHERE Class=%s AND Section=%s",
                   (class_name, section_name))
    return cursor.fetchall()
