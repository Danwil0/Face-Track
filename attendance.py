import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance


MAIN_BG = "#f0f9ff"  # Light blue background
HEADER_BG = "#4dabf7"  # Bright blue header
ACCENT_COLOR = "#339af0"  # Accent blue
TEXT_COLOR = "#1864ab"  # Dark blue text
BUTTON_BG = "#339af0"  # Button background
BUTTON_FG = "white"  # Button text
HOVER_COLOR = "#1c7ed6"  # Button hover color
INPUT_BG = "white"  # Input field background
INPUT_FG = "#495057"  # Input text color
NOTIFICATION_BG = "#e9ecef"  # Light gray for notifications


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "./TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

window = Tk()
window.title("FACE TRACK - Smart Attendance Management System")
window.geometry("1280x720")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background=MAIN_BG)


# Custom hover effect function for buttons
def on_enter(e):
    e.widget['background'] = HOVER_COLOR


def on_leave(e):
    e.widget['background'] = BUTTON_BG


# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.title("Warning!!")
    sc1.configure(background=HEADER_BG)
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Matric No & Name required!!!",
        fg="white",
        bg=HEADER_BG,
        font=("Poppins", 16, "bold"),
    ).pack()
    error_btn = tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="white",
        bg=BUTTON_BG,
        width=9,
        height=1,
        activebackground=HOVER_COLOR,
        font=("Poppins", 16, "bold"),
    )
    error_btn.place(x=150, y=50)
    error_btn.bind("<Enter>", on_enter)
    error_btn.bind("<Leave>", on_leave)


def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


# Create a header frame with gradient effect
header_frame = tk.Frame(window, bg=HEADER_BG, height=80)
header_frame.pack(fill=X)

# Load and display logo
try:
    logo = Image.open("UI_Image/0001.png")
    logo = logo.resize((60, 60), Image.LANCZOS)
    logo1 = ImageTk.PhotoImage(logo)
    l1 = tk.Label(header_frame, image=logo1, bg=HEADER_BG)
    l1.place(x=20, y=10)
except:
    # If logo not found, use text instead
    print("Logo image not found, using text instead")

# Title in header
titl = tk.Label(
    header_frame,
    text="FACE TRACK",
    bg=HEADER_BG,
    fg="white",
    font=("Poppins", 32, "bold"),
)
titl.place(x=100, y=15)

# Welcome message
welcome_frame = tk.Frame(window, bg=MAIN_BG)
welcome_frame.pack(fill=X, pady=20)

a = tk.Label(
    welcome_frame,
    text="Smart Attendance Management System",
    bg=MAIN_BG,
    fg=TEXT_COLOR,
    font=("Poppins", 28, "bold"),
)
a.pack()

subtitle = tk.Label(
    welcome_frame,
    text="Fast, Accurate, and Secure Face Recognition",
    bg=MAIN_BG,
    fg=ACCENT_COLOR,
    font=("Poppins", 16),
)
subtitle.pack(pady=10)

# Main content frame
content_frame = tk.Frame(window, bg=MAIN_BG)
content_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

# Create three feature frames with icons and descriptions
# 1. Register Frame
register_frame = tk.Frame(content_frame, bg=MAIN_BG, bd=2, relief=RIDGE)
register_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

try:
    ri = Image.open("UI_Image/register.png")
    r = ImageTk.PhotoImage(ri)
    label1 = Label(register_frame, image=r, bg=MAIN_BG)
    label1.image = r
    label1.pack(pady=10)
except:
    # Fallback if image not found
    placeholder1 = tk.Label(register_frame, text="📝", font=("Arial", 80), bg=MAIN_BG, fg=ACCENT_COLOR)
    placeholder1.pack(pady=10)

reg_title = tk.Label(
    register_frame,
    text="Student Registration",
    bg=MAIN_BG,
    fg=TEXT_COLOR,
    font=("Poppins", 16, "bold"),
)
reg_title.pack(pady=5)

reg_desc = tk.Label(
    register_frame,
    text="Register new students with\ntheir face data for recognition",
    bg=MAIN_BG,
    fg=TEXT_COLOR,
    font=("Poppins", 12),
    justify=CENTER,
)
reg_desc.pack(pady=10)

