import cv2
import mediapipe as mp
import csv
import os
import numpy as np
from matplotlib import pyplot as plt

#Writing labels into data.csv
def export_landmark(results, action):
    try:
        keypoints = np.array([[res.x,res.y,res.z,res.visibility] for res in results.pose_landmarks.landmark],dtype='object').flatten()
        keypoints = np.insert(keypoints,0, action)

        with open("PATH_TO_FILE", mode='a',newline='') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(keypoints)
    except Exception as e:
        print(e)

#Extracting Mediapipe utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.holistic

cap = cv2.VideoCapture('PATH_TO_FILE')

with mp_pose.Holistic(min_detection_confidence=.5,min_tracking_confidence=.5) as pose:
    while cap.isOpened():
        res, frame = cap.read()

        #flip and optimizing color space for mediapipe
        frame = cv2.cvtColor(cv2.flip(frame,1), cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = pose.process(frame)
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        #Listen to the keyboard
        k = cv2.waitKey(1)

        if k==117:
            export_landmark(results, "up")
        if k ==100:
            export_landmark(results, "down")
        
        cv2.imshow("Webcam Feed", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()