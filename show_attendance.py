import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            text_to_speech('Please enter the subject name.')
            return

        filenames = glob(f"Attendance\\{Subject}\\{Subject}*.csv")
        if not filenames:
            text_to_speech("No attendance records found for this subject.")
            return

        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = newdf.iloc[:, 2:].mean(axis=1).apply(lambda x: f"{int(round(x * 100))}%")
        newdf.to_csv(f"Attendance\\{Subject}\\attendance.csv", index=False)

        root = tkinter.Tk()
        root.title("📊 Attendance Summary")
        root.configure(background="#1f1f2e")
        cs = f"Attendance\\{Subject}\\attendance.csv"

        with open(cs) as file:
            reader = csv.reader(file)
            for r, col in enumerate(reader):
                for c, row in enumerate(col):
                    label = Label(
                        root,
                        width=12,
                        height=1,
                        fg="#00ffd5",
                        font=("Helvetica", 13, "bold"),
                        bg="#2c3e50",
                        text=row,
                        relief=RIDGE,
                        padx=5,
                        pady=5
                    )
                    label.grid(row=r, column=c, padx=2, pady=2)
        root.mainloop()

    def Attf():
        sub = tx.get()
        if sub == "":
            text_to_speech("Please enter the subject name!")
        else:
            os.startfile(f"Attendance\\{sub}")

    subject = Tk()
    subject.title("📁 Attendance Viewer")
    subject.geometry("600x350")
    subject.resizable(False, False)
    subject.configure(background="#1f1f2e")

    # Title
    title = Label(
        subject,
        text="📘 View Subject Attendance",
        bg="#1f1f2e",
        fg="#00ffd5",
        font=("Helvetica", 24, "bold"),
        pady=20
    )
    title.pack()

    # Subject Input Label
    sub_label = Label(
        subject,
        text="Subject:",
        width=10,
        bg="#1f1f2e",
        fg="#ffcc00",
        font=("Helvetica", 18, "bold")
    )
    sub_label.place(x=60, y=100)

    # Entry Field
    tx = Entry(
        subject,
        width=20,
        bd=3,
        bg="#2c3e50",
        fg="#ecf0f1",
        font=("Helvetica", 22, "bold"),
        justify="center",
        insertbackground="white"
    )
    tx.place(x=180, y=100)

    # View Attendance Button
    fill_btn = Button(
        subject,
        text="📊 View Attendance",
        command=calculate_attendance,
        font=("Helvetica", 14, "bold"),
        bg="#27ae60",
        fg="white",
        activebackground="#2ecc71",
        padx=15,
        pady=10,
        relief=RAISED
    )
    fill_btn.place(x=160, y=180)

    # Check Sheets Button
    attf_btn = Button(
        subject,
        text="📁 Check Sheets",
        command=Attf,
        font=("Helvetica", 14, "bold"),
        bg="#2980b9",
        fg="white",
        activebackground="#3498db",
        padx=15,
        pady=10,
        relief=RAISED
    )
    attf_btn.place(x=340, y=180)

    subject.mainloop()
