import os
import cv2
import numpy as np
import pickle
from analyzer import ExerciseAnalyzer

class SquatsAnalyzer(ExerciseAnalyzer):
    def __init__(self):
        super().__init__()
        self.threshold_lower_straight_angle = 90
        self.threshold_upper_straight_angle = 105

    def is_straight(self, knee, ankle):
            angle = self.calculate_angle(np.array([1,0]), np.array([0,0]), knee, ankle)
            return self.threshold_lower_straight_angle < angle < self.threshold_upper_straight_angle
    
    def analyze_exercise(self, mp_pose, skeleton, X, current_stage, frame, counter=[0]):
        file_path = os.path.join(os.path.dirname(__file__), "squats.pkl")
        with open(file_path, 'rb') as f:
            self.model = pickle.load(f)
        # self.detection = detection
        self.feedback.clear()
        self.detection = self.model.predict(X.values)[0]

        left_knee = np.array([skeleton[mp_pose.PoseLandmark.LEFT_KNEE].x, skeleton[mp_pose.PoseLandmark.LEFT_KNEE].y])
        left_ankle = np.array([skeleton[mp_pose.PoseLandmark.LEFT_ANKLE].x, skeleton[mp_pose.PoseLandmark.LEFT_ANKLE].y])

        image_height, image_width, _ = frame.shape
        cx, cy = int(left_knee[0] * image_width), int(left_knee[1] * image_height)
        cv2.putText(frame, str(self.calculate_angle(np.array([1,0]), np.array([0,0]),left_knee, left_ankle)), (cx + 10,cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA) 
        
        if self.detection == 'down':
            if not self.is_straight( left_knee, left_ankle):
                self.feedback.append('Your legs should be straight')
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

Squats = SquatsAnalyzer()
