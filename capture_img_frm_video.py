#  To capture Distinct faces from a video file and save in a directory.

import cv2
import os
import numpy as np
import time

def calculate_histogram(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculate the histogram of the image
    hist = cv2.calcHist([hsv_image], [0, 1], None, [180, 256], [0, 180, 0, 256])
    
    # Normalize the histogram
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    
    return hist.flatten()

def are_histograms_similar(hist1, hist2, threshold=8):
    # Compare histograms using correlation
    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    
    # Return True if correlation is above the threshold, indicating similarity
    return correlation > threshold

def detect_faces_and_save(video_path, output_directory,faces_per_second):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    cap = cv2.VideoCapture(video_path)

    face_count = 0
    saved_faces = []

    start_time = time.time()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        current_time = time.time()

        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]

            # Calculate histogram of the face
            hist = calculate_histogram(face_roi)

            # Check if the face is similar to any saved face
            similar_face = False
            for saved_hist in saved_faces:
                if are_histograms_similar(hist, saved_hist):
                    similar_face = True
                    break

            if not similar_face and (current_time - start_time) >= 1 / faces_per_second:
                # Save the face image to the output directory
                face_filename = os.path.join(output_directory, f"face_{face_count}.jpg")
                cv2.imwrite(face_filename, face_roi)
                face_count += 1

                # Save the histogram of the face
                saved_faces.append(hist)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def capture_img_frm_video(video_path, output_directory,faces_per_second):
    faces_per_second=int(faces_per_second)
    detect_faces_and_save(video_path,output_directory, faces_per_second)
    return "Images saved in folder , Please find it"

# if __name__ == "__main__":
#     video_path = "D:/Python Projects/Face_recognition/Inputvideo/intro.mp4"
#     output_directory = "Output_directory"

#     detect_faces_and_save(video_path, output_directory,faces_per_second=1)

