import cv2
import os
import pandas as pd
import time
from datetime import datetime

def load_images_and_encode(directory):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = cv2.imread(os.path.join(directory, filename))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_encoding = gray.mean(axis=0).mean(axis=0)

            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])

    return known_face_encodings, known_face_names

def recognize_faces_in_video(video_path, known_face_encodings, known_face_names, output_csv):
    cap = cv2.VideoCapture(video_path)

    recognized_faces = []
    frame_count = 0
    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_roi = gray_frame[y:y + h, x:x + w]
            face_encoding = face_roi.mean(axis=0).mean(axis=0)

            if known_face_encodings:
                distances = [((enc - face_encoding) ** 2).sum() for enc in known_face_encodings]
                min_distance_index = distances.index(min(distances))

                if min(distances) < 1000:
                    name = known_face_names[min_distance_index]
                    elapsed_time = time.time() - start_time
                    formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                    recognized_faces.append({
                        'Name': name,
                        'Present_IN_Video_AT_Time': formatted_time,
                        'Video_File_Path': os.path.abspath(video_path),
                        'Video_File_Name': os.path.basename(video_path)
                    })
                else:
                    name = "Unknown"
            else:
                name = "No Known Faces"

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (x, y - 10), font, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

        if frame_count % 10 == 0 and recognized_faces:
            save_to_csv(output_csv, recognized_faces, frame_count == 10)

        recognized_faces = []
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def save_to_csv(output_csv, data, header):
    # Get the current date and time
    current_datetime = datetime.now().strftime("%d_%m_%Y")
    
    # Extract the directory path and base filename from the output_csv
    output_dir, output_filename = os.path.split(output_csv)
    
    # Construct the new CSV filename with the recognized_faces_ prefix
    new_csv_filename = f"Recognized_faces_{current_datetime}.csv"
    
    # Create the new CSV file path by joining the output directory and the new CSV filename
    new_csv_path = os.path.join(output_dir, new_csv_filename)
    
    # If the new CSV file doesn't exist, create it with the data
    if not os.path.exists(new_csv_path):
        df = pd.DataFrame(data)
        df.to_csv(new_csv_path, index=False, mode='w', header=header)
    else:
        # If the new CSV file already exists, append the data to it
        df = pd.DataFrame(data)
        df.to_csv(new_csv_path, index=False, mode='a', header=False)

def recognize_faces_from_images_and_video(known_faces_dir, video_path, output_csv):
    output_csv_folder=output_csv+"/"
    known_face_encodings, known_face_names = load_images_and_encode(known_faces_dir)
    recognize_faces_in_video(video_path, known_face_encodings, known_face_names, output_csv_folder)
    
    return f"CSV file saved at: {output_csv}"

if __name__ == "__main__":
    known_faces_dir = "D:/Python Projects/Face_recognition/Output_directory"
    video_path = "D:/Python Projects/Face_recognition/Inputvideo/intro.mp4"
    
    # Define output CSV path
    output_csv = "D:/Python Projects/Face_recognition/Inputvideo"
    recognize_faces_from_images_and_video(known_faces_dir, video_path, output_csv)
