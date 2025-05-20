import tkinter as tk
import csv
from tkinter import ttk
from tkinter import messagebox

# File paths for student and course CSV files
student_file_path = "students.csv"
course_file_path = "courses.csv"

# Surface of GUI
root = tk.Tk()
root.title("Student Information System")
root.geometry("1350x700+0+0")
root.config(bg="light gray")

# Title Label
title_label = tk.Label(root, text="STUDENT INFORMATION SYSTEM", font=("Bebas 12 bold"), fg="#fff", bg="#a41d21",
                       border=10, relief=tk.GROOVE)
title_label.pack(side=tk.TOP, fill=tk.X)

# Creating empty list to store students' data
students = []

# Creating empty list to store courses
courses = []

# Function to load student data from CSV file
def load_student_data():
    try:
        with open(student_file_path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        # Display an error message if the file is not found
        messagebox.showerror('File Not Found', 'Student data file not found.')

# Function to save student data to CSV file
def save_student_data():
    try:
        with open(student_file_path, 'w', newline='') as file:
            fieldnames = ['Name', 'ID_Number', 'Year_Level', 'Course', 'Gender']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)
    except:
        # Display an error message if there is an issue with saving the data
        messagebox.showerror('Error', 'Error saving student data.')

# Function to load course data from CSV file
def load_course_data():
    try:
        with open(course_file_path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                courses.append(row)
    except FileNotFoundError:
        # Display an error message if the file is not found
        messagebox.showerror('File Not Found', 'Course data file not found.')

# Function to save course data to CSV file
def save_course_data():
    try:
        with open(course_file_path, 'w', newline='') as file:
            fieldnames = ['CourseCode', 'CourseName']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            # Assuming the courses list contains dictionaries with 'CourseCode' and 'CourseName' keys
            for course in courses:
                writer.writerow({'CourseCode': course['CourseName'], 'CourseName': course['CourseCode']})
                
    except Exception as e:
        # Display an error message if there is an issue with saving the data
        messagebox.showerror('Error', f'Error saving course data: {str(e)}')
        
# Load student and course data when the application starts
load_student_data()
load_course_data()

### STUDENT ###

# Defining function that adds student on information system
def add_student():
    Name = name_entry.get()
    ID_Number = id_entry.get()
    Year_Level = year_entry.get()
    Course = course_entry.get()
    Gender = gender_entry.get()
    
    valid_courses = [course['CourseName'] for course in courses]
    if Course in valid_courses:
        # Creating student dictionary
        student = {'Name': Name, 'ID_Number': ID_Number, 'Year_Level': Year_Level, 'Course': Course, 'Gender': Gender}
        students.append(student)
        # Clearing Input fields
        name_entry.delete(0, tk.END)
        id_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        year_entry.set("")
        course_entry.delete(0, tk.END)
        gender_entry.delete(0, tk.END)
        gender_entry.set("")
    else:
        # Display an error message if the course is not valid
        messagebox.showerror('Invalid Course', 'The entered course is not valid.')

    # Save the updated student data to the CSV file
    save_student_data()
    list_students()
# Defining function that deletes student on information system
def delete_student():
    ID_Number = id_entry.get()
    for student in students:
        if student['ID_Number'] == ID_Number:
            students.remove(student)
            myoutput.delete(*myoutput.get_children())
            for student in students:
                myoutput.insert("", tk.END, values=(student['Name'], student['ID_Number'], student['Year_Level'],student['Course'], student['Gender']))
            break
        
    # Removing input fields
    id_entry.delete(0, tk.END)
    # Save the updated student data to the CSV file
    save_student_data()
    list_students()

# Defining function that edits student on information system
def edit_student():
    ID_Number = id_entry.get()
    for student in students:
        if student['ID_Number'] == ID_Number:
            Name = name_entry.get()
            Year_Level = year_entry.get()
            Course = course_entry.get()
            Gender = gender_entry.get()

            # Check if the course is available
            if Course in [course['CourseName'] for course in courses]:
                student['Name'] = Name
                student['Year_Level'] = Year_Level
                student['Course'] = Course
                student['Gender'] = Gender
                myoutput.delete(*myoutput.get_children())
                for student in students:
                    myoutput.insert("", tk.END, values=(student['Name'], student['ID_Number'], student['Year_Level'], student['Course'], student['Gender']))
                # Clearing input fields
                id_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
                year_entry.delete(0, tk.END)
                year_entry.set("")
                course_entry.delete(0, tk.END)
                gender_entry.delete(0, tk.END)
                gender_entry.set("")
            else:
                # Display an error message if the course is not available
                messagebox.showerror('Invalid Course', 'The entered course is not available.')
            break
     
    # Save the updated student data to the CSV file
    save_student_data()
    list_students()
# Defining function that shows the list of students on information system
def list_students():
    myoutput.delete(*myoutput.get_children())
    # Add column headings with bold font
    myoutput.heading("Name", text="Name")
    myoutput.heading("ID_Number", text="ID Number")
    myoutput.heading("Year_Level", text="Year Level")
    myoutput.heading("Course", text="Course Code")
    myoutput.heading("Gender", text="Gender")
    # Displays students in the list
    for student in students:
        myoutput.insert("", tk.END, values=(student['Name'], student['ID_Number'],student['Year_Level'], student['Course'], student['Gender']))

# Defining function that search students' on information system
def search_students():
    query = search_entry.get()
    myoutput.delete(*myoutput.get_children())
    # Displays students that match query
    for student in students:
        if query.lower() in student['Name'].lower() or query.lower() in student['ID_Number'].lower():
            myoutput.insert("", tk.END, values=(student["Name"], student["ID_Number"], student['Year_Level'], student["Course"], student['Gender']))
    search_entry.delete(0, tk.END)
    
 # Background Data Frame
data_frame = tk.LabelFrame(root, bg="gray", relief=tk.RIDGE, bd=5)
data_frame.place(x=25, y=60, height=610, width=700)

# Output Frames
output_area = tk.Frame(data_frame, bd=3)
output_area.place(x=20, y=310, height=280, width=622)

style = ttk.Style()
style.theme_use("alt")
style.configure('Treeview.Heading', font=('Arial', 10, 'bold'), background='light gray', foreground='black')
style.map('Treeview.Heading', background=[('selected', 'light gray')])

myoutput = ttk.Treeview(output_area, columns=("Name", "ID_Number", "Year_Level", "Course", "Gender"), show="headings")
myoutput.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

myoutput.heading("Name", text="Name")
myoutput.heading("ID_Number", text="ID Number")
myoutput.heading("Year_Level", text="Year Level")
myoutput.heading("Course", text="Course Code")
myoutput.heading("Gender", text="Gender")

myoutput.column("Name", anchor="center")
myoutput.column("ID_Number", width=100, anchor="center")
myoutput.column("Year_Level", width=100, anchor="center")
myoutput.column("Course", anchor="center", width=100)
myoutput.column("Gender", anchor="center", width=100)

y_scrollbar = tk.Scrollbar(data_frame, orient="vertical", command=myoutput.yview)
y_scrollbar.place(x=640, y=310, height=280)
myoutput.configure(yscrollcommand=y_scrollbar.set)

# Labels
name_label = tk.Label(data_frame, text="Name", font=("Bebas 14 bold"), fg="white", bg="gray")
name_label.place(x=30, y=50)
id_label = tk.Label(data_frame, text="ID Number", font=("Bebas 14 bold"), fg="white", bg="gray")
id_label.place(x=380, y=50)
year_label = tk.Label(data_frame, text="Year Level", font=("Bebas 14 bold"), fg="white", bg="gray")
year_label.place(x=30, y=100)
course_label = tk.Label(data_frame, text="Course Code", font=("Bebas 14 bold"), fg="white", bg="gray")
course_label.place(x=380, y=100)
gender_label = tk.Label(data_frame, text = "Gender", font= ("Bebas 14 bold"), fg="white", bg="gray")
gender_label.place(x=30, y=150 )

# Entry Fields
name_entry = tk.Entry(data_frame, font=("Arial", 12), bd=2)
name_entry.place(x=100, y=50, width=250)
id_entry = tk.Entry(data_frame, font=("Arial", 12), bd=2)
id_entry.place(x=500, y=50, width=150)
year_values = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
year_entry = ttk.Combobox(data_frame, values=year_values, font=("Arial 12"), state="readonly")
year_entry.place(x= 150, y=100 )
course_entry = tk.Entry(data_frame, font=("Arial", 12), bd=2)
course_entry.place(x=510, y=100, width=140)
gender_values = ["Male", "Female"]
gender_entry = ttk.Combobox(data_frame, values=gender_values, font=("Arial 12"), state="readonly")
gender_entry.place(x=120, y=150, width=230)

# Buttons
add_button = tk.Button(data_frame, bg="light gray", text="Add", bd=5, font=("Arial 10"), width=16, command=add_student)
add_button.place(x=70, y=210, width=120)
delete_button = tk.Button(data_frame, bg="light gray", text="Delete", bd=5, font=("Arial 10"), width=16, command=delete_student)
delete_button.place(x=210, y=210, width=120)
edit_button = tk.Button(data_frame, bg="light gray", text="Edit", bd=5, font=("Arial 10"), width=16, command=edit_student)
edit_button.place(x=350, y=210, width=120)
list_button = tk.Button(data_frame, bg="light gray", text="List", bd=5, font=("Arial 10"), width=10, command=list_students)
list_button.place(x=490, y=210, width=120)

# Search Entry Field
search_label = tk.Label(data_frame, text="Search by Name or ID Number:", font=("Bebas 12 bold"), fg="white", bg="gray")
search_label.place(x=30, y=270)
search_entry = tk.Entry(data_frame, font=("Arial", 12), bd=3)
search_entry.place(x=275, y=270, width=200)

# Search Button
search_button = tk.Button(data_frame, bg="light gray", text="Search", bd=5, font=("Arial 10"), width=12, command=search_students)
search_button.place(x=500, y=266, width=110)

### COURSES ###

# Defining function to add a new course
def add_course():
    CourseName = courses_entry.get()
    CourseCode = coursecode_entry.get()
    # Creating course dictionary
    course1 = {'CourseCode': CourseCode,'CourseName': CourseName}
    courses.append(course1)
    # Clearing Input fields
    courses_entry.delete(0, tk.END)
    coursecode_entry.delete(0, tk.END)
    # Save the updated course data to the CSV file
    save_course_data()
    list_courses()
# Function to update a course
def update_course():
    CourseName = courses_entry.get()
    for course1 in courses:
        if course1['CourseName'] == CourseName:
            course1['CourseCode'] = coursecode_entry.get()
            course_tree.delete(*course_tree.get_children())
            for course1 in courses:
                course_tree.insert("", tk.END, values=(course1['CourseName'], course1['CourseCode']))
            # Clearing input fields
            courses_entry.delete(0, tk.END)
            coursecode_entry.delete(0, tk.END)
            break        
        # Save the updated course data to the CSV file
    save_course_data()
    list_courses()
# Function to delete a course
def delete_course():
    CourseName = courses_entry.get()
    for course1 in courses:
        if course1['CourseName'] == CourseName:
            courses.remove(course1)
            course_tree.delete(*course_tree.get_children())
            for course1 in courses:
                course_tree.insert("", tk.END, values=(course1['CourseName'], course1['CourseCode']))
            # Removing input fields
            coursecode_entry.delete(0, tk.END)
            courses_entry.delete(0,tk.END)
            break
        # Save the updated course data to the CSV file
    save_course_data()

# Function to list available courses
def list_courses():
    # Clear existing entries in the course_tree
    course_tree.delete(*course_tree.get_children())

    # If there are no courses, return without adding any entries
    if not courses:
        return

    # Add column headings only if they are not already present
    if not course_tree["columns"]:
        course_tree["columns"] = ("Course Code", "Course Name")
        course_tree.heading("Course Code", text="Course Code")
        course_tree.heading("Course Name", text="Course Name")

    # Display courses in the list
    for course1 in courses:
        course_tree.insert("", tk.END, values=(course1['CourseName'], course1['CourseCode']))
#course frame
course_frame = tk.LabelFrame(root,bg="gray", relief=tk.RIDGE, bd=5)
course_frame.place(x=780, y=60, height=610, width=540)

# Course Treeview
course_tree = ttk.Treeview(course_frame, columns=("Course Code", "Course Name"), show="headings")
course_tree.place(x=20, y=230, width=480, height=330)
course_tree.heading("Course Code", text="Course Code")
course_tree.heading("Course Name", text="Course Name")

y_scrollbar_course = tk.Scrollbar(course_frame, orient="vertical", command=course_tree.yview)
y_scrollbar_course.place(x=500, y=230, height=330)
course_tree.configure(yscrollcommand=y_scrollbar_course.set)

#Course Label
courselabel = tk.Label(course_frame, text="COURSES", font=("Bebas 25 bold"), fg="white", bg="gray")
courselabel.place(x=175, y=15)
coursescodelabel = tk.Label(course_frame, text="Course Code", font=("Bebas 14 bold"), fg="white", bg="gray")
coursescodelabel.place(x=20, y=80)
coursesnamelabel = tk.Label(course_frame, text="Course Name", font=("Bebas 14 bold"), fg="white", bg="gray")
coursesnamelabel.place(x=20, y=120)

# Create an Entry widget for course input
courses_entry = tk.Entry(course_frame, font=("Arial", 12), bd=2)
courses_entry.place(x=160, y=80, width=200)
coursecode_entry = tk.Entry(course_frame, font=("Arial 12"), bd=2)
coursecode_entry.place(x=160, y=120, width=300)

# Add Course Button
add_course_button = tk.Button(course_frame, bg="light gray", text="Add Course", bd=5, font=("Arial 10"), width=16, command=add_course)
add_course_button.place(x=50, y=170, width=85)


# Update Course Button
update_course_button = tk.Button(course_frame, bg="light gray", text="Edit Course", bd=5, font=("Arial 10"), width=16, command=update_course)
update_course_button.place(x=155, y=170, width=85)

# Delete Course Button
delete_course_button = tk.Button(course_frame, bg="light gray", text="Delete Course", bd=5, font=("Arial 10"), width=16, command=delete_course)
delete_course_button.place(x=260, y=170, width=95)

# Available Courses Button
courses_button = tk.Button(course_frame, bg="light gray", text="Course List", bd=5, font=("Arial 10"), width=16, command=list_courses)
courses_button.place(x=375, y=170, width=120)

# Starting the main loop
root.mainloop()
                
