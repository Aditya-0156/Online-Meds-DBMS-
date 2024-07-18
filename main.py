from datetime import datetime
from random import random
from tkinter import END, messagebox
import tkinter as tk
from connection import db
from tkinter import ttk
import random

def add_user(user_id_entry, user_name_entry, user_password_entry, age_entry, phone_num_entry):
    user_id = user_id_entry.get()
    user_name = user_name_entry.get()
    user_password = user_password_entry.get()
    age = age_entry.get()
    phone_num = phone_num_entry.get()

    # Insert the user into the database
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO Users (User_ID, User_Name, User_Password, Age, Phone_Num) VALUES (%s, %s, %s, %s, %s)",
                   (int(user_id), user_name, user_password, age, phone_num))
    except Exception as e:
        print(e)
    db.commit()

    # Clear the input fields
    user_id_entry.delete(0, END)
    user_name_entry.delete(0, END)
    user_password_entry.delete(0, END)
    age_entry.delete(0, END)
    phone_num_entry.delete(0, END)
def display_user_info(root,user_id, password):
    user_id = user_id.get()
    password = password.get()
    # execute the SQL query to select the user info based on the user_id and password
    query = "SELECT * FROM Users WHERE User_ID=%s AND User_Password=%s"
    cursor=db.cursor()
    cursor.execute(query, (user_id, password))

    # fetch the first row of the result set
    user_info = cursor.fetchone()

    if user_info:
        # create a new window for the user info
        user_info_window = tk.Toplevel(root)
        user_info_window.title("User Info")
        user_info_window.geometry("720x600")
        user_info_window.grab_set()

        # create a frame for the user info
        user_info_frame = tk.Frame(user_info_window)
        user_info_frame.pack(expand=True)

        # create labels and entry boxes for each field in the user info
        user_id_label = tk.Label(user_info_frame, text="User ID: ")
        user_id_label.grid(row=0, column=0)
        user_id_entry = tk.Entry(user_info_frame, state="readonly")
        user_id_entry.grid(row=0, column=1)
        user_id_entry.insert(0, user_info[0])  # set the default value for user_id

        user_name_label = tk.Label(user_info_frame, text="User Name: ")
        user_name_label.grid(row=1, column=0)
        user_name_entry = tk.Entry(user_info_frame)
        user_name_entry.grid(row=1, column=1)
        user_name_entry.insert(0, user_info[1])  # set the default value for user_name

        password_label = tk.Label(user_info_frame, text="Password ")
        password_label.grid(row=2, column=0)
        password_entry = tk.Entry(user_info_frame)
        password_entry.grid(row=2, column=1)
        password_entry.insert(0, user_info[2])

        age_label = tk.Label(user_info_frame, text="Age: ")
        age_label.grid(row=3, column=0)
        age_entry = tk.Entry(user_info_frame)
        age_entry.grid(row=3, column=1)
        age_entry.insert(0, user_info[3])  # set the default value for age

        phone_num_label = tk.Label(user_info_frame, text="Phone Number: ")
        phone_num_label.grid(row=4, column=0)
        phone_num_entry = tk.Entry(user_info_frame)
        phone_num_entry.grid(row=4, column=1)
        phone_num_entry.insert(0, user_info[4])  # set the default value for phone_num

        def take_order():
            order_window = tk.Toplevel()
            order_window.title("Place Order")
            order_window.grab_set()
            # Create widgets for taking input
            medicine_label = tk.Label(order_window, text="Enter medicine serial number:")
            medicine_entry = tk.Entry(order_window)
            pin_label = tk.Label(order_window, text="Enter delivery pincode:")
            pin_entry = tk.Entry(order_window)
            house_num_label = tk.Label(order_window, text="Enter house number:")
            house_num_entry = tk.Entry(order_window)
            city_label = tk.Label(order_window, text="Enter city:")
            city_entry = tk.Entry(order_window)
            state_label = tk.Label(order_window, text="Enter state:")
            state_entry = tk.Entry(order_window)

            # Place widgets using grid
            medicine_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            medicine_entry.grid(row=0, column=1, padx=5, pady=5)
            pin_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            pin_entry.grid(row=1, column=1, padx=5, pady=5)
            house_num_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            house_num_entry.grid(row=2, column=1, padx=5, pady=5)
            city_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
            city_entry.grid(row=3, column=1, padx=5, pady=5)
            state_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
            state_entry.grid(row=4, column=1, padx=5, pady=5)

            def place_order():
                # Get values from input widgets
                medicine = int(medicine_entry.get())
                pin = int(pin_entry.get())
                house_num = int(house_num_entry.get())
                city = city_entry.get()
                state = state_entry.get()

                # Insert a new record into Location table
                cursor.execute("INSERT INTO Location (House_num, City, State, Pincode) VALUES (%s, %s, %s, %s)",
                               (house_num, city, state, pin))
                db.commit()
                # Insert a new record into Orders table
                cursor.execute(
                    "INSERT INTO Orders (Order_ID, Order_Date, medicine, user_n, pin) VALUES (%s, %s, %s, %s, %s)",
                    (random.randint(1, 100000), datetime.now(), medicine, user_id, pin))
                db.commit()

                # Close the order window
                order_window.destroy()

            # Create the Place button and place it in the window
            place_button = tk.Button(order_window, text="Place Order", command=place_order)
            place_button.grid(row=5, column=0, columnspan=2, pady=20)
        def update_user_info(user_id, user_name, age, phone_num,password):
            cursor.execute(
                "UPDATE Users SET User_Name = %s, User_Password = %s, Age = %s, Phone_Num = %s WHERE User_ID = %s",
                (user_name, password, age, phone_num, user_id))

            db.commit()
            messagebox.showinfo("Success", "User information updated successfully")
        # create the "Submit" button
        submit_button = tk.Button(user_info_frame, text="Submit",
                                  command=lambda: update_user_info(user_id, user_name_entry.get(), age_entry.get(),
                                                                   phone_num_entry.get(), password))
        submit_button.grid(row=5, column=0, columnspan=2, pady=20)
        order_button = tk.Button(user_info_frame, text="Order",command=take_order)
        order_button.grid(row=5, column=2, columnspan=2, pady=20)
    else:
        # display an error message if the user info is not found
        tk.messagebox.showerror("Error", "Invalid User ID or Password")

