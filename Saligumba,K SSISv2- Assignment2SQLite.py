from tkinter import*
import tkinter as ssis
from tkinter import ttk
import tkinter.messagebox
import sqlite3

#________APPDATABASE________#

class AppDatabase(ssis.Tk):

    def __init__(self):
        ssis.Tk.__init__(self)
        self.config(bg="light gray")
        Table = ssis.Frame(self)
        Table.pack(side="top", fill="both", expand = True)
        Table.rowconfigure(0, weight=1)
        Table.columnconfigure(0, weight=1)
        self.frames = {}

        for i in (Home, Student, Course):
            frame = i(Table, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.ShowFrame(Home)

    def ShowFrame(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()
        

#________HOME________#
        
class Home(ssis.Frame):

    def __init__(self, parent, controller):
        ssis.Frame.__init__(self, parent)
        
        leftcolor = ssis.Label(self,height = 60,width=600, bg="light gray")
        leftcolor.place(x=0,y=0)
        label = ssis.Label(self, text="STUDENT INFORMATION SYSTEM", font=("Bebas 25 bold"), fg="#fff", bg="#a41d21", border=10, relief=ssis.GROOVE)
        label.place(x=0,y=0, width=1350)

        ttlstudents = StringVar() 
        totalcourses = StringVar()


#________HOME FUNCTIONS________#
        def Totalcourse():
            try:
                conn = sqlite3.connect("StudentDatabase.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM courses")
                rows = cur.fetchall()
                totalcourses.set(len(rows))
                self.totalenrolled = Label(self, font=("Bebas", 50),textvariable = totalcourses, bg = "gray", fg = "#fff")
                self.totalenrolled.place(x=820,y=427)
                self.after(1000,Totalcourse)
                conn.commit()            
                conn.close()
            except:
                pass
            
        def Totalstudents():
            try:
                conn = sqlite3.connect("StudentDatabase.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM studdatabase")
                rows = cur.fetchall()
                ttlstudents.set(len(rows))
                self.totalenrolled = Label(self, font=("Bebas", 50),textvariable = ttlstudents, bg = "gray", fg = "#fff")
                self.totalenrolled.place(x=820,y=157)
                self.after(1000,Totalstudents)
                conn.commit()            
                conn.close()
            except:
                pass
            

#________WINDOW BUTTONS________#
        
        Button1 =ssis.Button(self, text="COURSE",font=("Times New Roman",25),bd=7,width = 10,bg="Gray",command=lambda: controller.ShowFrame(Course))
        Button1.place(x=15,y=150)
        Button2 = ssis.Button(self, text="HOME",font=("Times New Roman",25),bd=7,width = 10,bg="Gray",command=lambda: controller.ShowFrame(Home))
        Button2.place(x=15,y=350)
        Button3 =ssis.Button(self, text="STUDENTS",font=("Times New Roman",25),bd=7, width = 10,bg="Gray",command=lambda: controller.ShowFrame(Student))
        Button3.place(x=15,y=550)

        self.totalstudents=Label(self, font=("Times New Roman",25,"bold"),height=5, width = 25, bd=7,text="TOTAL NO. OF STUDENTS",anchor=CENTER, bg="gray",fg="#fff", relief=ssis.RIDGE)
        self.totalstudents.place(x=600,y=150)
        
        self.totalcourse=Label(self, font=("Times New Roman", 25,"bold"),height=5, width = 25, bd=7, text="TOTAL NO. OF COURSE/S",anchor=CENTER, bg="gray",fg="#fff", relief=ssis.RIDGE)
        self.totalcourse.place(x=600,y=420)
        
    
        Totalcourse()
        Totalstudents()
        

#________COURSE FUNCTIONS________#

class Course(ssis.Frame):

    def __init__(self, parent, controller):
        ssis.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("COURSES")

        leftcolor = ssis.Label(self,height = 60,width=600, bg="Light Gray")
        leftcolor.place(x=0,y=0)
        frame = ssis.LabelFrame(self, height=100, width=400, bg="Gray", relief=ssis.GROOVE, bd=7)
        frame.place(x=15, y=120, width=530, height=450)
        label1 = ssis.Label(self, text="STUDENT INFORMATION SYSTEM", font=("Bebas 25 bold"), fg="#fff", bg="#a41d21", border=10, relief=ssis.GROOVE)
        label1.place(x=0,y=0, width=1350)
        label = ssis.Label(frame, text = "COURSES",bd=4, font=("Times New Roman",30,"bold"),bg="gray", fg="#fff")
        label.place(x=160,y=5)
        
        Course_Code = StringVar()
        Course_Name = StringVar()
        SearchBar_Var = StringVar()
        
        def connectCourse():
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses (Course_Code TEXT PRIMARY KEY, Course_Name TEXT)") 
            conn.commit() 
            conn.close()
            
        def addCourse():
            conn = sqlite3.connect("StudentDatabase.db")
            c = conn.cursor()                
            c.execute("INSERT INTO courses(Course_Code,Course_Name) VALUES (?,?)",\
                      (Course_Code.get(),Course_Name.get()))        
            conn.commit()           
            conn.close()
            Course_Code.set('')
            Course_Name.set('') 
            tkinter.messagebox.showinfo("STUDENT INFORMATION SYSTEM", "Successfully added!")
            displayCourse()
              
        def displayCourse():
            self.courselist.delete(*self.courselist.get_children())
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                self.courselist.insert("", ssis.END, text=row[0], values=row[0:])
            conn.close()
        
        def updateCourse():
            for selected in self.courselist.selection():
                conn = sqlite3.connect("StudentDatabase.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET Course_Code=?, Course_Name=? WHERE Course_Code=?", \
                            (Course_Code.get(),Course_Name.get(), self.courselist.set(selected, '#1')))    
                conn.commit()
                tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Successfully updated!")
                displayCourse()
                clear()
                conn.close()
                
        def editCourse():
            x = self.courselist.focus()
            if x == "":
                tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Please select a record.")
                return
            values = self.courselist.item(x, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
                    
        def deleteCourse(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("MSU-IIT STUDENT INFORMATION SYSTEM", "Deleting this record will remove it permanently. Are you okay with that?")
                if messageDelete > 0:   
                    con = sqlite3.connect("StudentDatabase.db")
                    cur = con.cursor()
                    x = self.courselist.selection()[0]
                    id_no = self.courselist.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE Course_Code = ?",(id_no,))                   
                    con.commit()
                    self.courselist.delete(x)
                    tkinter.messagebox.askyesno("MSU-IIT STUDENT INFORMATION SYSTEM", "Successfully deleted!")
                    displayCourse()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "This student's information has already been entered into the system")
                
        def searchCourse():
            Course_Code = SearchBar_Var.get()                
            con = sqlite3.connect("StudentDatabase.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE Course_Code = ?",(Course_Code,))
            con.commit()
            self.courselist.delete(*self.courselist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.courselist.insert("", ssis.END, text=row[0], values=row[0:])
            con.close()
 
        def Refresh():
            displayCourse()
        
        def clear():
            Course_Code.set('')
            Course_Name.set('') 
            
        def OnDoubleclick(event):
            item = self.courselist.selection()[0]
            values = self.courselist.item(item, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
            
#________WINDOW BUTTONS________#

        Button1 =ssis.Button(self, text="COURSE",font=("Times New Roman",25),bd=7,width = 10,bg="Gray",command=lambda: controller.ShowFrame(Course))
        Button1.place(x=300,y=600)
        Button2 = ssis.Button(self, text="HOME",font=("Times New Roman",25),bd=7,width = 10,bg="Gray",command=lambda: controller.ShowFrame(Home))
        Button2.place(x=560,y=600)
        Button3 =ssis.Button(self, text="STUDENTS",font=("Times New Roman",25),bd=7, width = 10,bg="Gray",command=lambda: controller.ShowFrame(Student))
        Button3.place(x=825,y=600)
        
#________LABELS AND ENTRIES________#
        
        self.lblCourseCode = Label(frame, font=("Times New Roman", 20), text="COURSE CODE:", padx=5, pady=5, bg = "gray", fg = "#fff")
        self.lblCourseCode.place(x=5,y=80)
        self.txtCourseCode = Entry(frame, font=("Time New Roman", 18), textvariable=Course_Code, width=12, fg = "black", bg = "#fff", relief=ssis.RIDGE, bd=3)
        self.txtCourseCode.place(x=210,y=83)

        self.lblCourseName = Label(frame, font=("Times New Roman", 20), text="COURSE NAME:", padx=5, pady=5, bg = "gray", fg = "#fff")
        self.lblCourseName.place(x=5,y=140)
        self.txtCourseName = Entry(self, font=("Time New Roman", 18), textvariable=Course_Name, width=20, fg = "black", bg = "#fff", relief=ssis.RIDGE, bd=3)
        self.txtCourseName.place(x=240,y=270)

        self.SearchBarlbl = Label(self, font=("Times New Roman", 16,"bold"), text="COURSE CODE:", padx=5, pady=5, bg = "light gray", fg = "Black")
        self.SearchBarlbl.place(x=600,y=125)
        self.SearchBar = Entry(self, font=("Time New Roman", 14), textvariable=SearchBar_Var,width=20, fg = "black", relief=ssis.GROOVE, bd=3)
        self.SearchBar.place(x=790,y=128)


#________TREEVIEW________#
        y_scrollbar = Scrollbar(self, orient=VERTICAL)
        y_scrollbar.place(x=1320,y=165,height=352)
        self.courselist = ttk.Treeview(self,columns=("Course Code","Course Name"),height = 16,  yscrollcommand=y_scrollbar.set)
        self.courselist.heading("Course Code", text="COURSE CODE")
        self.courselist.heading("Course Name", text="COURSE NAME")
        self.courselist['show'] = 'headings'
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("Treeview.Heading", font=("Times New Roman",15,"bold"),foreground="Black")
        style.configure("Treeview",font=("Times New Roman",15))
        style.map('Treeview', background=[('selected', 'grey')], foreground=[('selected', 'Black')])
        self.courselist.column("Course Code", width=290, anchor=W)
        self.courselist.column("Course Name", width=440)
        self.courselist.bind("<Double-1> ", OnDoubleclick)
        self.courselist.place(x=585,y=165)
        y_scrollbar.config(command=self.courselist.yview)
        
#________COURSE BUTTONS________#

        ButtonFrame=Frame(self, bd=4, bg="gray")
        ButtonFrame.place(x=30,y=350, width=500, height=170)
        
        self.btnAddID = Button(ButtonFrame, text="ADD", font=("Times New Roman", 20 ), height=1, width=12, bd=1,bg="light gray", fg="black",command=addCourse)
        self.btnAddID.place(x=35,y=15)
        self.btnUpdate = Button(ButtonFrame, text="UPDATE", font=("Times New Roman", 20), height=1, width=12, bd=1,bg="light gray", fg="black", command=updateCourse) 
        self.btnUpdate.place(x=275,y=15)
        self.btnClear = Button(ButtonFrame, text="CLEAR", font=("Times New Roman", 20), height=1, width=12, bd=1,bg="light gray", fg="black", command=clear)
        self.btnClear.place(x=35,y=90)
        self.btnDelete = Button(ButtonFrame, text="DELETE", font=("Times New Roman", 20), height=1, width=12, bd=1,bg="light gray", fg="black", command=deleteCourse)
        self.btnDelete.place(x=275,y=90)
        self.btnSearch = Button(self,text= "SEARCH",font=("Times New Roman", 14,"bold"), bg = "gray", fg = "black", command=searchCourse, width=11)
        self.btnSearch.place(x=1050,y=118)
        self.btnRefresh = Button(self, text="REFRESH", font=('Times New Roman', 14, "bold"), height=1, width=11, bg="gray", fg="Black", command=Refresh)
        self.btnRefresh.place(x=1184,y=118)
        
        connectCourse()
        displayCourse()
        
#_______STUDENT FUNCTION________#

class Student(ssis.Frame):

    def __init__(self, parent, controller):
        ssis.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("STUDENT INFORMATION")

        leftcolor = ssis.Label(self,height = 60,width=600, bg="light gray")
        leftcolor.place(x=0,y=0)
        label1 = ssis.Label(self, text="STUDENT INFORMATION SYSTEM", font=("Bebas 25 bold"), fg="#fff", bg="#a41d21", border=10, relief=ssis.GROOVE)
        label1.place(x=0,y=0, width=1350)
        frame = ssis.LabelFrame(self, height=100, width=400, bg="Gray", relief=ssis.GROOVE, bd=7)
        frame.place(x=15, y=120, width=530, height=450)
        label = ssis.Label(self, text = "STUDENT INFORMATION",bd=4, font=("Times New Roman",25,"bold"),bg="light gray", fg="black")
        label.place(x=65,y=72)

        Student_ID = StringVar()
        Student_Name = StringVar()       
        Student_YearLevel = StringVar()
        Student_Gender = StringVar()
        Course_Code = StringVar()
        SearchBar_Var = StringVar()

        def connect():
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS studdatabase (Student_ID TEXT PRIMARY KEY, Student_Name TEXT, Course_Code TEXT, \
                      Student_YearLevel TEXT, Student_Gender TEXT, \
                      FOREIGN KEY(Course_Code) REFERENCES courses(Course_Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def addData():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Completely fill the fields")
            else:  
                ID = Student_ID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "The ID number is not valid, please check and try again.")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "The ID number is not valid, please check and try again.")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("StudentDatabase.db")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO studdatabase(Student_ID,Student_Name,Course_Code,Student_YearLevel,Student_Gender) VALUES (?,?,?,?,?)",\
                                                          (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get()))                                       
                                                                       
                                    tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Successfully added!")
                                    conn.commit() 
                                    clear()
                                    displayData()
                                    conn.close()
                                except:
                                    ids=[]
                                    conn = sqlite3.connect("StudentDatabase.db")
                                    c = conn.cursor()
                                    c.execute("SELECT * FROM studdatabase")
                                    rows = c.fetchall()
                                    for row in rows:
                                        ids.append(row[0])
                                    print(ids)
                                    if ID in ids:
                                       tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "This ID already exist")
                                    else: 
                                       tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Course Unavailable")
                                   
                    else:
                        tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")
                else:
                    tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")
                 
        def updateData():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Select a student")
            else:
                for selected in self.studentlist.selection():
                    conn = sqlite3.connect("StudentDatabase.db")
                    cur = conn.cursor()
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("UPDATE studdatabase SET Student_ID=?, Student_Name=?, Course_Code=?, Student_YearLevel=?,Student_Gender=?\
                          WHERE Student_ID=?", (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get(),\
                              self.studentlist.set(selected, '#1')))
                    conn.commit()
                    tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Successfully Updated!")
                    displayData()
                    clear()
                    conn.close()
        
        def deleteData():   
            try:
                messageDelete = tkinter.messagebox.askyesno("MSU-IIT STUDENT INFORMATION SYSTEM", "Are you sure you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("StudentDatabase.db")
                    cur = con.cursor()
                    x = self.studentlist.selection()[0]
                    id_no = self.studentlist.item(x)["values"][0]
                    cur.execute("DELETE FROM studdatabase WHERE Student_ID = ?",(id_no,))                   
                    con.commit()
                    self.studentlist.delete(x)
                    tkinter.messagebox.showinfo("MSU-IIT STUDENT INFORMATION SYSTEM", "Successfully Deleted!")
                    displayData()
                    clear()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def searchData():
            Student_ID = SearchBar_Var.get()
            try:  
                con = sqlite3.connect("StudentDatabase.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM studdatabase")
                con.commit()
                self.studentlist.delete(*self.studentlist.get_children())
                rows = cur.fetchall()
                for row in rows:
                    if row[0].startswith(Student_ID):
                        self.studentlist.insert("", ssis.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Invalid ID Number")           
                
        def displayData():
            self.studentlist.delete(*self.studentlist.get_children())
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM studdatabase")
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", ssis.END, text=row[0], values=row[0:])
            conn.close()
                            
        def editData():
            x = self.studentlist.focus()
            if x == "":
                tkinter.messagebox.showerror("MSU-IIT STUDENT INFORMATION SYSTEM", "Please Select a record.")
                return
            values = self.studentlist.item(x, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
            
        def Refresh():
            displayData()
        
        def clear():
            Student_ID.set('')
            Student_Name.set('') 
            Student_YearLevel.set('')
            Student_Gender.set('')
            Course_Code.set('')
            
        def OnDoubleClick(event):
            item = self.studentlist.selection()[0]
            values = self.studentlist.item(item, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])


#________WINDOWS BUTTON________#
        
        Button1 =ssis.Button(self, text="COURSE",font=("Times New Roman",25),bd=7,width = 10,bg="Gray",command=lambda: controller.ShowFrame(Course))
        Button1.place(x=300,y=600)
        Button2 = ssis.Button(self, text="HOME",font=("Times New Roman",25),bd=7,width = 10,bg="Gray",command=lambda: controller.ShowFrame(Home))
        Button2.place(x=560,y=600)
        Button3 =ssis.Button(self, text="STUDENTS",font=("Times New Roman",25),bd=7, width = 10,bg="Gray",command=lambda: controller.ShowFrame(Student))
        Button3.place(x=825,y=600)

#_______LABELS AND ENTRIES_______#

        self.lblStudentID = Label(frame, font=("Times New Roman", 16,"bold"), text="ID NO:", padx=5, pady=5, bg = "gray", fg = "WHITE", width = 10)
        self.lblStudentID.place(x=10,y=20)

        self.txtStudentID = Entry(frame, font=("Times New Roman", 16), textvariable=Student_ID, width=26, fg = "BLACK")
        self.txtStudentID.place(x=160,y=25)
        self.txtStudentID.insert(0,'YYYY-NNNN')

        self.lblStudentName = Label(frame, font=("Times New Roman", 15,"bold"), text="FULL NAME:", padx=5, pady=5, bg = "gray", fg = "white",  width = 10)
        self.lblStudentName.place(x=10,y=75)
        self.txtStudentName = Entry(frame, font=("Times New Roman", 16), textvariable=Student_Name, width=26, fg = "BLACK")
        self.txtStudentName.place(x=160,y=80)

        self.lblStudentCourse = Label(frame, font=("Times New Roman", 16,"bold"), text="COURSE:", padx=5, pady=5, bg = "gray", fg = "white",  width = 10)
        self.lblStudentCourse.place(x=10,y=145)
        self.txtStudentCourse = Entry(frame, font=("Times New Roman", 16), textvariable=Course_Code, width=26, fg = "black")
        self.txtStudentCourse.place(x=160,y=150)

        self.lblStudentYearLevel = Label(frame, font=("Times New Roman", 15,"bold"), text="YEAR LEVEL:", padx=5, pady=5, bg = "gray", fg = "white",  width = 10)
        self.lblStudentYearLevel.place(x=10,y=215)
        ttk.Style().layout('combostyleO.TCombobox')
        ttk.Style().configure('combostyleO.TCombobox', selectforeground='black', selectbackground='white',  foreground='black')
        self.txtStudentYearLevel = ttk.Combobox(frame,value=["First Year", "Second Year", "Third Year", "Fourth Year"],state="readonly", font=("Times new roman", 16), textvariable=Student_YearLevel,width=10, style="combostyleO.TCombobox")
        self.txtStudentYearLevel.place(x=160,y=220)
        
        self.lblStudentGender = Label(frame, font=("Times New Roman", 15,"bold"), text="GENDER:", padx=5, pady=5, bg = "gray", fg = "white",  width = 10)
        self.lblStudentGender.place(x=10,y=285)
        self.txtStudentGender = ttk.Combobox(frame, value=["Male", "Female"], font=("Palatino roman", 16),state="readonly", textvariable=Student_Gender, width=9, style="combostyleO.TCombobox")
        self.txtStudentGender.place(x=160,y=290)

        self.SearchBarlbl = Label(self, font=("Time new roman", 16,"bold"), text="ID Number:", padx=2, pady=2, bg = "light gray", fg = "black")
        self.SearchBarlbl.place(x=610,y=120)        
        self.SearchBar = Entry(self, font=("Times new roman", 15), textvariable=SearchBar_Var,width=23, fg = "black", relief=GROOVE, bd=3)
        self.SearchBar.place(x=735,y=122)

#______TREE VIEW_______#
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1286,y=160,height=411)
        x_scrollbar = Scrollbar(self, orient=HORIZONTAL)
        x_scrollbar.place(x=600, y= 570, width=685)
        self.studentlist = ttk.Treeview(self,columns=("ID Number", "Name", "Gender", "Year Level", "Course"),height = 19,yscrollcommand=scrollbar.set, xscrollcommand=x_scrollbar.set)
        self.studentlist.heading("ID Number", text="ID Number", anchor=CENTER)
        self.studentlist.heading("Name", text="Name",anchor=CENTER)
        self.studentlist.heading("Gender", text="Course",anchor=CENTER)
        self.studentlist.heading("Year Level", text="Year Level",anchor=CENTER)
        self.studentlist.heading("Course", text="Gender",anchor=CENTER)
        self.studentlist['show'] = 'headings'
        self.studentlist.column("ID Number", width=150, anchor=CENTER)
        self.studentlist.column("Name", width=350, anchor=CENTER)
        self.studentlist.column("Course", width=120, anchor=CENTER)
        self.studentlist.column("Year Level", width=150, anchor=CENTER)
        self.studentlist.column("Gender", width=120, anchor=CENTER)
        self.studentlist.bind("<Double-1>",OnDoubleClick)
        self.studentlist.place(x=600,y=160,width=685)
        scrollbar.config(command=self.studentlist.yview)
        x_scrollbar.config(command=self.studentlist.xview)
        
#________STUDENT BUTTONS______#

        ButtonFrame=Frame(frame, bd=4, bg="gray")
        ButtonFrame.place(x=0,y=350, width=515, height=75)

        self.btnAddID = Button(ButtonFrame, text="ADD", font=('Times New Roman', 15, "bold" ), height=1, width=7, bd=1,bg="light gray", fg="Black",command=addData)
        self.btnAddID.place(x=12,y= 10)
        self.btnUpdate = Button(ButtonFrame, text="UPDATE", font=('Times New Roman', 15, "bold"), height=1, width=7, bd=1,bg="light gray", fg="Black", command=updateData) 
        self.btnUpdate.place(x=269,y=10)
        self.btnClear = Button(ButtonFrame, text="CLEAR", font=('Times New Roman', 15, "bold"), height=1, width=7, bd=1,bg="light gray", fg="Black", command=clear)
        self.btnClear.place(x=138,y=10)
        self.btnDelete = Button(ButtonFrame, text="DELETE", font=('Times New Roman', 15, "bold"), height=1, width=7, bd=1,bg="light gray", fg="Black", command=deleteData)
        self.btnDelete.place(x=398,y=10)
        self.btnSearch = Button(self,text= "SEARCH",font=("Times New Roman", 14,"bold"), height=1, width=11, bg = "gray", fg = "Black", command=searchData)
        self.btnSearch.place(x=1000,y=115)
        self.btnRefresh = Button(self, text="REFRESH", font=('Times New Roman', 14, "bold"), height=1, width=11, bg="gray", fg="Black", command=Refresh)
        self.btnRefresh.place(x=1150,y=115)
        
        connect()
        displayData()
        
app = AppDatabase()
app.geometry("1350x700+0+0")
app.title("Student Information System")
app.mainloop()