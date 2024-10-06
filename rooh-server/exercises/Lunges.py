import numpy as np
import pickle
import cv2
from analyzer import ExerciseAnalyzer
import os

class LungesAnalyzer(ExerciseAnalyzer):
    def __init__(self):
        super().__init__()
        self.threshold_lower_straight_angle = 90
        self.threshold_upper_straight_angle = 105

    def is_straight(self, hip, knee, ankle):
        angle = self.calculate_angle(hip, knee, knee, ankle)
        return self.threshold_lower_straight_angle < angle < self.threshold_upper_straight_angle

    def analyze_exercise(self, mp_pose, skeleton, X, current_stage, frame, counter=[0]):
        file_path = os.path.join(os.path.dirname(__file__), "lunges.pkl")
        with open(file_path, 'rb') as f:
            self.model = pickle.load(f)
        self.feedback.clear()
        self.detection = self.model.predict(X.values)[0]

        left_hip = np.array([skeleton[mp_pose.PoseLandmark.LEFT_HIP].x, skeleton[mp_pose.PoseLandmark.LEFT_HIP].y])
        left_knee = np.array([skeleton[mp_pose.PoseLandmark.LEFT_KNEE].x, skeleton[mp_pose.PoseLandmark.LEFT_KNEE].y])
        left_ankle = np.array([skeleton[mp_pose.PoseLandmark.LEFT_ANKLE].x, skeleton[mp_pose.PoseLandmark.LEFT_ANKLE].y])

        right_hip = np.array([skeleton[mp_pose.PoseLandmark.RIGHT_HIP].x, skeleton[mp_pose.PoseLandmark.RIGHT_HIP].y])
        right_knee = np.array([skeleton[mp_pose.PoseLandmark.RIGHT_KNEE].x, skeleton[mp_pose.PoseLandmark.RIGHT_KNEE].y])
        right_ankle = np.array([skeleton[mp_pose.PoseLandmark.RIGHT_ANKLE].x, skeleton[mp_pose.PoseLandmark.RIGHT_ANKLE].y])
            
        image_height, image_width, _ = frame.shape
        cx, cy = int(left_knee[0] * image_width), int(left_knee[1] * image_height)
        cv2.putText(frame, str(self.calculate_angle(left_hip, left_knee, left_knee, left_ankle)), (cx + 10,cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA) 
        cx, cy = int(right_knee[0] * image_width), int(right_knee[1] * image_height)
        cv2.putText(frame, str(self.calculate_angle(right_hip, right_knee, right_knee, right_ankle)), (cx + 10,cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA) 
        
        self.detection = self.model.predict(X.values)[0]
        if self.detection == 'down':
            self.current_stage = "down"
            if not self.is_straight(left_hip, left_knee, left_ankle):
               self.feedback.append('Your left leg should be straight')
            if not self.is_straight(right_hip, right_knee, right_ankle):
               self.feedback.append('Your right leg should be straight')
        elif self.current_stage == 'down' and self.detection == "up":
            self.current_stage = "up"
            counter[0] += 1
        if counter[0] >= self.reps: 
            counter[0] = 0
            self.finished = True
        if self.finished:
            return self.feedback, self.reps, self.detection, current_stage, self.finished
        return self.feedback, counter[0], self.detection, current_stage, self.finished

Lunges = LungesAnalyzer()