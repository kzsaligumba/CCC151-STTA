from tkinter import *
import tkinter as brms
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta, date
import sqlite3

class Application(brms.Tk):
    def __init__(self):
        brms.Tk.__init__(self)
        # Create a container to hold all the frames
        Table = brms.Frame(self)
        Table.pack(side="top", fill="both", expand=True)
        Table.rowconfigure(0, weight=1)
        Table.columnconfigure(0, weight=1)
        
        # Create a dictionary to store the frames
        self.frames = {}

        # Create and add frames to the dictionary
        for i in (HomePage, BooksPage, BorrowersPage, RentsPage, ReservationsPage):
            frame = i(Table, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the home page initially
        self.show_frame(HomePage)

    def show_frame(self, page):
        # Show the specified frame
        frame = self.frames[page]
        frame.tkraise()
        
class HomePage(brms.Frame):
    def __init__(self, parent, controller):
        brms.Frame.__init__(self, parent)
        
        label = brms.Label(self, text="BOOK RENTAL AND RESERVATION MANAGEMENT SYSTEM", font=("Bebas 25 bold"), fg="#fff", bg="royalblue4", border=10, relief=brms.GROOVE)
        label.place(x=0,y=0, width=1358)

        button1 = brms.Button(self, text="BOOKS",font=("Times New Roman",25),bd=7,width = 10, bg="royalblue4", fg="white", command=lambda: controller.show_frame(BooksPage))
        button1.place(x=380, y=250, width=260, height=100)

        button2 = brms.Button(self, text="BORROWERS",font=("Times New Roman",25),bd=7,width = 10, bg="royalblue4", fg="white", command=lambda: controller.show_frame(BorrowersPage))
        button2.place(x=710, y=250, width=260, height=100)
        
        button3 = brms.Button(self, text="RENTS",font=("Times New Roman",25),bd=7,width = 10, bg="royalblue4", fg="white",  command=lambda: controller.show_frame(RentsPage))
        button3.place(x=380, y=430, width=260, height=100)

        button4 = brms.Button(self, text="RESERVATIONS",font=("Times New Roman",25),bd=7,width = 10, bg="royalblue4", fg="white", command=lambda: controller.show_frame(ReservationsPage))
        button4.place(x=710, y= 430, width=260, height=100)
        
class BooksPage(brms.Frame):
    def __init__(self, parent, controller):
        brms.Frame.__init__(self, parent)
        self.controller = controller
        self.books = []
        label = brms.Label(self, text="BOOK INFORMATION", font=("Bebas 25 bold"), fg="#fff", bg="royalblue4", border=10, relief=brms.GROOVE)
        label.place(x=0,y=0, width=1358)
        frame = brms.LabelFrame(self, height=100, width=400, bg="royalblue4", relief=brms.GROOVE, bd=5)
        frame.place(x=15, y=75, width=1328, height=580)
        
        # Establish connection to SQLite database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()
        
        # Create the 'books' table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books(
                bookno INT PRIMARY KEY ON CONFLICT IGNORE,
                status VARCHAR(9), 
                title VARCHAR(255), 
                author VARCHAR(255), 
                genre VARCHAR(255), 
                isbn VARCHAR(255),  
                price INT)
        ''')

        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON") 
    
        ## BOOK TREEVIEW ##
        y_scrollbar = Scrollbar(frame, orient=VERTICAL)
        y_scrollbar.place(x=1295,y=70,height=492)
        x_scrollbar = Scrollbar(frame, orient=HORIZONTAL)
        x_scrollbar.place(x=5, y=545,width=1290)
        self.booklist = ttk.Treeview(frame,columns=("BookNo", "Status", "Book Title", "Author", "Genre", "ISBN", "Price"),height = 16, 
                                     yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        self.booklist.heading("BookNo", text="BOOKNO")
        self.booklist.heading("Status", text="STATUS")
        self.booklist.heading("Book Title", text="BOOK TITLE")
        self.booklist.heading("Author", text="AUTHOR")
        self.booklist.heading("Genre", text="GENRE")
        self.booklist.heading("ISBN", text="ISBN")
        self.booklist.heading("Price", text="PRICE")
        self.booklist['show'] = 'headings'
        self.booklist.place(x=5,y=70, width=1290, height=475)
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("Treeview.Heading", font=("Times New Roman",12,"bold"),foreground="Black")
        style.configure("Treeview",font=("Times New Roman",11))
        style.map('Treeview', background=[('selected', 'grey')], foreground=[('selected', 'Black')])
        self.booklist.column("BookNo", width=150, anchor="center")
        self.booklist.column("Status", width=150, anchor="center") 
        self.booklist.column("Book Title", width=350, anchor="center")
        self.booklist.column("Author", width=300, anchor="center")
        self.booklist.column("Genre", width=150, anchor="center")
        self.booklist.column("ISBN", width=200, anchor="center")
        self.booklist.column("Price", width=150, anchor="center")
        y_scrollbar.config(command=self.booklist.yview)
        x_scrollbar.config(command=self.booklist.xview) 
        
        #TREEVIEW BUTTONS#
        searchlabel = Label(frame, text="SEARCH",font=("Times New Roman",15), bg="royalblue4", fg="white")
        searchlabel.place(x=30, y=30)
        self.searchentry = Entry(frame,font=("Times New Roman",12), width=55, relief=RIDGE)
        self.searchentry.place(x=130, y=33)
        searchbutton = brms.Button(frame, text="SEARCH", font=("Times New Roman",12),bd=2,width = 10, command=self.search_books)
        searchbutton.place(x=590, y=28)
        
        addbutton = brms.Button(frame, text="ADD", font=("Times New Roman",12),bd=2,width = 13, command=self.open_add_window)
        addbutton.place(x=870,y=28)
        updatebutton = brms.Button(frame, text="UPDATE", font=("Times New Roman",12),bd=2,width = 13, command=self.open_update_window)
        updatebutton.place(x=1010, y=28)
        deletebutton = brms.Button(frame, text="DELETE", font=("Times New Roman", 12), bd=2, width=13, command=self.delete_book)
        deletebutton.place(x=1150, y=28)
        listbutton = brms.Button(frame, text="LIST ALL", font=("Times New Roman", 12), bd=2, width=10,
                                 command=self.list_all_books)
        listbutton.place(x=710, y=28)
        #WIDGET BUTTONS#
        buttonframe = brms.LabelFrame(self,bg="royalblue4", relief=brms.GROOVE, bd=5)
        buttonframe.place(x=360, y=670, width=650, height=50)
        
        button0 = brms.Button(buttonframe, text="HOME", font=("Times New Roman",12),bd=2,width = 14, command=lambda: controller.show_frame(HomePage))
        button0.place(x=20, y=4)
        button2 = brms.Button(buttonframe, text="BORROWERS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(BorrowersPage))
        button2.place(x=175, y=4)
        button3 = brms.Button(buttonframe, text="RENTS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(RentsPage))
        button3.place(x=330, y=4)
        button4 = brms.Button(buttonframe, text="RESERVATIONS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(ReservationsPage))
        button4.place(x=485, y=4)
        
    def open_add_window(self):
        add_window = brms.Toplevel(self)
        add_window.title("Add Book")
        # Configure the window size and position according to your requirements
        add_window.geometry("550x300+400+300")
        # Example: Add a label and an entry widget for book title
        label = brms.Label(add_window, text="ADD BOOKS", font=("Bebas 12 bold"), fg="#fff", bg="royalblue4", border=5, relief=GROOVE)
        label.pack(side=TOP, fill=X)
        frame=brms.Frame(add_window, bg="gray", relief=RIDGE, bd=5)
        frame.place(x=5, y=40, height=250, width=538)
        #ENTRIES AND LABELS 
        self.bookno = brms.Label(frame, text="BOOK NO", font=("Times New Roman", 12, 'bold'), bg="gray", fg="white", width=10)
        self.bookno.place(x=10, y=10)
        self.bookno_en = brms.Entry(frame, font=("Times New Roman", 11), width=20, relief=RIDGE, bd=2)
        self.bookno_en.place(x=110, y=10)
        
        self.status = brms.Label(frame, text="STATUS", font=("Times New Roman", 12, 'bold'), bg="gray", fg="white", width=10)
        self.status.place(x=260, y=10)
        self.status_en = brms.Entry(frame, font=("Times New Roman", 11), width=20, relief=RIDGE, bd=2)
        self.status_en.insert(0, "Available")
        self.status_en.place(x=360, y=10)
        
        self.title = brms.Label(frame, text="TITLE", font=("Times New Roman", 12, "bold"), bg="gray", fg="white")
        self.title.place(x=30, y=50)
        self.title_en = brms.Entry(frame, font=("Times New Roman", 11), width=56, relief=RIDGE, bd=2)
        self.title_en.place(x=110, y=50)
        
        self.author = brms.Label(frame, text="AUTHOR", font=("Times New Roman", 12, 'bold'), bg="gray", fg='white')
        self.author.place(x=20, y=90)
        self.author_en = brms.Entry(frame, font=("Times New Roman", 11), width=56, relief=RIDGE, bd=2)
        self.author_en.place(x=110, y=90)
        
        self.genrelab = brms.Label(frame, text="GENRE", font=("Times New Roman", 12, 'bold'), bg="gray", fg='white')
        self.genrelab.place(x=25, y=130)
        self.genre_en = brms.Entry(frame, font=("Times New Roman", 11), width=20, relief=RIDGE, bd=2)
        self.genre_en.place(x=110, y=130)
        
        self.isbn = brms.Label(frame, text="ISBN", font=("Times New Roman", 12, 'bold'), bg="gray", fg='white')
        self.isbn.place(x=30, y=170)
        self.isbn_en = brms.Entry(frame, font=("Times New Roman", 11), width=35, relief=RIDGE, bd=2)
        self.isbn_en.place(x=110, y=170)
        
        self.price = brms.Label(frame, text="PRICE", font=("Times New Roman", 12, 'bold'), bg="gray", fg="white", width=10)
        self.price.place(x=260, y=130)
        self.price_en = brms.Entry(frame, font=("Times New Roman", 11), width=20, relief=RIDGE, bd=2)
        self.price_en.place(x=360, y=130)
        # Example: Add a button 
        addbut = brms.Button(frame, text="ADD", width=10, command=lambda: self.add_book(add_window))
        addbut.place(x=170, y=210)
        close_button = brms.Button(frame, text="CANCEL",width=10, command=add_window.destroy)
        close_button.place(x=280, y=210)
        
    #Adding of books
    def add_book(self, add_window):
        book_no = self.bookno_en.get()
        status = self.status_en.get()
        title = self.title_en.get()
        author = self.author_en.get()
        genre = self.genre_en.get()
        isbn = self.isbn_en.get()
        price = self.price_en.get()

        # Establish a connection to the SQLite database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()

        # Check if the book number already exists in the database
        cursor.execute("SELECT * FROM books WHERE bookno = ?", (book_no,))
        if cursor.fetchone() is not None:
            messagebox.showerror("Error", "Book number already exists")
            connection.close()
            return

        # Check if the status is one of the allowed values
        if status not in ["Available", "Rented", "Reserved"]:
            messagebox.showerror("Error", "Invalid status. Please enter either 'Available', 'Rented', or 'Reserved'")
            connection.close()
            return

        # Insert the book information into the database
        cursor.execute("INSERT INTO books (bookno, status, title, author, genre, isbn, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (book_no, status, title, author, genre, isbn, price))
        connection.commit()

        # Insert the book information into the treeview
        self.booklist.insert("", "end", values=(book_no, status, title, author, genre, isbn, price))

        # Show success message
        messagebox.showinfo("Success", "Book has been successfully added")

        # Close the database connection
        cursor.close()
        connection.close()

        # Close the add window
        add_window.destroy()
        
    def open_update_window(self):
        selected_item = self.booklist.focus()
        if selected_item:
            item_values = self.booklist.item(selected_item, "values")  # Get the values of the selected item
            update_window = brms.Toplevel(self)
            update_window.title("Update Book")
            # Configure the window size and position according to your requirements
            update_window.geometry("550x300+400+300")
            # Example: Add a label and an entry widget for book title
            label = brms.Label(update_window, text="UPDATE BOOK", font=("Bebas 12 bold"), fg="#fff", bg="royalblue4", border=5, relief=GROOVE)
            label.pack(side=TOP, fill=X)
            frame = brms.Frame(update_window, bg="gray", relief=RIDGE, bd=5)
            frame.place(x=5, y=40, height=250, width=538)
            #ENTRIES AND LABELS
            self.bookno = brms.Label(frame, text="BOOK NO", font=("Times New Roman", 12, 'bold'), bg="gray", fg="white", width=10)
            self.bookno.place(x=10, y=10)
            self.bookno_en = brms.Entry(frame, font=("Times New Roman", 11), width=20, relief=RIDGE, bd=2)
            self.bookno_en.place(x=110, y=10)
            self.bookno_en.insert(0, item_values[0])
            self.bookno_en.configure(state="disabled")

            self.status = brms.Label(frame, text="STATUS", font=("Times New Roman", 12, 'bold'), bg="gray", fg="white", width=10)
            self.status.place(x=260, y=10)
            self.status_en = brms.Entry(frame, font=("Times New Roman", 11), width=20, relief=RIDGE, bd=2)
            self.status_en.place(x=360, y=10)
            self.status_en.insert(0, item_values[1])

            self.title = brms.Label(frame, text="TITLE", font=("Times New Roman", 12, "bold"), bg="gray", fg="white")
            self.title.place(x=30, y=50)
            self.title_en = brms.Entry(frame, font=("Times New Roman", 11), width=56, relief=RIDGE, bd=2)
            self.title_en.place(x=110, y=50)
            self.title_en.insert(0, item_values[2])

            self.author = brms.Label(frame, text="AUTHOR", font=("Times New Roman", 12, 'bold'), bg="gray", fg='white')
            self.author.place(x=20, y=90)
            self.author_en = brms.Entry(frame, font=("Times New Roman", 11), width=56, relief=RIDGE, bd=2)
            self.author_en.place(x=110, y=90)
            self.author_en.insert(0, item_values[3])

            self.genrelab = brms.Label(frame, text="GENRE", font=("Times New Roman", 12, 'bold'), bg="gray", fg='white')
            self.genrelab.place(x=25, y=130)
            self.genre_en = brms.Entry(frame, font=("Times New Roman", 11), width=20, relief=RIDGE, bd=2)
            self.genre_en.place(x=110, y=130)
            self.genre_en.insert(0, item_values[4])

            self.isbn = brms.Label(frame, text="ISBN", font=("Times New Roman", 12, 'bold'), bg="gray", fg='white')
            self.isbn.place(x=30, y=170)
            self.isbn_en = brms.Entry(frame, font=("Times New Roman", 11), width=35, relief=RIDGE, bd=2)
            self.isbn_en.place(x=110, y=170)
            self.isbn_en.insert(0, item_values[5])

            self.price = brms.Label(frame, text="PRICE", font=("Times New Roman", 12, 'bold'), bg="gray", fg="white", width=10)
            self.price.place(x=260, y=130)
            self.price_en = brms.Entry(frame, font=("Times New Roman", 11), width=20, relief=RIDGE, bd=2)
            self.price_en.place(x=360, y=130)
            self.price_en.insert(0, item_values[6])

            
        # Example: Add a button
        update_button = brms.Button(frame, text="UPDATE", width=10, command=lambda: self.update_book(selected_item, update_window))
        update_button.place(x=170, y=210)
        close_button = brms.Button(frame, text="CANCEL", width=10, command=update_window.destroy)
        close_button.place(x=280, y=210)
        
    #Updating book
    def update_book(self, selected_item, update_window):
        # Check if the selected_item is in the booklist
        if selected_item not in self.booklist.get_children():
            messagebox.showerror("Error", "Selected book not found in the list.")
            return

        # Get the index of the selected item
        index = self.booklist.index(selected_item)

        # Retrieve the updated values from the entry widgets
        book_no = self.bookno_en.get()
        title = self.title_en.get()
        author = self.author_en.get()
        genre = self.genre_en.get()
        isbn = self.isbn_en.get()
        price = self.price_en.get()

        # Retrieve the current status from the selected item
        current_status = self.booklist.item(selected_item, "values")[1]
        
       # Update the corresponding record in the database with the current status
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE books SET bookno=?, status=?, title=?, author=?, genre=?, isbn=?, price=? WHERE bookno=?",
            (book_no, current_status, title, author, genre, isbn, price, book_no)
        )
        connection.commit()
        connection.close()
        
        # Clear the booklist widget
        self.booklist.delete(*self.booklist.get_children())
        
        # Fetch the updated book records from the database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books")
        updated_books = cursor.fetchall()
        connection.close()
        
        # Populate the booklist widget with the updated book records
        for book in updated_books:
            self.booklist.insert("", "end", values=book)

        # Show success message
        messagebox.showinfo("Success", "Book has been successfully updated")
        
        # Close the update window
        update_window.destroy()
        
    def delete_book(self):
        selected_item = self.booklist.focus()
        if selected_item:
            book_no = self.booklist.item(selected_item, "values")[0]  # Get the book number of the selected item

            # Ask for confirmation before deleting the book
            confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to delete the book?")
            if not confirmed:
                return

            self.booklist.delete(selected_item)  # Delete the selected item from the treeview

            # Delete the corresponding book entries in the RentsPage treeview
            rents_page = self.controller.frames[RentsPage]  # Get the instance of RentsPage
            rents_items = rents_page.rentlist.get_children()  # Get all items in the RentsPage treeview
            for item in rents_items:
                if rents_page.rentlist.item(item, "values")[0] == book_no:  # Check if the book number matches
                    rents_page.rentlist.delete(item)  # Delete the item from the RentsPage treeview

            # Delete the book entry from the books list
            for book in self.books:
                if book['BookNo'] == book_no:
                    self.books.remove(book)
                    break  # Exit the loop after deleting the book entry

            # Establish connection to the SQLite database
            connection = sqlite3.connect("brms.db")
            cursor = connection.cursor() 

            # Delete the book entry from the database
            cursor.execute("DELETE FROM books WHERE bookno = ?", (book_no,))
            connection.commit()

            # Close the database connection
            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Book has been successfully deleted")
            
    def search_books(self):
        query = self.searchentry.get().lower()  # Get the search query from the entry widget

        # Clear existing items from the treeview
        self.booklist.delete(*self.booklist.get_children())

        try:
            # Establish connection to the SQLite database
            connection = sqlite3.connect("brms.db")
            cursor = connection.cursor()
            # Execute the SQL query to search for books matching the query
            cursor.execute("SELECT * FROM books WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ?",
                        ('%' + query + '%', '%' + query + '%'))
            found_books = cursor.fetchall()

            # Iterate over the found books and insert them into the treeview
            for book in found_books:
                self.booklist.insert("", "end", values=book)

            # Check if no books were found and show a message box
            if not found_books:
                messagebox.showinfo("Book Not Found", "No books matching the search query were found.")

        except sqlite3.Error as error:
            print("Error searching books:", error)

        finally:
            # Close the database connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        # Clear the search entry field
        self.searchentry.delete(0, 'end')
        
    def list_all_books(self):
        # Clear existing items from the treeview
        self.booklist.delete(*self.booklist.get_children())

        try:
            # Establish connection to the SQLite database
            connection = sqlite3.connect("brms.db")
            cursor = connection.cursor()

            # Execute the SQL query to fetch all books
            cursor.execute("SELECT * FROM books")
            all_books = cursor.fetchall()

            # Iterate over all books and insert them into the treeview
            for book in all_books:
                self.booklist.insert("", "end", values=book)

        except sqlite3.Error as error:
            print("Error fetching books:", error)

        finally:
            # Close the database connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                
class RentsPage(brms.Frame):
    def __init__(self, parent, controller):
        brms.Frame.__init__(self, parent)
        self.controller = controller
        self.books_page = controller.frames[BooksPage]
        self.borrowers_page = controller.frames[BorrowersPage]
        label = brms.Label(self, text="RENTED BOOKS", font=("Bebas 25 bold"), fg="#fff", bg="royalblue4", border=10, relief=brms.GROOVE)
        label.place(x=0,y=0, width=1358)
        frame = brms.LabelFrame(self, height=100, width=400, bg="royalblue4", relief=brms.GROOVE, bd=5)
        frame.place(x=15, y=75, width=1328, height=580)
        frame1 = brms.Label(frame, text="BORROWER INFO",font=("Bebas 25 bold"), fg="#fff", bg="royalblue4", border=7, relief=brms.GROOVE )
        frame1.place(x=45, y=25, width=360)
        
        # Establish connection to SQLite database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()
        
        # Create the 'rents' table if it doesn't exist
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS rents(
                        bookno INT REFERENCES books(bookno) ON DELETE CASCADE,
                        borrowerNo INT REFERENCES borrower(borrowerNo) ON DELETE CASCADE,
                        startDate VARCHAR(255), 
                        dueDate VARCHAR(255),
                        returnDate VARCHAR(255), 
                        fines INT)
                    ''')
        
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON") 
        
        #Labels and Entries#
        borrowernolabel = Label(frame,text="BORROWER NO",font=("Times New Roman",12), bg="royalblue4", fg="white")
        borrowernolabel.place(x=5,y=123)
        self.borrowernoentry = Entry(frame,font=("Times New Roman",12), width=20, relief=RIDGE, bd=2)
        self.borrowernoentry.place(x=130, y=122)
        namelabel = Label(frame, text="NAME",font=("Times New Roman",12), bg="royalblue4", fg="white", width=12)
        namelabel.place(x=5, y=158)
        self.nameentry = Entry(frame,font=("Times New Roman",12), width=40, relief=RIDGE, bd=2)
        self.nameentry.place(x=130, y=157)
        addresslabel = Label(frame, text="ADDRESS",font=("Times New Roman",12), bg="royalblue4", fg="white", width=12)
        addresslabel.place(x=5, y=193)
        self.addressentry = Entry(frame,font=("Times New Roman",12), width=40, relief=RIDGE, bd=2)
        self.addressentry.place(x=130, y=192)
        phonelabel = Label(frame, text="PHONE NO",font=("Times New Roman",12), bg="royalblue4", fg="white", width=12)
        phonelabel.place(x=5, y=228)
        self.phoneentry = Entry(frame,font=("Times New Roman",12), width=40, relief=RIDGE, bd=2)
        self.phoneentry.place(x=130, y=227)
        validid = Label(frame, text="VALID ID",font=("Times New Roman",12), bg="royalblue4", fg="white", width=12)
        validid.place(x=5, y=263)
        self.validentry = Entry(frame,font=("Times New Roman",12), width=20, relief=RIDGE, bd=2)
        self.validentry.place(x=130, y=262)
        
        bookno = Label(frame, text="BOOK NO",font=("Times New Roman",12), bg="royalblue4", fg="white", width=12)
        bookno.place(x=5, y=325)
        self.bookno_en = Entry(frame,font=("Times New Roman",12), width=20, relief=RIDGE, bd=2)
        self.bookno_en.place(x=130, y=324)
        
        #Date Entries#
        start_label = Label(frame, text="START DATE", font=("Times New Roman",12), bg="royalblue4", fg="white", width=12 )
        start_label.place(x=5, y=360)
        self.start_date_entry = Entry(frame,font=("Times New Roman",12), width=20, relief=RIDGE, bd=2)
        self.start_date_entry.place(x=130, y=359)
        due_label = Label(frame, text="DUE DATE", font=("Times New Roman",12), bg="royalblue4", fg="white", width=12 )
        due_label.place(x=5, y=395)
        self.due_date_entry = Entry(frame,font=("Times New Roman",12), width=20, relief=RIDGE, bd=2)
        self.due_date_entry.place(x=130, y=394)
        current_date = datetime.today().date()
        due_date = current_date + timedelta(days=7)
        self.start_date_entry.insert(0, current_date)
        self.due_date_entry.insert(0, due_date)
        
        #TREEVIEW#
        y_scrollbar = Scrollbar(frame, orient=VERTICAL)
        y_scrollbar.place(x=1290,y=30,height=522)
        x_scrollbar = Scrollbar(frame, orient=HORIZONTAL)
        x_scrollbar.place(x=500, y=535,width=790)
        self.rentlist = ttk.Treeview(frame,columns=("BookNo", "BorrowerNo", "Start Date", "Due Date", "Return Date", "Fines"),height = 16, 
                                     yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        self.rentlist.heading("BookNo", text="BOOKNO")
        self.rentlist.heading("BorrowerNo", text="BORROWERNO")
        self.rentlist.heading("Start Date", text="START DATE")
        self.rentlist.heading("Due Date", text="DUE DATE")
        self.rentlist.heading("Return Date", text="RETURN DATE")
        self.rentlist.heading("Fines", text="FINES")
        self.rentlist['show'] = 'headings'
        self.rentlist.place(x=500,y=30, width=790, height=505)
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("Treeview.Heading", font=("Times New Roman",12,"bold"),foreground="Black")
        style.configure("Treeview",font=("Times New Roman",11))
        style.map('Treeview', background=[('selected', 'grey')], foreground=[('selected', 'Black')])
        self.rentlist.column("BookNo", width=150, anchor="center")
        self.rentlist.column("BorrowerNo", width=150, anchor="center")
        self.rentlist.column("Start Date", width=150, anchor="center")
        self.rentlist.column("Due Date", width=150, anchor="center")
        self.rentlist.column("Return Date", width=150, anchor="center")
        self.rentlist.column("Fines", width=150, anchor="center")
        y_scrollbar.config(command=self.rentlist.yview)
        x_scrollbar.config(command=self.rentlist.xview)
        

        #BUTTONS#    
        rentbutton = brms.Button(frame,text="RENT BOOK", font=("Times New Roman", 12), bd=2, width=15, height=1, command = self.rent_book)
        rentbutton.place(x=70, y= 460)
        returnbutton = brms.Button(frame,text="RETURN BOOK", font=("Times New Roman", 12), bd=2, width=15, height=1, command = self.return_book)
        returnbutton.place(x=250, y=460)
        refrlist = brms.Button(frame,text="REFRESH LIST", font=("Times New Roman", 12), bd=2, width=15, height=1, command = self.refresh_rentlist)
        refrlist.place(x=160, y=510)
        
        #WIDGET BUTTONS#
        buttonframe = brms.LabelFrame(self,bg="royalblue4", relief=brms.GROOVE, bd=5)
        buttonframe.place(x=360, y=670, width=650, height=50)
        
        button0 = brms.Button(buttonframe,text="HOME",font=("Times New Roman",12),bd=2,width = 14,command=lambda: controller.show_frame(HomePage))
        button0.place(x=20, y=4)
        button1 = brms.Button(buttonframe, text="BOOKS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(BooksPage))
        button1.place(x=175, y=4)
        button2 = brms.Button(buttonframe, text="BORROWERS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(BorrowersPage))
        button2.place(x=330, y=4)
        button4 = brms.Button(buttonframe, text="RESERVATIONS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(ReservationsPage))
        button4.place(x=485, y=4)

    def rent_book(self):
        book_no = self.bookno_en.get()
        borrower_no = self.borrowernoentry.get()
        start_date = self.start_date_entry.get()
        due_date = self.due_date_entry.get()

        # Establish a connection to the SQLite database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor() 

        # Check if the book exists in the database
        cursor.execute("SELECT * FROM books WHERE bookno = ?", (book_no,))
        book = cursor.fetchone()

        if book:
            if book[1] == "Rented" or book[1] == "Reserved":
                messagebox.showerror("Error", "Book is not available for renting")
                connection.close()
                return  # Exit the method if the book is not available
            else:
                # Update the status of the book in the database
                cursor.execute("UPDATE books SET status = ? WHERE bookno = ?", ("Rented", book_no))
                connection.commit()

                # Insert the rent information into the database
                cursor.execute("INSERT INTO rents (bookno, borrowerNo, startDate, dueDate) VALUES (?, ?, ?, ?)",
                            (book_no, borrower_no, start_date, due_date))
                connection.commit()

                # Close the connection
                connection.close()

                messagebox.showinfo("Success", "Book has been rented")

                # Insert the rent information into the Treeview
                self.insert_rent(book_no, borrower_no, start_date, due_date)

                # Insert the borrower information into the borrowers' database table and Treeview
                self.controller.frames[BorrowersPage].insert_borrower(
                    borrower_no, self.nameentry.get(), self.addressentry.get(),
                    self.phoneentry.get(), self.validentry.get()
                )

        else:
            messagebox.showerror("Error", "Book number not found")

        # Clear entry fields
        self.bookno_en.delete(0, "end")
        self.borrowernoentry.delete(0, "end")
        self.nameentry.delete(0, "end")
        self.addressentry.delete(0, "end")
        self.phoneentry.delete(0, "end")
        self.validentry.delete(0, "end")

    
    def insert_rent(self, book_no, borrower_no, start_date, due_date):
        self.rentlist.insert("", "end", values=(book_no, borrower_no, start_date, due_date))
        
    def return_book(self):
        return_window = Toplevel(self)
        return_window.title("Return Book")
        # Configure the window size and position according to your requirements
        return_window.geometry("380x230+400+300")

        # Example: Add a label and an entry widget for book title
        label = Label(return_window, text="RETURN BOOKS", font=("Bebas 12 bold"), fg="#fff", bg="royalblue4", border=5, relief=GROOVE)
        label.pack(side=TOP, fill=X)

        frame = Frame(return_window, bg="gray", relief=RIDGE, bd=5)
        frame.place(x=5, y=40, height=180, width=368)

        # ENTRIES AND LABELS
        self.bookno = Label(frame, text="BOOK NO", font=("Times New Roman", 12, 'bold'), bg="gray", fg="white", width=10)
        self.bookno.place(x=10, y=10)

        self.bookno_en_return = Entry(frame, font=("Times New Roman", 11), width=20, relief=RIDGE, bd=2)
        self.bookno_en_return.place(x=110, y=10)

        self.borrowerno = Label(frame, text="BORROWER NO", font=("Times New Roman", 12, 'bold'), bg="gray", fg="white")
        self.borrowerno.place(x=16, y=40)

        self.borrowernoentry_return = Entry(frame, font=("Times New Roman", 11), width=20, relief=RIDGE, bd=2)
        self.borrowernoentry_return.place(x=157, y=40)

        self.return_date = Label(frame, text="RETURN DATE", font=("Times New Roman", 12, 'bold'), bg="gray", fg="white")
        self.return_date.place(x=16, y=70)

        self.return_date_entry = Entry(frame, font=("Times New Roman", 11), width=20, relief=RIDGE, bd=2)
        self.return_date_entry.place(x=157, y=70)
        current_date = datetime.today().date()
        self.return_date_entry.insert(0, current_date)

        ret_button = Button(frame, text="RETURN", font=("Times New Roman", 11), bd=2, width=9, height=1, command=lambda:self.ret_book(return_window))
        ret_button.place(x=140, y=135)

    def ret_book(self, return_window):
        book_no = self.bookno_en_return.get()
        return_date = self.return_date_entry.get()

        # Establish a connection to the SQLite database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()

        # Check if the book exists in the database
        cursor.execute("SELECT * FROM books WHERE bookno = ?", (book_no,))
        book = cursor.fetchone()

        if book:
            if book[1] != "Rented":
                messagebox.showerror("Error", "Book is not currently rented")
                connection.close()
                return  # Exit the method if the book is not rented
            else:
                # Update the status of the book to "Available"
                cursor.execute("UPDATE books SET status = ? WHERE bookno = ?", ("Available", book_no))
                connection.commit()

                # Retrieve the due date from the RentsPage
                cursor.execute("SELECT dueDate FROM rents WHERE bookno = ?", (book_no,))
                rent = cursor.fetchone()
                if rent:
                    due_date = datetime.strptime(rent[0], "%Y-%m-%d").date()
                    return_date = datetime.strptime(return_date, "%Y-%m-%d").date()
                    if return_date > due_date:
                        # Calculate the number of days the book is overdue
                        days_overdue = (return_date - due_date).days

                        # Calculate the fines (100 + 10 per day)
                        fines = 100 + (10 * days_overdue)
                    else:
                        fines = 0

                    cursor.execute("UPDATE rents SET returnDate = ?, fines = ? WHERE bookno = ?", (return_date, fines, book_no))
                    connection.commit()

                    messagebox.showinfo("Success", "Book has been returned")

                    # Update the return information in the rentlist Treeview
                    for item in self.controller.frames[RentsPage].rentlist.get_children():
                        values = self.controller.frames[RentsPage].rentlist.item(item, "values")
                        if values[0] == book_no:
                            self.controller.frames[RentsPage].rentlist.set(item, column="Return Date", value=str(return_date))
                            self.controller.frames[RentsPage].rentlist.set(item, column="Fines", value=str(fines))
                            break
                else:
                    messagebox.showerror("Error", "Due date information is missing for the book")
                    connection.close()
                    return
        else:
            messagebox.showerror("Error", "Book number not found")

        connection.close()

        # Clear entry fields
        self.bookno_en_return.delete(0, END)
        self.return_date_entry.delete(0, END)
        return_window.destroy()
        
    def refresh_rentlist(self):
        # Clear the current items in the rentlist Treeview
        rentlist = self.controller.frames[RentsPage].rentlist
        rentlist.delete(*rentlist.get_children())

        # Establish a connection to the SQLite database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()

        # Retrieve the data from the rents table
        cursor.execute("SELECT * FROM rents")
        rent_data = cursor.fetchall()

        # Iterate over the rows and insert them into the rentlist Treeview
        for rent in rent_data:
            book_no = rent[0]
            borrower_no = rent[1]
            start_date = rent[2]
            due_date = rent[3]
            return_date = rent[4]
            fines = rent[5]
            
            # Check if the book exists in the books database table
            cursor.execute("SELECT * FROM books WHERE bookno = ?", (book_no,))
            book = cursor.fetchone()
            
            if book:
                # Insert the rent information into the rentlist Treeview
                rentlist.insert("", "end", values=(book_no, borrower_no, start_date, due_date, return_date, fines))
            else:
                # Delete the corresponding rental record from the rents table
                cursor.execute("DELETE FROM rents WHERE bookno = ?", (book_no,))
                connection.commit()

        connection.close()
class ReservationsPage(brms.Frame):
    def __init__(self, parent, controller):
        brms.Frame.__init__(self, parent)
        self.controller = controller
        self.books_page = controller.frames[BooksPage]
        self.borrowers_page = controller.frames[BorrowersPage]
        self.rents_page = controller.frames[RentsPage]
        self.reservations = {}
        label = brms.Label(self, text="RESERVATION BOOKS", font=("Bebas 25 bold"), fg="#fff", bg="royalblue4", border=10, relief=brms.GROOVE)
        label.place(x=0,y=0, width=1358)
        frame = brms.LabelFrame(self, height=100, width=400, bg="royalblue4", relief=brms.GROOVE, bd=5)
        frame.place(x=15, y=75, width=1328, height=580)
        frame1 = brms.Label(frame, text="RESERVATION INFO",font=("Bebas 25 bold"), fg="#fff", bg="royalblue4", border=7, relief=brms.GROOVE )
        frame1.place(x=45, y=25, width=360)
        
        # Establish connection to SQLite database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()
        # Create the 'reservations' table if it doesn't exist
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS reservations(
                        bookno INT REFERENCES books(bookno) ON DELETE CASCADE,
                        borrowerNo INT REFERENCES borrower(borrowerNo) ON DELETE CASCADE, 
                        reserveDate VARCHAR(255), 
                        reserveDue VARCHAR(255))
                    ''')
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        #Labels and Entries#
        borrowernolabel = Label(frame,text="BORROWER NO",font=("Times New Roman",12), bg="royalblue4", fg="white")
        borrowernolabel.place(x=5,y=123)
        self.borrowernoentry = Entry(frame,font=("Times New Roman",12), width=20, relief=RIDGE, bd=2)
        self.borrowernoentry.place(x=130, y=122)
        namelabel = Label(frame, text="NAME",font=("Times New Roman",12), bg="royalblue4", fg="white", width=12)
        namelabel.place(x=5, y=158)
        self.nameentry = Entry(frame,font=("Times New Roman",12), width=40, relief=RIDGE, bd=2)
        self.nameentry.place(x=130, y=157)
        addresslabel = Label(frame, text="ADDRESS",font=("Times New Roman",12), bg="royalblue4", fg="white", width=12)
        addresslabel.place(x=5, y=193)
        self.addressentry = Entry(frame,font=("Times New Roman",12), width=40, relief=RIDGE, bd=2)
        self.addressentry.place(x=130, y=192)
        phonelabel = Label(frame, text="PHONE NO",font=("Times New Roman",12), bg="royalblue4", fg="white", width=12)
        phonelabel.place(x=5, y=228)
        self.phoneentry = Entry(frame,font=("Times New Roman",12), width=40, relief=RIDGE, bd=2)
        self.phoneentry.place(x=130, y=227)
        validid = Label(frame, text="VALID ID",font=("Times New Roman",12), bg="royalblue4", fg="white", width=12)
        validid.place(x=5, y=263)
        self.validentry = Entry(frame,font=("Times New Roman",12), width=20, relief=RIDGE, bd=2)
        self.validentry.place(x=130, y=262)
        
        bookno = Label(frame, text="BOOK NO",font=("Times New Roman",12), bg="royalblue4", fg="white", width=12)
        bookno.place(x=25, y=325)
        self.bookno_en = Entry(frame,font=("Times New Roman",12), width=20, relief=RIDGE, bd=2)
        self.bookno_en.place(x=165, y=324)
        
        #Date Entries#
        start_label = Label(frame, text="RESERVATION DATE", font=("Times New Roman",12), bg="royalblue4", fg="white" )
        start_label.place(x=5, y=360)
        self.start_date_entry = Entry(frame,font=("Times New Roman",12), width=20, relief=RIDGE, bd=2)
        self.start_date_entry.place(x=165, y=359)
        due_label = Label(frame, text="RESERVATION DUE", font=("Times New Roman",12), bg="royalblue4", fg="white")
        due_label.place(x=10, y=395)
        self.due_date_entry = Entry(frame,font=("Times New Roman",12), width=20, relief=RIDGE, bd=2)
        self.due_date_entry.place(x=165, y=394)
        current_date = datetime.today().date()
        due_date = current_date + timedelta(days=3)
        self.start_date_entry.insert(0, current_date)
        self.due_date_entry.insert(0, due_date)
        
        #TREEVIEW#
        y_scrollbar = Scrollbar(frame, orient=VERTICAL)
        y_scrollbar.place(x=1290,y=30,height=522)
        x_scrollbar = Scrollbar(frame, orient=HORIZONTAL)
        x_scrollbar.place(x=500, y=535,width=790)
        self.reslist = ttk.Treeview(frame,columns=("BookNo", "BorrowerNo", "Reservation Date", "Reservation Due"),height = 16, 
                                     yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        self.reslist.heading("BookNo", text="BOOKNO")
        self.reslist.heading("BorrowerNo", text="BORROWERNO")
        self.reslist.heading("Reservation Date", text="RESERVATION DATE")
        self.reslist.heading("Reservation Due", text="RESERVATION DUE")
        self.reslist['show'] = 'headings'
        self.reslist.place(x=500,y=30, width=790, height=505)
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("Treeview.Heading", font=("Times New Roman",12,"bold"),foreground="Black")
        style.configure("Treeview",font=("Times New Roman",11))
        style.map('Treeview', background=[('selected', 'grey')], foreground=[('selected', 'Black')])
        self.reslist.column("BookNo", width=150, anchor="center")
        self.reslist.column("BorrowerNo", width=150, anchor="center")
        self.reslist.column("Reservation Date", width=150, anchor="center")
        self.reslist.column("Reservation Due", width=150, anchor="center")
        y_scrollbar.config(command=self.reslist.yview)
        x_scrollbar.config(command=self.reslist.xview)

        #BUTTONS#
        resbutton = brms.Button(frame,text="RESERVE BOOK", font=("Times New Roman", 12), bd=2, width=15, height=1, command = self.reserve_book)
        resbutton.place(x=80, y= 460)
        renbutton = brms.Button(frame,text="RENT BOOK", font=("Times New Roman", 12), bd=2, width=15, height=1, command = self.rent_reserve_book)
        renbutton.place(x=250, y= 460)
        reflist = brms.Button(frame,text="REFRESH LIST", font=("Times New Roman", 12), bd=2, width=15, height=1, command = self.refresh_treeview)
        reflist.place(x=160, y=510)
        
        
        #WIDGET BUTTONS#
        buttonframe = brms.LabelFrame(self,bg="royalblue4", relief=brms.GROOVE, bd=5)
        buttonframe.place(x=360, y=670, width=650, height=50)
        
        button0 = brms.Button(buttonframe,text="HOME",font=("Times New Roman",12),bd=2,width = 14,command=lambda: controller.show_frame(HomePage))
        button0.place(x=20, y=4)
        button1 = brms.Button(buttonframe, text="BOOKS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(BooksPage))
        button1.place(x=175, y=4)
        button2 = brms.Button(buttonframe, text="BORROWERS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(BorrowersPage))
        button2.place(x=330, y=4)
        button4 = brms.Button(buttonframe, text="RENTS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(RentsPage))
        button4.place(x=485, y=4)
        
    def reserve_book(self):
        book_no = self.bookno_en.get()
        borrowerno = self.borrowernoentry.get()
        start_date = self.start_date_entry.get()
        due_date = self.due_date_entry.get()

        # Establish a connection to the SQLite database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()

        # Check if the book exists in the database
        cursor.execute("SELECT * FROM books WHERE bookno = ?", (book_no,))
        book = cursor.fetchone()

        if book:
            if book[1] == "Available":
                # Update the book status to "Reserved" in the database
                cursor.execute("UPDATE books SET status = ? WHERE bookno = ?", ("Reserved", book_no))
                connection.commit()

                # Insert the reservation information into the reservations table
                cursor.execute("INSERT INTO reservations (bookno, borrowerNo, reserveDate, reserveDue) VALUES (?, ?, ?, ?)",
                                (book_no, borrowerno, start_date, due_date))
                connection.commit()

                # Insert the book information into the treeview
                self.reslist.insert("", "end", values=(book_no, borrowerno, start_date, due_date))
                self.borrowers_page.insert_borrower(
                    borrowerno, self.nameentry.get(), self.addressentry.get(), self.phoneentry.get(), self.validentry.get()
                )
                reservation_id = f"{book_no}_{borrowerno}_{start_date}_{due_date}"
                reservation = {
                    'BookNo': book_no,
                    'BorrowerNo': borrowerno,
                    'StartDate': start_date,
                    'DueDate': due_date
                }
                self.reservations[reservation_id] = reservation

                # Show success message
                messagebox.showinfo("Success", "Book has been successfully reserved!")

                # Check if the due date has passed
                self.check_due_date(book_no, borrowerno, start_date, due_date)

            else:
                messagebox.showerror("Error", "Book is not available for reservation")
        else:
            messagebox.showerror("Error", "Book number not found")

        # Close the connection
        connection.close()

        # Clear entry fields
        self.bookno_en.delete(0, "end")
        self.borrowernoentry.delete(0, "end")
        self.nameentry.delete(0, "end")
        self.addressentry.delete(0, "end")
        self.phoneentry.delete(0, "end")
        self.validentry.delete(0, "end")
        
    def check_due_date(self, book_no, borrowerno, start_date, due_date):
        # Check if the due date has passed
        current_date = date.today()
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        if current_date >= due_date:
            # Remove the reservation from the treeview
            for item in self.reslist.get_children():
                values = self.reslist.item(item, "values")
                if values[0] == book_no and values[1] == borrowerno and values[2] == start_date and values[3] == due_date:
                    self.reslist.delete(item)
                    break

            # Update the book status to "Available" in the database
            connection = sqlite3.connect("brms.db")
            # Update the book status to "Available" in the database
            cursor = connection.cursor() 
            cursor.execute("UPDATE books SET status = ? WHERE bookno = ?", ("Available", book_no))
            connection.commit()

            # Remove the reservation from the reservations table
            cursor.execute("DELETE FROM reservations WHERE bookno = ? AND borrowerNo = ?",
                        (book_no, borrowerno))
            connection.commit()

            # Remove the reservation from self.reservations dictionary
            reservation_id = f"{book_no}_{borrowerno}_{start_date}_{due_date}"
            if reservation_id in self.reservations:
                del self.reservations[reservation_id]

            # Close the connection
            connection.close()

    def rent_reserve_book(self):
        selected_item = self.reslist.selection()
        if selected_item:
            book_no = self.reslist.item(selected_item, "values")[0]
            borrowerno = self.reslist.item(selected_item, "values")[1]
            start_date = self.reslist.item(selected_item, "values")[2]
            due_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=7)
            due_date = due_date.strftime("%Y-%m-%d")

            # Establish a connection to the SQLite database
            connection = sqlite3.connect("brms.db")
            cursor = connection.cursor()

            # Check if the reservation exists in the database
            cursor.execute("SELECT * FROM reservations WHERE bookno = ? AND borrowerNo = ?", (book_no, borrowerno))
            reservation = cursor.fetchone()

            if reservation:
                # Remove the selected item from the treeview
                self.reslist.delete(selected_item)

                # Update the book status to "Rented" in the database
                cursor.execute("UPDATE books SET status = ? WHERE bookno = ?",
                            ("Rented", book_no))
                connection.commit()

                # Insert the rented book information into the rents table
                cursor.execute("INSERT INTO rents (bookno, borrowerNo, startDate, dueDate) VALUES (?, ?, ?, ?)",
                            (book_no, borrowerno, start_date, due_date))
                connection.commit()

                # Delete the reservation from the reservations table
                cursor.execute("DELETE FROM reservations WHERE bookno = ? AND borrowerNo = ?", (book_no, borrowerno))
                connection.commit()

                # Close the connection
                connection.close()

                # Update the book status in the BooksPage class
                for book in self.books_page.books:
                    if book['BookNo'] == book_no and book['Status'] == "Reserved" and book.get('BorrowerNo') == borrowerno:
                        book['Status'] = "Rented"
                        book['StartDate'] = start_date
                        book['DueDate'] = due_date
                        break

                # Insert the rented book information into the RentsPage treeview
                self.rents_page.insert_rent(book_no, borrowerno, start_date, due_date)

                # Show success message
                messagebox.showinfo("Success", "Book has been successfully rented!")
            else:
                messagebox.showerror("Error", "Selected item is not reserved by the specified borrower number")
                connection.close()
        else:
            messagebox.showerror("Error", "No item selected")
            
    def refresh_treeview(self):
        # Clear existing items in the treeview
        self.reslist.delete(*self.reslist.get_children())

        # Establish a connection to the SQLite database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()

        # Retrieve reservation data from the reservations table
        cursor.execute("SELECT * FROM reservations")
        reservations = cursor.fetchall()

        # Iterate over the reservations and check if the corresponding book still exists
        for reservation in reservations:
            book_no = reservation[0]
            borrower_no = reservation[1]
            start_date = reservation[2]
            due_date = reservation[3]

            # Check if the book exists in the books table
            cursor.execute("SELECT * FROM books WHERE bookno = ?", (book_no,))
            book = cursor.fetchone()

            if book:
                # Insert the reservation into the treeview
                self.reslist.insert("", "end", values=(book_no, borrower_no, start_date, due_date))
            else:
                # Book doesn't exist, delete the reservation from the reservations table
                cursor.execute("DELETE FROM reservations WHERE bookno = ? AND borrowerNo = ?",
                            (book_no, borrower_no))
                connection.commit()

        # Close the connection
        connection.close()
        
class BorrowersPage(brms.Frame):
    def __init__(self, parent, controller):
        brms.Frame.__init__(self, parent)
        self.controller = controller
        self.borrowers = {}
        label = brms.Label(self, text="BORROWER INFORMATION", font=("Bebas 25 bold"), fg="#fff", bg="royalblue4", border=10, relief=brms.GROOVE)
        label.place(x=0,y=0, width=1358)
        frame = brms.LabelFrame(self, height=100, width=400, bg="royalblue4", relief=brms.GROOVE, bd=5)
        frame.place(x=15, y=75, width=1328, height=580)
        # Establish connection to SQLite database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        # Create the 'borrower' table if it doesn't exist
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS borrower(
                        borrowerNo INT PRIMARY KEY ON CONFLICT IGNORE, 
                        name VARCHAR(255), 
                        address VARCHAR(255),
                        phoneNo VARCHAR(255),
                        validId VARCHAR(255))
                    ''')
        # Commit and close the connection
        connection.commit()
        connection.close()
        ## BOOK TREEVIEW ##
        y_scrollbar = Scrollbar(frame, orient=VERTICAL)
        y_scrollbar.place(x=1295,y=70,height=492)
        x_scrollbar = Scrollbar(frame, orient=HORIZONTAL)
        x_scrollbar.place(x=5, y=545,width=1290)
        self.borrowlist = ttk.Treeview(frame,columns=("BorrowerNo", "Name", "Address", "Phone_Number", "Valid ID"),height = 16, 
                                     yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        self.borrowlist.heading("BorrowerNo", text="BORROWERNO")
        self.borrowlist.heading("Name", text="NAME")
        self.borrowlist.heading("Address", text="ADDRESS")
        self.borrowlist.heading("Phone_Number", text="PHONE NUMBER")
        self.borrowlist.heading("Valid ID", text="VALID ID")
        self.borrowlist['show'] = 'headings'
        self.borrowlist.place(x=5,y=70, width=1290, height=475)
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("Treeview.Heading", font=("Times New Roman",12,"bold"),foreground="Black")
        style.configure("Treeview",font=("Times New Roman",11))
        style.map('Treeview', background=[('selected', 'grey')], foreground=[('selected', 'Black')])
        self.borrowlist.column("BorrowerNo", width=150, anchor="center")
        self.borrowlist.column("Name", width=400, anchor="center")
        self.borrowlist.column("Address", width=400, anchor="center")
        self.borrowlist.column("Phone_Number", width=150, anchor="center")
        self.borrowlist.column("Valid ID", width=150, anchor="center")
        y_scrollbar.config(command=self.borrowlist.yview)
        x_scrollbar.config(command=self.borrowlist.xview) 
        
        #TREEVIEW BUTTONS#
        searchlabel = Label(frame, text="SEARCH",font=("Times New Roman",15), bg="royalblue4", fg="white")
        searchlabel.place(x=30, y=30)
        self.searchborroweren = Entry(frame,font=("Times New Roman",12), width=55, relief=RIDGE)
        self.searchborroweren.place(x=130, y=33)
        searchbutton = brms.Button(frame, text="SEARCH", font=("Times New Roman",12),bd=2,width = 10, command=self.search_borrower)
        searchbutton.place(x=590, y=28)
        borlistbutton = brms.Button(frame, text="LIST", font=("Times New Roman",12),bd=2,width = 10, command=self.show_all_borrowers)
        borlistbutton.place(x=710, y=28)
        #WIDGET BUTTONS#
        buttonframe = brms.LabelFrame(self,bg="royalblue4", relief=brms.GROOVE, bd=5)
        buttonframe.place(x=360, y=670, width=650, height=50)
        
        button0 = brms.Button(buttonframe, text="HOME", font=("Times New Roman",12),bd=2,width = 14, command=lambda: controller.show_frame(HomePage))
        button0.place(x=20, y=4)
        button1 = brms.Button(buttonframe, text="BOOKS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(BooksPage))
        button1.place(x=175, y=4)
        button3 = brms.Button(buttonframe, text="RENTS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(RentsPage))
        button3.place(x=330, y=4)
        button4 = brms.Button(buttonframe, text="RESERVATIONS", font= ("Times New Roman",12),bd=2,width = 14, command=lambda:controller.show_frame(ReservationsPage))
        button4.place(x=485, y=4)
            
    def insert_borrower(self, borrower_no, name, address, phone_number, valid_id):
        # Check if the borrower number already exists in the dictionary
        if borrower_no in self.borrowers:
            # If the borrower already exists, update the information
            self.borrowers[borrower_no] = {
                'Name': name,
                'Address': address,
                'Phone_Number': phone_number,
                'Valid ID': valid_id
            }
            # Find the item in the treeview and update its values
            for item in self.borrowlist.get_children():
                if self.borrowlist.item(item, 'values')[0] == borrower_no:
                    self.borrowlist.item(item, values=(borrower_no, name, address, phone_number, valid_id))
                    break
        else:
            # If the borrower does not exist, insert the information into the dictionary and treeview
            self.borrowers[borrower_no] = {
                'Name': name,
                'Address': address,
                'Phone_Number': phone_number,
                'Valid ID': valid_id
            }
            self.borrowlist.insert("", "end", values=(borrower_no, name, address, phone_number, valid_id))

        # Insert the borrower information into the "borrower" table in the database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO borrower (borrowerNo, name, address, phoneNo, validId) VALUES (?, ?, ?, ?, ?)",
            (borrower_no, name, address, phone_number, valid_id)
        )
        connection.commit()
        connection.close()

    def search_borrower(self):
        search_query = self.searchborroweren.get().lower()

        # Clear the current search results
        self.borrowlist.delete(*self.borrowlist.get_children())

        # Search for borrowers based on the provided query
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM borrower WHERE borrowerNo LIKE ? OR LOWER(name) LIKE ?",
                    ('%' + search_query + '%', '%' + search_query + '%'))
        rows = cursor.fetchall()
        connection.close()

        if rows:
            for row in rows:
                # Insert the matching borrower into the treeview
                borrower_no = row[0]
                name = row[1]
                address = row[2]
                phone_number = row[3]
                valid_id = row[4]
                self.borrowlist.insert("", "end", values=(borrower_no, name, address, phone_number, valid_id))
            self.searchborroweren.delete(0, 'end')
        else:
            # Display an error message if no match is found
            messagebox.showerror("Error", "Borrower not found")

        # Clear the search input field
        self.searchborroweren.delete(0, 'end')


    def show_all_borrowers(self):
        # Clear the current search results
        self.borrowlist.delete(*self.borrowlist.get_children())

        # Fetch all borrowers from the database
        connection = sqlite3.connect("brms.db")
        cursor = connection.cursor() 
        cursor.execute("SELECT * FROM borrower")
        rows = cursor.fetchall()
        connection.close()

        if rows:
            for row in rows:
                # Insert the borrower information into the treeview
                borrower_no = row[0]
                name = row[1]
                address = row[2]
                phone_number = row[3]
                valid_id = row[4]
                self.borrowlist.insert("", "end", values=(borrower_no, name, address, phone_number, valid_id))
        else:
            # Display a message if no borrowers are found
            messagebox.showinfo("Information", "No borrowers found")

        # Clear the search input field
        self.searchborroweren.delete(0, 'end')

        
if __name__ == "__main__":
    app = Application()
    app.geometry("1358x753+0+0")
    app.title("Book Rental Management Application")
    app.mainloop()