def add_employee_record():
    # create a new window for adding employee record
    add_employee_window = tk.Toplevel()
    add_employee_window.title("Add Employee Record")
    add_employee_window.grab_set()
    # create labels and entry fields for employee information
    id_label = tk.Label(add_employee_window, text="Employee ID:")
    id_label.grid(row=0, column=0)
    id_entry = tk.Entry(add_employee_window)
    id_entry.grid(row=0, column=1)

    name_label = tk.Label(add_employee_window, text="Employee Name:")
    name_label.grid(row=1, column=0)
    name_entry = tk.Entry(add_employee_window)
    name_entry.grid(row=1, column=1)

    age_label = tk.Label(add_employee_window, text="Age:")
    age_label.grid(row=2, column=0)
    age_entry = tk.Entry(add_employee_window)
    age_entry.grid(row=2, column=1)

    phone_label = tk.Label(add_employee_window, text="Phone Number:")
    phone_label.grid(row=3, column=0)
    phone_entry = tk.Entry(add_employee_window)
    phone_entry.grid(row=3, column=1)

    # function to insert employee record into database
    def insert_employee_record():
        # get input values
        id = id_entry.get()
        name = name_entry.get()
        age = age_entry.get()
        phone = phone_entry.get()

        # insert record into database
        c = db.cursor()
        c.execute("INSERT INTO Employee (Employee_ID, Employee_Name, Age, Phone_Num) VALUES (%s,%s,%s,%s)", (id, name, age, phone))
        db.commit()

        # close window after inserting record
        add_employee_window.destroy()

    # create insert button
    insert_button = tk.Button(add_employee_window, text="Insert", command=insert_employee_record)
    insert_button.grid(row=4, column=0, columnspan=2, pady=10)
