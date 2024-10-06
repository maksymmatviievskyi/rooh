import numpy as np
import pickle
import cv2
from analyzer import ExerciseAnalyzer
import os

class PushupsAnalyzer(ExerciseAnalyzer):
    def __init__(self):
        super().__init__()
        self.threshold_arc_spine = 20

    def is_arched_back(self, hip, knee, shoulder):
        angle = self.calculate_angle(knee, hip, hip, shoulder)
        if angle <  self.threshold_arc_spine: return False
        return True
    
    def analyze_exercise(self, mp_pose, skeleton, X, current_stage, frame, counter=[0]):
        file_path = os.path.join(os.path.dirname(__file__), "pushups.pkl")
        with open(file_path, 'rb') as f:
            self.model = pickle.load(f)
        self.feedback.clear()
        self.detection = self.model.predict(X.values)[0]

        left_hip = np.array([skeleton[mp_pose.PoseLandmark.LEFT_HIP].x, skeleton[mp_pose.PoseLandmark.LEFT_HIP].y])
        left_knee = np.array([skeleton[mp_pose.PoseLandmark.LEFT_KNEE].x, skeleton[mp_pose.PoseLandmark.LEFT_KNEE].y])
        left_shoulder = np.array([skeleton[mp_pose.PoseLandmark.LEFT_SHOULDER].x, skeleton[mp_pose.PoseLandmark.LEFT_SHOULDER].y])

        image_height, image_width, _ = frame.shape
        cx, cy = int(left_knee[0] * image_width), int(left_knee[1] * image_height)
        cv2.putText(frame, str(self.calculate_angle(left_knee, left_hip, left_hip, left_shoulder)), (cx + 10,cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA) 
        

        if self.is_arched_back(left_hip, left_knee, left_shoulder):
            self.feedback.append('Straighten your body')
        if self.detection == 'down':
            self.current_stage = "down"
        elif self.current_stage == 'down' and self.detection == "up":
            self.current_stage = "up"
            counter[0] += 1
        if counter[0] >= self.reps: 
            counter[0] = 0
            self.finished = True
        if self.finished:
            return  self.feedback, self.reps, self.detection, current_stage, self.finished
        return self.feedback, counter[0], self.detection, current_stage, self.finished
    
Pushups = PushupsAnalyzer()