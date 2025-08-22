import tkinter as tk
from tkinter import *
import os, cv2, shutil, csv, numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel\Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails\studentdetails.csv"
attendance_path = "Attendance"

def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        if sub == "":
            text_to_speech("Please enter the subject name!!!")
            return

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            try:
                recognizer.read(trainimagelabel_path)
            except:
                e = "Model not found, please train model"
                Notifica.configure(text=e, bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
                Notifica.place(x=20, y=250)
                text_to_speech(e)
                return

            facecasCade = cv2.CascadeClassifier(haarcasecade_path)
            df = pd.read_csv(studentdetail_path)
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ["Enrollment", "Name"]
            attendance = pd.DataFrame(columns=col_names)
            end_time = time.time() + 20

            while time.time() < end_time:
                ret, im = cam.read()
                if not ret:
                    continue

                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = facecasCade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    if conf < 70:
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                        aa = df.loc[df["Enrollment"] == Id]["Name"].values
                        tt = str(Id) + "-" + str(aa[0])
                        attendance.loc[len(attendance)] = [Id, aa[0]]
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 4)
                        cv2.putText(im, tt, (x + h, y), font, 1, (255, 255, 0), 4)
                    else:
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 4)
                        cv2.putText(im, "Unknown", (x + h, y), font, 1, (0, 0, 255), 4)

                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                cv2.imshow("Filling Attendance...", im)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            Hour, Minute, Second = timeStamp.split(":")

            path = os.path.join(attendance_path, sub)
            if not os.path.exists(path):
                os.makedirs(path)

            fileName = f"{path}/{sub}_{date}_{Hour}-{Minute}-{Second}.csv"
            attendance[date] = 1
            attendance.to_csv(fileName, index=False)

            m = f"Attendance Filled Successfully for {sub}"
            Notifica.configure(text=m, bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
            text_to_speech(m)
            Notifica.place(x=20, y=250)

            cam.release()
            cv2.destroyAllWindows()
            time.sleep(3)  # Add delay to show success message

            root = tk.Tk()
            root.title("Attendance of " + sub)
            root.configure(background="black")

            with open(fileName, newline="") as file:
                reader = csv.reader(file)
                for r, col in enumerate(reader):
                    for c, row in enumerate(col):
                        label = tk.Label(root, text=row, width=10, height=1, fg="yellow", font=("times", 15, "bold"), bg="black", relief=tk.RIDGE)
                        label.grid(row=r, column=c)
            root.mainloop()

        except Exception as e:
            print(f"Error: {e}")
            text_to_speech("No Face found for attendance")
            cv2.destroyAllWindows()

    def Attf():
        sub = tx.get()
        if sub:
            os.startfile(os.path.join(attendance_path, sub))
        else:
            text_to_speech("Please enter the subject name!!!")

    subject = Tk()
    subject.title("Subject Attendance")
    subject.geometry("600x350")
    subject.resizable(False, False)
    subject.configure(background="#1f1f2e")

    Label(subject, text="📝 Enter Subject Name", bg="#1f1f2e", fg="#00ffd5", font=("Helvetica", 26, "bold"), pady=20).pack()
    Label(subject, text="Subject:", bg="#1f1f2e", fg="#ffcc00", font=("Helvetica", 18), padx=10, pady=10).place(x=80, y=110)

    global tx, Notifica
    tx = Entry(subject, width=20, bd=3, bg="#2c3e50", fg="#ecf0f1", font=("Helvetica", 22, "bold"), justify="center", insertbackground="white")
    tx.place(x=180, y=110)

    Button(subject, text="✅ Fill Attendance", command=FillAttendance, bd=0, font=("Helvetica", 14, "bold"), bg="#27ae60", fg="white", activebackground="#2ecc71", padx=15, pady=10, relief=RAISED).place(x=180, y=180)
    Button(subject, text="📁 Check Sheets", command=Attf, bd=0, font=("Helvetica", 14, "bold"), bg="#2980b9", fg="white", activebackground="#3498db", padx=15, pady=10, relief=RAISED).place(x=340, y=180)

    Notifica = Label(subject, text="", bg="#1f1f2e", fg="#f39c12", font=("Helvetica", 14, "bold"), wraplength=500, justify="center")
    Notifica.place(x=50, y=260)

    subject.mainloop()