# 2. Verify Frame
verify_frame = tk.Frame(content_frame, bg=MAIN_BG, bd=2, relief=RIDGE)
verify_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

try:
    vi = Image.open("UI_Image/verifyy.png")
    v = ImageTk.PhotoImage(vi)
    label3 = Label(verify_frame, image=v, bg=MAIN_BG)
    label3.image = v
    label3.pack(pady=10)
except:
    # Fallback if image not found
    placeholder2 = tk.Label(verify_frame, text="✓", font=("Arial", 80), bg=MAIN_BG, fg=ACCENT_COLOR)
    placeholder2.pack(pady=10)

verify_title = tk.Label(
    verify_frame,
    text="Take Attendance",
    bg=MAIN_BG,
    fg=TEXT_COLOR,
    font=("Poppins", 16, "bold"),
)
verify_title.pack(pady=5)

verify_desc = tk.Label(
    verify_frame,
    text="Automatically mark attendance\nusing face recognition",
    bg=MAIN_BG,
    fg=TEXT_COLOR,
    font=("Poppins", 12),
    justify=CENTER,
)
verify_desc.pack(pady=10)

# 3. Attendance Frame
attend_frame = tk.Frame(content_frame, bg=MAIN_BG, bd=2, relief=RIDGE)
attend_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

try:
    ai = Image.open("UI_Image/attendance.png")
    a = ImageTk.PhotoImage(ai)
    label2 = Label(attend_frame, image=a, bg=MAIN_BG)
    label2.image = a
    label2.pack(pady=10)
except:
    # Fallback if image not found
    placeholder3 = tk.Label(attend_frame, text="📊", font=("Arial", 80), bg=MAIN_BG, fg=ACCENT_COLOR)
    placeholder3.pack(pady=10)

attend_title = tk.Label(
    attend_frame,
    text="View Records",
    bg=MAIN_BG,
    fg=TEXT_COLOR,
    font=("Poppins", 16, "bold"),
)
attend_title.pack(pady=5)

attend_desc = tk.Label(
    attend_frame,
    text="Access and analyze\nattendance records",
    bg=MAIN_BG,
    fg=TEXT_COLOR,
    font=("Poppins", 12),
    justify=CENTER,
)
attend_desc.pack(pady=10)

# Configure grid weights for proper spacing
content_frame.grid_columnconfigure(0, weight=1)
content_frame.grid_columnconfigure(1, weight=1)
content_frame.grid_columnconfigure(2, weight=1)
content_frame.grid_rowconfigure(0, weight=1)

# Button frame
button_frame = tk.Frame(window, bg=MAIN_BG)
button_frame.pack(fill=X, pady=20)


