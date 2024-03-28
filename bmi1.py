from tkinter import *
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

# Function to initialize database
def initialize_database():
    try:
        conn = sqlite3.connect('bmi_data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS bmi_records
                     (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT, height INTEGER, weight INTEGER, bmi REAL)''')
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f'Error occurred while initializing database: {e}')
    finally:
        if conn:
            conn.close()

# Function to insert BMI data into database
def insert_bmi_data(name, age, gender, height, weight, bmi):
    try:
        conn = sqlite3.connect('bmi_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO bmi_records (name, age, gender, height, weight, bmi) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, age, gender, height, weight, bmi))
        conn.commit()
        show_insert_feedback()
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f'Error occurred while inserting data: {e}')
    finally:
        if conn:
            conn.close()

# Function to reset entry fields
def reset_entry():
    name_var.set('')
    age_var.set('')
    height_var.set('')
    weight_var.set('')
    result_var.set('')
    male_rb.deselect()
    female_rb.deselect()

# Function to calculate BMI
def calculate_bmi():
    name = name_var.get()
    age = age_var.get()
    height = height_var.get()
    weight = weight_var.get()
    gender = gender_var.get()

    if name and age and height and weight and gender:
        try:
            age = int(age)
            height = int(height)
            weight = int(weight)
            bmi = round(weight / ((height / 100) ** 2), 1)
            result_var.set(f'BMI: {bmi}')
            bmi_index(bmi)
            insert_bmi_data(name, age, gender, height, weight, bmi)
        except ValueError:
            messagebox.showerror('Input Error', 'Please enter valid numeric values for age, height, and weight.')
    else:
        messagebox.showerror('Input Error', 'Please fill in all the fields.')

# Function to display BMI index
def bmi_index(bmi):
    if bmi < 18.5:
        messagebox.showinfo('BMI', f'BMI = {bmi} is Underweight')
    elif 18.5 <= bmi < 24.9:
        messagebox.showinfo('BMI', f'BMI = {bmi} is Normal')
    elif 24.9 <= bmi < 29.9:
        messagebox.showinfo('BMI', f'BMI = {bmi} is Overweight')
    else:
        messagebox.showinfo('BMI', f'BMI = {bmi} is Obesity')

# Function to plot BMI data
def plot_bmi_data():
    try:
        conn = sqlite3.connect('bmi_data.db')
        c = conn.cursor()
        c.execute("SELECT bmi FROM bmi_records")
        data = c.fetchall()
        conn.close()
        if data:
            bmi_values = [record[0] for record in data]
            plt.hist(bmi_values, bins=10, color='skyblue', edgecolor='black')
            plt.xlabel('BMI')
            plt.ylabel('Frequency')
            plt.title('BMI Distribution')
            plt.grid(True)
            plt.show()
        else:
            show_plot_feedback()
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f'Error occurred while accessing database: {e}')

# Function to show feedback message after inserting BMI data
def show_insert_feedback():
    messagebox.showinfo('Feedback', 'BMI data successfully inserted into the database.')

# Function to show feedback message when there is no data to plot
def show_plot_feedback():
    messagebox.showinfo('Feedback', 'No BMI data available to plot.')

# Function to exit the application
def exit_application():
    ws.destroy()

# Function to open an "Edit" window
def open_edit_window():
    edit_window = Toplevel(ws)
    edit_window.title("Edit")

# Initialize database
initialize_database()

# GUI setup
ws = Tk()
ws.title('BMI Calculator')

# Frame setup
frame = Frame(ws, padx=10, pady=10)
frame.pack(expand=True)

# Labels setup
Label(frame, text="Enter Name:").grid(row=0, column=0, sticky='w')
Label(frame, text="Enter Age (2 - 120):").grid(row=1, column=0, sticky='w')
Label(frame, text='Select Gender:').grid(row=2, column=0, sticky='w')
Label(frame, text="Enter Height (cm):").grid(row=3, column=0, sticky='w')
Label(frame, text="Enter Weight (kg):").grid(row=4, column=0, sticky='w')

result_var = StringVar()  # Define result_var
Label(frame, textvariable=result_var, fg='blue').grid(row=6, column=0, columnspan=2, pady=10)

# Entries setup
name_var = StringVar()
name_entry = Entry(frame, textvariable=name_var)
name_entry.grid(row=0, column=1)
age_var = StringVar()
age_entry = Entry(frame, textvariable=age_var)
age_entry.grid(row=1, column=1)
height_var = StringVar()
height_entry = Entry(frame, textvariable=height_var)
height_entry.grid(row=3, column=1)
weight_var = StringVar()
weight_entry = Entry(frame, textvariable=weight_var)
weight_entry.grid(row=4, column=1)

# Radio buttons setup
gender_var = StringVar()
male_rb = Radiobutton(frame, text='Male', variable=gender_var, value='Male')
male_rb.grid(row=2, column=1, sticky='w')
female_rb = Radiobutton(frame, text='Female', variable=gender_var, value='Female')
female_rb.grid(row=2, column=1, sticky='e')

# Menu setup
menu = Menu(ws)
ws.config(menu=menu)
file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Edit", command=open_edit_window)

# Buttons setup
Button(frame, text='Calculate', command=calculate_bmi).grid(row=5, column=0, pady=5)
Button(frame, text='Reset', command=reset_entry).grid(row=5, column=1, pady=5)
Button(frame, text='Plot BMI Data', command=plot_bmi_data).grid(row=6, column=0, pady=5)
Button(frame, text='Exit', command=exit_application).grid(row=6, column=1, pady=5)

# Run GUI
ws.mainloop()
