import os
import cv2
import numpy as np
import pickle
import streamlit as st
def capture_face(name):
    # Initialize the face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Create a directory if it doesn't exist to store individual data
    if name:
        if not os.path.exists('data/' + name):
            os.makedirs('data/' + name)

        # Counter for images
        i = 0

        # List to store faces data
        faces_data = []

        # Start capturing video from webcam
        cap = cv2.VideoCapture(0)

        # Initialize an empty numpy array for storing the frame data
        frame_data = np.zeros((300, 300, 3), dtype=np.uint8)

        # Create a placeholder for displaying the camera frame
        frame_placeholder = st.empty()

        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                crop_img = frame[y:y + h, x:x + w, :]
                resized_img = cv2.resize(crop_img, (50, 50))

                if len(faces_data) < 5:
                    faces_data.append(resized_img)
                i += 1

            # Update the frame data
            frame_data = frame.copy()

            # Display the frame in the Streamlit widget
            frame_placeholder.image(frame_data, channels="BGR", use_column_width=True)

            # Break the loop if 5 images are captured
            if len(faces_data) == 5:
                break

        # Release the video capture object and destroy OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        # Save all the face images of the person in a single pickle file
        if not os.path.exists('data/' + name + '/'):
            os.makedirs('data/' + name + '/')

        with open('data/' + name + '/' + name + '_faces.pkl', 'wb') as f:
            pickle.dump(faces_data, f)

        # Update names pickle file
        if 'names.pkl' not in os.listdir('data/'):
            names = [name]
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)
        else:
            with open('data/names.pkl', 'rb') as f:
                names = pickle.load(f)
            names.append(name)
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)

        # Inform the user that the images have been captured
        st.success("Photos have been captured successfully!")
