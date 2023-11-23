# Face Recognition 

This is a simple graphical user interface (GUI) for running face recognition scripts. The GUI is built using Tkinter in Python.It usage four backend python files to process.

## Requirements

- Python 3.x
- Tkinter (usually included with Python installation)

## Usage

1. Clone the repository or download the script files.
2. Run the main script `face_recognition_gui.py`.

## Scripts Included

### 1. Detect Faces From A Video File

Script Path: `Detect_face_frm_video_file_save_csv.py`

**Usage:**
- Enter the path to the known face directory (PNG or JPG only).
- Enter the video file path.
- Enter the path to store the CSV file.

### 2. Detect Faces From Webcam

Script Path: `detect_face_frm_webcam_save_csv.py`

**Usage:**
- Enter the path to the known faces directory (PNG or JPG only).
- Enter the path to store the CSV file.

### 3. Capture Image From Video

Script Path: `capture_img_frm_video.py`

**Usage:**
- Enter the video file path.
- Enter the directory where images are to be saved.
- Enter faces/images per second to save.

### 4. Capture Image From Webcam

Script Path: `capture_img_frm_webCam.py`

**Usage:**
- Enter the directory where images are to be saved.
- Enter faces/images per second to save.

## Notes

- Make sure to provide all the required details before running a script.
- Running a script may disable buttons for other scripts until completion.