def check_employee_info(existing_user_window,employee_id, employee_name):
    # check if the entered employee ID and name match any record in the database
    c = db.cursor()
    c.execute("SELECT * FROM Employee WHERE Employee_ID=%s AND Employee_Name=%s", (employee_id, employee_name))
    result = c.fetchone()

    if result:
        # create a new window for the employee information
        employee_info_window = tk.Toplevel()
        employee_info_window.title("Employee Information")
        employee_info_window.geometry("300x300")
        employee_info_window.grab_set()

        # display "Logged in!" message
        logged_in_label = tk.Label(employee_info_window, text="Logged in!")
        logged_in_label.pack()

        # create a frame for the employee information entry boxes
        entry_frame = tk.Frame(employee_info_window)
        entry_frame.pack(pady=10)

        # create a label and entry box for employee ID (non-editable)
        employee_id_label = tk.Label(entry_frame, text="Employee ID: ")
        employee_id_label.grid(row=0, column=0)
        employee_id_entry = tk.Entry(entry_frame, state="disabled")
        employee_id_entry.insert(0, result[0])
        employee_id_entry.grid(row=0, column=1)

        # create a label and entry box for employee name
        employee_name_label = tk.Label(entry_frame, text="Employee Name: ")
        employee_name_label.grid(row=1, column=0)
        employee_name_entry = tk.Entry(entry_frame)
        employee_name_entry.insert(0, result[1])
        employee_name_entry.grid(row=1, column=1)

        # create a label and entry box for employee age
        age_label = tk.Label(entry_frame, text="Age: ")
        age_label.grid(row=2, column=0)
        age_entry = tk.Entry(entry_frame)
        age_entry.insert(0, result[2])
        age_entry.grid(row=2, column=1)

        # create a label and entry box for employee phone number
        phone_label = tk.Label(entry_frame, text="Phone Number: ")
        phone_label.grid(row=3, column=0)
        phone_entry = tk.Entry(entry_frame)
        phone_entry.insert(0, result[3])
        phone_entry.grid(row=3, column=1)

        # create a function to update the employee record in the database
        def update_employee():
            c = db.cursor()
            c.execute("UPDATE Employee SET Employee_Name=%s, Age=%s, Phone_Num=%s WHERE Employee_ID=%s",
                      (employee_name_entry.get(), age_entry.get(), phone_entry.get(), result[0]))
            db.commit()
            update_success_label = tk.Label(entry_frame, text="Record updated successfully!")
            update_success_label.grid(row=4, column=1)

        # create a button to save the updated employee record
        save_button = tk.Button(employee_info_window, text="Save", command=update_employee)
        save_button.pack()
        add_employee_button = tk.Button(employee_info_window, text="Add Employee",command=add_employee_record)
        add_employee_button.pack()
        doctor_button = tk.Button(employee_info_window, text="Doctors",command=search_doctors)
        doctor_button.pack()
        order_button = tk.Button(employee_info_window, text="Orders",command=search_orders)
        order_button.pack()
        company_button = tk.Button(employee_info_window, text="Company")
        company_button.pack()
        medicine_button = tk.Button(employee_info_window, text="Medicine",command=medicine)
        medicine_button.pack()
    else:
        # display "Invalid login. Please try again." message
        invalid_login_label = tk.Label(existing_user_window, text="Invalid login. Please try again.")
        invalid_login_label.pack()
