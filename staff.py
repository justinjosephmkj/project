import sqlite3
import re
from datetime import datetime
def options(userId):
    choice = 1
    while choice != 6:
        while True:
            try:
                print("****************************")
                print("Staff's Window Menu Options")
                print("****************************")
                print("1. Patient Registration")
                print("2. Slot Booking")
                print("3. View Last Prescription")
                print("4. Doctor profile creation")
                print("5. Doctor's Availability addition")
                print("6. Logout")
                choice = int(input("Please select an operation (eg: 1) : "))
                break
            except:
                print("Please input a digit (eg: 1)")
        if choice > 6 or choice <= 0:
            print("Invalid choice. Please try again.")
        else:
            if choice == 1:
                patientRegistration()
            if choice == 2:
                bookSlotsStaff()
            if choice == 3:
                viewPrescription()
            if choice == 4:
                addDoctor()
            if choice == 5:
                addDoctorAvailability()

    print("5. Logout selected")
    print("Returning to application main window.")


def patientRegistration():
    print("Patine Registration Selected")
    try:
        firstname = input('First Name: ')
        secondname = input('Second Name: ')
        gender = input('Gender: ')
        age = input('Age: ')
        maritalstatus = input('Marital Status: ')
        bloodtype = input('Blood Type: ')
        primarycontact = input('Primary contact: ')
        secondarycontact = input('Secondary contact: ')
        emergencycontact = input('Emergency contact: ')

        connection = sqlite3.connect("walkinclinic.db")
        cursor = connection.cursor()
        cursor.execute(
            "insert into PatientDetails (FirstName, SecondName, Gender, Age, MaritalStatus, BloodType, PrimaryContact, SecondaryContact, EmergencyContact) values (?,?,?,?,?,?,?,?,?)",
            (firstname, secondname, gender, age, maritalstatus, bloodtype, primarycontact,
             secondarycontact, emergencycontact));
        cursor.execute("COMMIT;")
        cursor.close()
        connection.close()
        print("Patient Registration completed successfully.")
    except:
        print("An error occured, please try agian.")

