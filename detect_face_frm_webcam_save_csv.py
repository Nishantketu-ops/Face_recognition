import cv2
import os
import pandas as pd
import time
from datetime import datetime
# Function to load images and encode faces
def load_images_and_encode(directory):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = cv2.imread(os.path.join(directory, filename))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Use a simple encoding method, e.g., average pixel values
            face_encoding = gray.mean(axis=0).mean(axis=0)

            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])

    return known_face_encodings, known_face_names

# Function to recognize faces from webcam feed
def recognize_faces_from_webcam(known_face_encodings, known_face_names, output_csv):
    cap = cv2.VideoCapture(0)  # Use the default camera (change to a different index if needed)

    recognized_faces = []

    frame_count = 0

    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Use the Haar Cascade Classifier for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_roi = gray_frame[y:y + h, x:x + w]

            # Use the same encoding method as in the load_images_and_encode function
            face_encoding = face_roi.mean(axis=0).mean(axis=0)

            if known_face_encodings:
                # Compare distances to recognize faces
                distances = [((enc - face_encoding) ** 2).sum() for enc in known_face_encodings]
                min_distance_index = distances.index(min(distances))

                # You can set a threshold for distance to determine if a face is recognized
                if min(distances) < 1000:  # Adjust the threshold accordingly
                    name = known_face_names[min_distance_index]
                    elapsed_time = time.time() - start_time
                    formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                    recognized_faces.append({
                        'Name': name,
                        'Present_IN_Video_AT_Time': formatted_time
                    })
                else:
                    name = "Unknown"
            else:
                name = "No Known Faces"

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Put the name on the rectangle
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (x, y - 10), font, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the frame
        cv2.imshow('Webcam', frame)

        # Save results to CSV every 10 frames
        if frame_count % 10 == 0 and recognized_faces:
            # df = pd.DataFrame(recognized_faces)
            # df.to_csv(output_csv, index=False, mode='a', header=(frame_count == 10))
            save_to_csv(output_csv, recognized_faces, frame_count == 10)
        recognized_faces = []

        # Break the loop if the 'esc' key is pressed
        if cv2.waitKey(1) & 0xFF ==27:
            break

    cap.release()
    cv2.destroyAllWindows()
def save_to_csv(output_csv, data, header):
    # Get the current date and time
    current_datetime = datetime.now().strftime("%d_%m_%Y")
    
    # Extract the directory path and base filename from the output_csv
    output_dir, output_filename = os.path.split(output_csv)
    
    # Construct the new CSV filename with the recognized_faces_ prefix
    new_csv_filename = f"Recognized_faces_frm_Webcam_{current_datetime}.csv"
    
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


def detect_faces_from_webcam(known_faces_dir, output_csv):
    output_csv_folder=output_csv+"/"
    known_face_encodings, known_face_names = load_images_and_encode(known_faces_dir)
    recognize_faces_from_webcam(known_face_encodings, known_face_names, output_csv_folder)
    
    return f"CSV file saved at: {output_csv}"
    
if __name__ == "__main__":
    known_faces_dir = "D:/Python Projects/Face_recognition/Output_directory"
    output_csv = "D:/Python Projects/Face_recognition/Inputvideo"

    known_face_encodings, known_face_names = load_images_and_encode(known_faces_dir)
    recognize_faces_from_webcam(known_face_encodings, known_face_names, output_csv)