def search_doctors():
    # function to search for doctors based on user input

    # create a new window for the search
    search_window = tk.Toplevel()
    search_window.title("Search for Doctors")
    search_window.geometry("300x300")
    search_window.grab_set()

    # create a frame for the search options
    search_frame = tk.Frame(search_window)
    search_frame.pack(pady=10)

    # create a label and entry box for doctor name search
    doctor_name_label = tk.Label(search_frame, text="Doctor Name: ")
    doctor_name_label.grid(row=0, column=0)
    doctor_name_entry = tk.Entry(search_frame)
    doctor_name_entry.grid(row=0, column=1)

    # create a label and entry box for doctor age search
    age_label = tk.Label(search_frame, text="Age: ")
    age_label.grid(row=1, column=0)
    age_entry = tk.Entry(search_frame)
    age_entry.grid(row=1, column=1)

    # create a label and entry box for doctor degree search
    degree_label = tk.Label(search_frame, text="Degree: ")
    degree_label.grid(row=2, column=0)
    degree_entry = tk.Entry(search_frame)
    degree_entry.grid(row=2, column=1)

    # create a label and entry box for doctor phone number search
    phone_label = tk.Label(search_frame, text="Phone Number: ")
    phone_label.grid(row=3, column=0)
    phone_entry = tk.Entry(search_frame)
    phone_entry.grid(row=3, column=1)

    # create a function to search for doctors based on user input
    def search():
        c = db.cursor()
        query = "SELECT * FROM Doctor WHERE "
        conditions = []
        values = []

        if doctor_name_entry.get():
            conditions.append("Doctor_Name = %s")
            values.append(doctor_name_entry.get())
        if age_entry.get():
            conditions.append("Age = %s")
            values.append(int(age_entry.get()))
        if degree_entry.get():
            conditions.append("Degree = %s")
            values.append(degree_entry.get())
        if phone_entry.get():
            conditions.append("Phone_Num = %s")
            values.append(phone_entry.get())

        query += " AND ".join(conditions)

        if conditions:
            c.execute(query, values)
            results = c.fetchall()

            # create a new window to display the search results
            results_window = tk.Toplevel()
            results_window.title("Search Results")
            results_window.geometry("300x300")
            results_window.grab_set()

            if results:
                # display the search results in a listbox
                results_listbox = tk.Listbox(results_window)
                results_listbox.pack()

                for result in results:
                    results_listbox.insert(tk.END,
                                           f"{result[0]} - {result[1]} - {result[2]} - {result[3]} - {result[4]}")
            else:
                # display "No results found." message
                no_results_label = tk.Label(results_window, text="No results found.")
                no_results_label.pack()
        else:
            # display "Please enter at least one search criteria." message
            no_criteria_label = tk.Label(search_window, text="Please enter at least one search criteria.")
            no_criteria_label.pack()

    def add_doctor():
        # function to add a new doctor to the database

        # create a new window for adding a doctor
        add_window = tk.Toplevel()
        add_window.title("Add New Doctor")
        add_window.geometry("300x300")
        add_window.grab_set()

        # create a frame for the input fields
        input_frame = tk.Frame(add_window)
        input_frame.pack(pady=10)

        # create a label and entry box for doctor name input
        doctor_id_label = tk.Label(input_frame, text="Doctor Name: ")
        doctor_id_label.grid(row=0, column=0)
        doctor_id_entry = tk.Entry(input_frame)
        doctor_id_entry.grid(row=0, column=1)

        doctor_name_label = tk.Label(input_frame, text="Doctor Name: ")
        doctor_name_label.grid(row=1, column=0)
        doctor_name_entry = tk.Entry(input_frame)
        doctor_name_entry.grid(row=1, column=1)

        # create a label and entry box for doctor age input
        age_label = tk.Label(input_frame, text="Age: ")
        age_label.grid(row=2, column=0)
        age_entry = tk.Entry(input_frame)
        age_entry.grid(row=2, column=1)

        # create a label and entry box for doctor degree input
        degree_label = tk.Label(input_frame, text="Degree: ")
        degree_label.grid(row=3, column=0)
        degree_entry = tk.Entry(input_frame)
        degree_entry.grid(row=3, column=1)

        # create a label and entry box for doctor phone number input
        phone_label = tk.Label(input_frame, text="Phone Number: ")
        phone_label.grid(row=4, column=0)
        phone_entry = tk.Entry(input_frame)
        phone_entry.grid(row=4, column=1)

        # create a label and entry box for user id input
        user_id_label = tk.Label(input_frame, text="User ID: ")
        user_id_label.grid(row=5, column=0)
        user_id_entry = tk.Entry(input_frame)
        user_id_entry.grid(row=5, column=1)

        # create a function to insert the new doctor into the database
        def insert():
            c = db.cursor()
            query = "INSERT INTO Doctor (Doctor_ID, Doctor_Name, Age, Phone_Num, Degree, User_ID) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (
            doctor_id_entry.get(), doctor_name_entry.get(), age_entry.get(), phone_entry.get(), degree_entry.get(),
            user_id_entry.get())
            db.commit
            c.execute(query, values)
            # display a success message
            messagebox.showinfo("Success", "Doctor added successfully.")

            # clear the input fields
            doctor_name_entry.delete(0, tk.END)
            age_entry.delete(0, tk.END)
            degree_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            user_id_entry.delete(0, tk.END)

        # create a button to insert the new doctor into the database
        insert_button = tk.Button(add_window, text="Insert", command=insert)
        insert_button.pack()
    # create a button to search for doctors
    search_button = tk.Button(search_window, text="Search", command=search)
    search_button.pack()
    add_button = tk.Button(search_window, text="Add Doctor",command=add_doctor)
    add_button.pack()
