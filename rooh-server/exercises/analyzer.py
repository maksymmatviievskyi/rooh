import numpy as np

class ExerciseAnalyzer:
    def __init__(self):
        self.reps = 10
        self.current_stage = None
        self.feedback = []
        self.finished = False
        self.detection = ""

    @staticmethod
    def calculate_angle(a, b, c, d):
        ba = a - b
        cd = c - d
        cosine_angle = np.dot(ba, cd) / (np.linalg.norm(ba) * np.linalg.norm(cd))
        angle = np.degrees(np.arccos(cosine_angle))
        if angle > 180.0:
            angle = 360 - angle
        return round(angle)

    def analyze_exercise(self):
        raise NotImplementedError("Subclasses must implement analyze_exercise method.")