def bookSlotsStaff():
    print("Slot Booking Selected")
    print("Please select doctor's id for slot booking.")

    connection = sqlite3.connect("walkinclinic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT Id,FirstName,SecondName FROM DoctorDetails ;")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    for row in result:
        data = ' '.join(str(item) for item in row)
        print(data)

    try:
        id = int(input("Please enter a doctor's id (eg: 1) : "))
        connection = sqlite3.connect("walkinclinic.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM DoctorDetails where id = ? ;", [id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row == None:
            print("Invalid Id!")
        else:
            print("Please enter the date for booking.")
            date = input("Please enter date (dd-mm-yy, eg: 28-12-2021) : ")
            regexEmail = r'\b[0-9][0-9]-[0-9][0-9]-[2][0][2-9][2-9]\b'
            if re.fullmatch(regexEmail, date):
                dt = datetime.strptime(date, '%d-%m-%Y')
                day = dt.strftime('%a').lower()
                connection = sqlite3.connect("walkinclinic.db")
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM slots where day =? and doctor_id = ? ;", [day, id])
                result = cursor.fetchall()
                cursor.close()
                connection.close()

                connection = sqlite3.connect("walkinclinic.db")
                cursor = connection.cursor()
                cursor.execute("SELECT slot_id FROM booking where date = ? and doctor_id = ? ;", [date, id])
                booking = cursor.fetchall()
                cursor.close()
                connection.close()

                bookingIds = []
                slotsIds = []

                for item in booking:
                    bookingIds.append(item[0])

                status = True

                for row in result:
                    if (row[0] not in bookingIds):
                        if status:
                            print('#Id #Day #Hour #Minute')
                            status = False
                        print(row[0],row[1],',',row[2],':',row[3])
                        slotsIds.append(row[0])

                if status == False:

                    try:
                        slotId = int(input("Please enter a slot id for booking (eg: 1) : "))
                    except:
                        print("Invalid Slot Id!")

                    try:
                        patientId = int(input("Please enter patient id for booking (eg: 1) : "))
                    except:
                        print("Invalid Patient Id!")

                    if (slotId not in slotsIds):
                        print("Invalid Slot Id!")
                    else:

                        connection = sqlite3.connect("walkinclinic.db")
                        cursor = connection.cursor()
                        cursor.execute("INSERT INTO booking (doctor_id, patient_id,date,slot_id) values (?,?,?,?);",
                                       [id, patientId, date, slotId])
                        cursor.execute("COMMIT;")
                        cursor.close()
                        connection.close()
                        print("Booking added successfully.")

                else:
                    print("No slots available for the given date and the doctor! Please choose another doctor or date.")

            else:
                print("Invalid date!")
    except:
        print("Invalid Doctor's id (eg: 1)")



def viewPrescription():
    id = int(input("Please enter a patient's id (eg: 1) : "))
    connection = sqlite3.connect("walkinclinic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT PATIENTID, MEDICINES from PRESCRIPTION where PATIENTID = ? order by Id desc;", [id])
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row == None:
        print("Invalid Id!")
    else:
        print('Patient ID : ', row[0])
        print('Medication prescribed :', row[1])

def addDoctor():
    print("Doctor Registration Selected")
    try:
        firstname = input('First Name: ')
        secondname = input('Second Name: ')
        gender = input('Gender: ')
        age = input('Age: ')
        maritalstatus = input('Marital Status: ')
        bloodtype = input('Blood Type: ')
        primarycontact = input('Primary contact: ')
        secondarycontact = input('Secondary contact: ')
        emergencycontact = input('Emergency contact: ')
        qualificationAndLicence = input('Qualification and License: ')

        connection = sqlite3.connect("walkinclinic.db")
        cursor = connection.cursor()
        cursor.execute(
            "insert into DoctorDetails (FirstName, SecondName, Gender, Age, MaritalStatus, BloodType, PrimaryContact, SecondaryContact, EmergencyContact, QualificationAndLicence ) values (?,?,?,?,?,?,?,?,?,?)",
            (firstname, secondname, gender, age, maritalstatus, bloodtype, primarycontact,
             secondarycontact, emergencycontact,qualificationAndLicence));
        cursor.execute("COMMIT;")
        cursor.close()
        connection.close()
        print("Doctor Registration completed successfully.")
    except:
        print("An error occured, please try agian.")

def addDoctorAvailability():
    print("Please select doctor's id for slot addition")

    connection = sqlite3.connect("walkinclinic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT Id,FirstName,SecondName FROM DoctorDetails ;")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    for row in result:
        data = '. '.join(str(item) for item in row)
        print(data)
    try:
        id = int(input("Please enter a doctor's id (eg: 1) : "))
        connection = sqlite3.connect("walkinclinic.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM DoctorDetails where id = ? ;", [id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row == None:
            print("Invalid Id!")
        else:
            day = input("Please enter week day (eg: mon,tue,..,fri,sat) : ")
            weekDays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat']
            if day in weekDays:
                try:
                    starting_hour = int(input("Please enter the starting hour (24 hour format, eg: 10,11,..,23) : "))
                    try:
                        starting_min = int(input("Please enter the starting min ( 00 or 30) : "))
                    except:
                        print("Invalid Minute (00 or 30)")

                    connection = sqlite3.connect("walkinclinic.db")
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO slots (day, starting_hour,starting_minute,doctor_id) values (?,?,?,?);",
                                   [day, starting_hour, starting_min, id])
                    cursor.execute("COMMIT;")
                    cursor.close()
                    connection.close()
                    print("Availability added successfully.")

                    connection = sqlite3.connect("walkinclinic.db")
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM slots where doctor_id = ? ;", [id])
                    result = cursor.fetchall()
                    cursor.close()
                    connection.close()

                    print('#Id #Day #Hour #Minute')
                    for row in result:
                        print(row[0], row[1], ',', row[2], ':', row[3])

                except:
                    print("Invalid Hour! (24 hour format) (eg: 10,11,..)")
            else:
                print("Invalid Day!")

    except:
        print("Invalid Doctor's id (eg: 1)")