def search_orders():
    # function to search for orders based on user input

    # create a new window for the search
    search_window = tk.Toplevel()
    search_window.title("Search for Orders")
    search_window.geometry("300x300")
    search_window.grab_set()

    # create a frame for the search options
    search_frame = tk.Frame(search_window)
    search_frame.pack(pady=10)

    # create a label and entry box for order ID search
    order_id_label = tk.Label(search_frame, text="Order ID: ")
    order_id_label.grid(row=0, column=0)
    order_id_entry = tk.Entry(search_frame)
    order_id_entry.grid(row=0, column=1)

    # create a label and entry box for order date search
    order_date_label = tk.Label(search_frame, text="Order Date (yyyy-mm-dd): ")
    order_date_label.grid(row=1, column=0)
    order_date_entry = tk.Entry(search_frame)
    order_date_entry.grid(row=1, column=1)

    # create a label and entry box for medicine search
    medicine_label = tk.Label(search_frame, text="Medicine: ")
    medicine_label.grid(row=2, column=0)
    medicine_entry = tk.Entry(search_frame)
    medicine_entry.grid(row=2, column=1)

    # create a label and entry box for user search
    user_label = tk.Label(search_frame, text="User ID: ")
    user_label.grid(row=3, column=0)
    user_entry = tk.Entry(search_frame)
    user_entry.grid(row=3, column=1)

    # create a label and entry box for pincode search
    pincode_label = tk.Label(search_frame, text="Pincode: ")
    pincode_label.grid(row=4, column=0)
    pincode_entry = tk.Entry(search_frame)
    pincode_entry.grid(row=4, column=1)

    # create a function to search for orders based on user input
    def search_orders():
        c = db.cursor()
        query = "SELECT * FROM Orders WHERE "
        conditions = []

        if order_id_entry.get():
            conditions.append("Order_ID = %s")
        if order_date_entry.get():
            conditions.append("Order_Date = %s")
        if medicine_entry.get():
            conditions.append("medicine = %s")
        if user_entry.get():
            conditions.append("user_n = %s")
        if pincode_entry.get():
            conditions.append("pin = %s")

        if conditions:

            query += " AND ".join(conditions)
            values = tuple(
                entry.get() for entry in (order_id_entry, order_date_entry, medicine_entry, user_entry, pincode_entry)
                if entry.get())
            c.execute(query, values)
            results = c.fetchall()
            # create a new window to display the search results
            results_window = tk.Toplevel()
            results_window.title("Search Results")
            results_window.geometry("300x300")
            results_window.grab_set()

            if results:
                # display the search results in a listbox
                results_listbox = tk.Listbox(results_window)
                results_listbox.pack()

                for result in results:
                    results_listbox.insert(tk.END, f"{result[0]} - {result[1]} - {result[2]} - {result[3]} - {result[4]}")
            else:
                # display "No results found." message
                no_results_label = tk.Label(results_window, text="No results found.")
                no_results_label.pack()

    search_button = tk.Button(search_window, text="Search", command=search_orders)
    search_button.pack()