def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Register New Student")
    ImageUI.geometry("780x480")
    ImageUI.configure(background=MAIN_BG)
    ImageUI.resizable(0, 0)

    # Header frame
    img_header = tk.Frame(ImageUI, bg=HEADER_BG, height=80)
    img_header.pack(fill=X)

    # Title in header
    titl = tk.Label(
        img_header,
        text="Student Registration",
        bg=HEADER_BG,
        fg="white",
        font=("Poppins", 24, "bold"),
    )
    titl.place(x=20, y=20)

    # Content frame
    img_content = tk.Frame(ImageUI, bg=MAIN_BG)
    img_content.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Subtitle
    a = tk.Label(
        img_content,
        text="Enter Student Details",
        bg=MAIN_BG,
        fg=TEXT_COLOR,
        font=("Poppins", 18, "bold"),
    )
    a.grid(row=0, column=0, columnspan=2, pady=20)

    lbl1 = tk.Label(
        img_content,
        text="Matric No:",
        bg=MAIN_BG,
        fg=TEXT_COLOR,
        font=("Poppins", 14),
    )
    lbl1.grid(row=1, column=0, sticky=W, pady=10, padx=10)

    txt1 = tk.Entry(
        img_content,
        width=25,
        bd=2,
        validate="key",
        bg=INPUT_BG,
        fg=INPUT_FG,
        font=("Poppins", 14),
    )
    txt1.grid(row=1, column=1, pady=10, padx=10, sticky=W)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        img_content,
        text="Full Name:",
        bg=MAIN_BG,
        fg=TEXT_COLOR,
        font=("Poppins", 14),
    )
    lbl2.grid(row=2, column=0, sticky=W, pady=10, padx=10)

    txt2 = tk.Entry(
        img_content,
        width=25,
        bd=2,
        bg=INPUT_BG,
        fg=INPUT_FG,
        font=("Poppins", 14),
    )
    txt2.grid(row=2, column=1, pady=10, padx=10, sticky=W)

    # Notification
    lbl3 = tk.Label(
        img_content,
        text="Status:",
        bg=MAIN_BG,
        fg=TEXT_COLOR,
        font=("Poppins", 14),
    )
    lbl3.grid(row=3, column=0, sticky=W, pady=10, padx=10)

    message = tk.Label(
        img_content,
        text="",
        width=30,
        height=2,
        bd=2,
        relief=RIDGE,
        bg=NOTIFICATION_BG,
        fg=TEXT_COLOR,
        font=("Poppins", 12),
    )
    message.grid(row=3, column=1, pady=10, padx=10, sticky=W)

    # Button Frame
    btn_frame = tk.Frame(img_content, bg=MAIN_BG)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # Take Image button
    takeImg = tk.Button(
        btn_frame,
        text="Capture Images",
        command=take_image,
        bd=0,
        font=("Poppins", 14, "bold"),
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        height=2,
        width=15,
        relief=FLAT,
    )
    takeImg.grid(row=0, column=0, padx=10)
    takeImg.bind("<Enter>", on_enter)
    takeImg.bind("<Leave>", on_leave)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # Train Image button
    trainImg = tk.Button(
        btn_frame,
        text="Train Images",
        command=train_image,
        bd=0,
        font=("Poppins", 14, "bold"),
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        height=2,
        width=15,
        relief=FLAT,
    )
    trainImg.grid(row=0, column=1, padx=10)
    trainImg.bind("<Enter>", on_enter)
    trainImg.bind("<Leave>", on_leave)

    # Configure grid
    img_content.grid_columnconfigure(1, weight=1)


register_btn = tk.Button(
    button_frame,
    text="Register New Student",
    command=TakeImageUI,
    bd=0,
    font=("Poppins", 14, "bold"),
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    height=2,
    width=18,
    relief=FLAT,
)
register_btn.grid(row=0, column=0, padx=20)
register_btn.bind("<Enter>", on_enter)
register_btn.bind("<Leave>", on_leave)


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


take_attend_btn = tk.Button(
    button_frame,
    text="Take Attendance",
    command=automatic_attedance,
    bd=0,
    font=("Poppins", 14, "bold"),
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    height=2,
    width=18,
    relief=FLAT,
)
take_attend_btn.grid(row=0, column=1, padx=20)
take_attend_btn.bind("<Enter>", on_enter)
take_attend_btn.bind("<Leave>", on_leave)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


view_attend_btn = tk.Button(
    button_frame,
    text="View Attendance",
    command=view_attendance,
    bd=0,
    font=("Poppins", 14, "bold"),
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    height=2,
    width=18,
    relief=FLAT,
)
view_attend_btn.grid(row=0, column=2, padx=20)
view_attend_btn.bind("<Enter>", on_enter)
view_attend_btn.bind("<Leave>", on_leave)

# Configure grid weights for button frame
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

# Footer with exit button
footer_frame = tk.Frame(window, bg=MAIN_BG, height=80)
footer_frame.pack(fill=X, side=BOTTOM, pady=10)

exit_btn = tk.Button(
    footer_frame,
    text="EXIT",
    command=quit,
    bd=0,
    font=("Poppins", 14, "bold"),
    bg="#ff6b6b",  # Red color for exit button
    fg="white",
    height=2,
    width=10,
    relief=FLAT,
)
exit_btn.pack(pady=10)


version_label = tk.Label(
    footer_frame,
    text="FACE TRACK v1.0 | Smart Attendance Management System",
    bg=MAIN_BG,
    fg=TEXT_COLOR,
    font=("Poppins", 10),
)
version_label.pack(side=BOTTOM, pady=5)

window.mainloop()