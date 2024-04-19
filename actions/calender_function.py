import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

def display_calendar():
    selected_date = None

    def on_date_select():
        nonlocal selected_date
        selected_date = cal.get_date()
        print("Selected date:", selected_date)
        top.destroy()

    top = tk.Tk()  # Create a new Tk window for the calendar
    top.title("Select Date for your appointment")
    top.attributes('-topmost', True)  # Make the window topmost to ensure it grabs attention

    cal = Calendar(top, selectmode="day", year=2024, month=4, day=1)
    cal.pack(pady=20)

    select_button = ttk.Button(top, text="Select Date", command=on_date_select)
    select_button.pack()

    top.mainloop()  # Start the Tk event loop

    return selected_date