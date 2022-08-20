import sqlite3
import re
from datetime import datetime

import matplotlib.pyplot as plt

def options(userId):
    choice = 1
    while choice != 4:
        while True:
            try:
                print("****************************")
                print("Admin's Window Menu Options")
                print("****************************")
                print("1. Report - Consultation")
                print("2. Report - Patient visits")
                print("3. Report - Doctors availability")
                print("4. Logout")
                choice = int(input("Please select an operation (eg: 1) : "))
                break
            except:
                print("Please input a digit (eg: 1)")
        if choice > 4 or choice <= 0:
            print("Invalid choice. Please try again.")
        else:
            if choice == 1:
                reportOne()
            if choice == 2:
                reportTwo()
            if choice == 3:
                reportThree()

    print("4. Logout selected")
    print("Returning to application main window.")

def reportOne():
    today = datetime.today()
    date = '%-'+str(today.month)+'-'+str(today.year)+'%'

    connection = sqlite3.connect("walkinclinic.db")
    cursor = connection.cursor()
    cursor.execute("select dd.FirstName,count(b.Id) from DoctorDetails dd join booking b on dd.Id = b.doctor_id group by dd.Id,dd.FirstName")
    docresult = cursor.fetchall()
    cursor.close()
    connection.close()

    left = []
    height = []
    tick_label = []

    i=1

    for item in docresult:
        tick_label.append(item[0])
        height.append(item[1])
        left.append(i)
        i = i + 1

    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['red', 'green'])

    # naming the x-axis
    plt.xlabel('Doctor')
    # naming the y-axis
    plt.ylabel('Patients visited')
    # plot title
    plt.title('Consultation Graph')

    # function to show the plot
    plt.show()

def reportTwo():
    today = datetime.today()
    date = '%-'+str(today.month)+'-'+str(today.year)+'%'

    connection = sqlite3.connect("walkinclinic.db")
    cursor = connection.cursor()
    cursor.execute("select dd.FirstName,count(b.Id) from PatientDetails dd join booking b on dd.Patient_Id = b.patient_id group by dd.Patient_Id,dd.FirstName")
    docresult = cursor.fetchall()
    cursor.close()
    connection.close()

    left = []
    height = []
    tick_label = []
    i = 1

    for item in docresult:
        tick_label.append(item[0])
        height.append(item[1])
        left.append(i)
        i = i + 1

    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['red', 'green'])

    # naming the x-axis
    plt.xlabel('Patient')
    # naming the y-axis
    plt.ylabel('Patients visits')
    # plot title
    plt.title('Visit Graph')

    # function to show the plot
    plt.show()

def reportThree():
    today = datetime.today()
    date = '%-'+str(today.month)+'-'+str(today.year)+'%'

    connection = sqlite3.connect("walkinclinic.db")
    cursor = connection.cursor()
    cursor.execute("select dd.FirstName,count(b.Id) from DoctorDetails dd join slots b on dd.Id = b.doctor_id group by dd.Id,dd.FirstName")
    docresult = cursor.fetchall()
    cursor.close()
    connection.close()

    left = []
    height = []
    tick_label = []
    i = 1

    for item in docresult:
        tick_label.append(item[0])
        height.append(item[1])
        left.append(i)
        i = i + 1

    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['red', 'green'])

    # naming the x-axis
    plt.xlabel('Doctor')
    # naming the y-axis
    plt.ylabel('Slots')
    # plot title
    plt.title('Availability Graph')

    # function to show the plot
    plt.show()