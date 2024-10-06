from aiortc import MediaStreamTrack
import mediapipe as mp
from mediapipe.python.solutions.pose import POSE_CONNECTIONS
import cv2
import numpy as np
import pandas as pd
from utils import loadModule
from av import VideoFrame
import json

mp_pose = mp.solutions.pose

class Process(MediaStreamTrack):
    kind = "video"
    def __init__(self, track, ws, workoutList):
        super().__init__()
        self.track = track
        self.ws = ws
        self.workoutList = workoutList
        self.pose_estimator = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.exerciseIndex = 0
        self.exercise = loadModule("exercises",self.workoutList[0])
        self.result = None
        self.current_stage = ""
        self._state = {
            "detection": [],
            "prob": [],
            'detected': False,
            "feedback": [],
            "count": 0,
            "time": 0,
            "finished": False,
            'workoutDuration': 0,
            'exerciseDuration': []
        }

    async def recv(self):
        input = await self.track.recv()
        try:
            output = input.to_ndarray(format="bgr24")
            #Flip and optimizing color space for mediapipe
            output = cv2.cvtColor(cv2.flip(output,1), cv2.COLOR_BGR2RGB)
            output.flags.writeable = False
            self.result = self.pose_estimator.process(output)
            output.flags.writeable = True
            output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)

            # Draw the pose on the image
            if self.result.pose_landmarks:
                keypoints = [(int(lm.x * output.shape[1]), int(lm.y * output.shape[0])) for lm in self.result.pose_landmarks.landmark]
                mp.solutions.drawing_utils.draw_landmarks(
                    output, self.result.pose_landmarks, POSE_CONNECTIONS
                )
                user_visible = self.is_user_visible(keypoints, output.shape[1], output.shape[0])
                if user_visible:
                    self.analyze(output)
                else:
                    self.state["feedback"] = ['Fit into frame, please']

            await self.ws.send_str(json.dumps(self.state))

            # Rebuild a VideoFrame, preserving timing information
            output = VideoFrame.from_ndarray(output, format="bgr24")
            output.pts = input.pts
            output.time_base = input.time_base
            return output
        except Exception as error:
            print("Processing error:", error)
            return input
        
    def analyze(self, frame):
        row = np.array([[res.x,res.y, res.z, res.visibility] for res in self.result.pose_landmarks.landmark]).flatten()
        X = pd.DataFrame([row])
        correctionResponse, self.state["count"], self.state['detection'], self.current_stage, finished = self.exercise.analyze_exercise(mp_pose, self.result.pose_landmarks.landmark, X, self.current_stage, frame)
        
        if finished: 
            if (self.exerciseIndex+1) == len(self.workoutList):
                self.state["finished"] = True
            else:
                self.exerciseIndex += 1
                self.exercise = loadModule("exercises", self.workoutList[self.exerciseIndex])
        if self.state["feedback"] != correctionResponse:
            if correctionResponse: self.state["feedback"] = correctionResponse
            else: self.state["feedback"].clear()
    
    @staticmethod
    def is_user_visible(keypoints, frame_width, frame_height):
        for kp in keypoints:
            x, y = kp[0], kp[1]
            if x < 0 or x >= frame_width or y < 0 or y >= frame_height:
                return False
        return True

    @property
    def state(self):
        return self._state
    
    @state.setter
    async def state(self, key, value):
        self._state[key] = value