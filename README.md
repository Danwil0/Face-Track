# Face-Track

A face recognition attendance system I built as my final year project. It registers students with a webcam, trains a recogniser on their faces, then marks attendance automatically for each subject.

## How it works

1. **Register:** enter an enrolment number and name, and the app captures face images from the webcam (`takeImage.py`)
2. **Train:** an LBPH face recogniser is trained on the captured images (`trainImage.py`)
3. **Take attendance:** pick a subject, the webcam detects faces with a Haar cascade, recognises each student and saves attendance to a dated CSV (`automaticAttedance.py`)
4. **View:** open the attendance sheet for any subject (`show_attendance.py`)

There is also a manual entry option (`takemanually.py`) and voice feedback through `pyttsx3`.

## Run it

```bash
git clone https://github.com/Danwil0/Face-Track.git
cd Face-Track
pip install -r requirements.txt
python attendance.py
```

You need a webcam. Tested on Windows.

**Stack:** Python, OpenCV (Haar cascade + LBPH), Tkinter, Pandas, Pillow
