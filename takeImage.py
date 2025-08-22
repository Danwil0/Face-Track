import csv
import os
import cv2
import numpy as np
import pandas as pd
import datetime
import time

def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if not l1 or not l2:
        if not l1 and not l2:
            t = 'Please enter your Enrollment Number and Name.'
        elif not l1:
            t = 'Please enter your Enrollment Number.'
        else:
            t = 'Please enter your Name.'
        text_to_speech(t)
        return

    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            text_to_speech("Could not open camera")
            return

        detector = cv2.CascadeClassifier(haarcasecade_path)
        if detector.empty():
            text_to_speech("Failed to load Haar Cascade classifier")
            return

        directory = f"{l1}_{l2}"
        path = os.path.join(trainimage_path, directory)

        if os.path.exists(path):
            text_to_speech("Student data already exists")
            return

        os.makedirs(path, exist_ok=True)
        sampleNum = 0
        detection_interval = 5
        frame_count = 0

        while sampleNum < 50:
            ret, img = cam.read()
            if not ret:
                continue

            frame_count += 1
            if frame_count % detection_interval != 0:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                sampleNum += 1
                face_img = gray[y:y+h, x:x+w]
                img_name = f"{l2}_{l1}_{sampleNum}.jpg"
                cv2.imwrite(os.path.join(path, img_name), face_img)
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(img, f"Sample {sampleNum}/50", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("Capturing Face Images", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

        # Save student details
        details_file = os.path.join("StudentDetails", "studentdetails.csv")
        os.makedirs(os.path.dirname(details_file), exist_ok=True)
        with open(details_file, "a+", newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([l1, l2])

        res = f"Images Saved for ER No: {l1} Name: {l2}"
        message.configure(text=res)
        text_to_speech(res)

    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        text_to_speech(error_msg)