def medicine():
    # function to search for medicine based on user input

    # create a new window for the search
    search_window = tk.Toplevel()
    search_window.title("Search for Medicine")
    search_window.geometry("300x300")
    search_window.grab_set()

    # create a frame for the search options
    search_frame = tk.Frame(search_window)
    search_frame.pack(pady=10)

    # create a label and entry box for serial number search
    serial_num_label = tk.Label(search_frame, text="Serial Number: ")
    serial_num_label.grid(row=0, column=0)
    serial_num_entry = tk.Entry(search_frame)
    serial_num_entry.grid(row=0, column=1)

    # create a label and entry box for brand name search
    brand_name_label = tk.Label(search_frame, text="Brand Name: ")
    brand_name_label.grid(row=1, column=0)
    brand_name_entry = tk.Entry(search_frame)
    brand_name_entry.grid(row=1, column=1)

    # create a label and entry box for generic name search
    generic_name_label = tk.Label(search_frame, text="Generic Name: ")
    generic_name_label.grid(row=2, column=0)
    generic_name_entry = tk.Entry(search_frame)
    generic_name_entry.grid(row=2, column=1)

    # create a label and entry box for manufacturing date search
    man_date_label = tk.Label(search_frame, text="Date of Manufacturing (yyyy-mm-dd): ")
    man_date_label.grid(row=3, column=0)
    man_date_entry = tk.Entry(search_frame)
    man_date_entry.grid(row=3, column=1)

    # create a label and entry box for expiration date search
    exp_date_label = tk.Label(search_frame, text="Date of Expiration (yyyy-mm-dd): ")
    exp_date_label.grid(row=4, column=0)
    exp_date_entry = tk.Entry(search_frame)
    exp_date_entry.grid(row=4, column=1)

    # create a label and entry box for over the counter search
    otc_label = tk.Label(search_frame, text="Over the Counter (1 for Yes, 0 for No): ")
    otc_label.grid(row=5, column=0)
    otc_entry = tk.Entry(search_frame)
    otc_entry.grid(row=5, column=1)

    # create a label and entry box for price search
    price_label = tk.Label(search_frame, text="Price: ")
    price_label.grid(row=6, column=0)
    price_entry = tk.Entry(search_frame)
    price_entry.grid(row=6, column=1)

    # create a label and entry box for company search
    company_label = tk.Label(search_frame, text="Company ID: ")
    company_label.grid(row=7, column=0)
    company_entry = tk.Entry(search_frame)
    company_entry.grid(row=7, column=1)

    def search_medicine():
        c = db.cursor()
        query = "SELECT * FROM Medicine WHERE "
        conditions = []

        if serial_num_entry.get():
            conditions.append("Serial_num = %s")
        if brand_name_entry.get():
            conditions.append("Brand_Name = %s")
        if generic_name_entry.get():
            conditions.append("Generic_Name = %s")
        if man_date_entry.get():
            conditions.append("Date_of_Manufacturing = %s")
        if exp_date_entry.get():
            conditions.append("Date_of_Expiration = %s")
        if otc_entry.get():
            conditions.append("Over_counter = %s")
        if price_entry.get():
            conditions.append("Price = %s")
        if company_entry.get():
            conditions.append("company = %s")

        if conditions:
            query += " AND ".join(conditions)
            values = tuple(
                entry.get() for entry in (serial_num_entry, brand_name_entry, generic_name_entry, man_date_entry, exp_date_entry, otc_entry,price_entry, company_entry)
                if entry.get())
            c.execute(query, values)
            results = c.fetchall()

            if not results:
                messagebox.showinfo("Search Results", "No matching records found.")
            else:
                search_results_window = tk.Toplevel()
                search_results_window.title("Search Results")
                search_results_window.geometry("600x400")

                # create a table to display the search results
                table = ttk.Treeview(search_results_window)
                table["columns"] = (
                "Serial Number", "Brand Name", "Generic Name", "Manufacturing Date", "Expiration Date",
                "Over the Counter", "Price", "Company ID")
                table.column("#0", width=0, stretch="no")
                table.column("Serial Number", anchor="center", width=100)
                table.column("Brand Name", anchor="center", width=100)
                table.column("Generic Name", anchor="center", width=100)
                table.column("Manufacturing Date", anchor="center", width=100)
                table.column("Expiration Date", anchor="center", width=100)
                table.column("Over the Counter", anchor="center", width=100)
                table.column("Price", anchor="center", width=100)
                table.column("Company ID", anchor="center", width=100)

                # add the search results to the table
                for row in results:
                    table.insert("", tk.END, text="", values=row)

                table.pack(fill="both", expand=True)
        else:
            messagebox.showerror("Search Error", "Please enter at least one search criteria.")

    search_button = tk.Button(search_window, text="Search", command=search_medicine)
    search_button.pack()