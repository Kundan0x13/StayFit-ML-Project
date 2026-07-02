from streamlit_webrtc import VideoProcessorBase
import threading
import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from detectors.biceps_curl import BicepsCurlDetector
from detectors.squat import SquatDetector
from detectors.pushup import PushUpDetector
from detectors.shoulder_press import ShoulderPressDetector
from detectors.lunges import LungesDetector
from services.config import POSE_CONNECTIONS 

class VideoProcessorClass(VideoProcessorBase):
    def __init__(self):
        self._lock = threading.Lock()
        self._latest_metrics = None
        self._exercise_type = None
        
        model_path = os.path.join(os.getcwd(), "ml_models", "pose_landmarker_full.task")
        base_options = mp.tasks.BaseOptions(model_asset_path=model_path)
        
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            min_pose_detection_confidence=0.7,
            min_pose_landmark_confidence=0.7,
            output_segmentation_masks=False
        )
        
        # Create the PoseLandmarker object with the specified options
        self._landmarker = vision.PoseLandmarker.create_from_options(options)
        
        self._detectors = {
            "Biceps Curl": BicepsCurlDetector(),
            "Squats": SquatDetector(),
            "Push Ups": PushUpDetector(),
            "Lunges": LungesDetector(),
            "Shoulder Press": ShoulderPressDetector()
        }
        
        # Initialize the frame timestamp to 0
        self._frame_timestamps_ms = 0       # because Video mode
        

    def set_latest_metrics(self, metrics):
        with self._lock:
            self._latest_metrics = metrics.copy()

    def get_latest_metrics(self):
        with self._lock:
            return None if self._latest_metrics is None else self._latest_metrics.copy()
        
    def set_exercise(self, exercise_type):
        with self._lock:
            self._exercise_type = exercise_type

    def get_exercise(self):
        with self._lock:
            return self._exercise_type
        
    def _draw_skeleton(self, img, landmarks):
        h, w = img.shape[:2]        # dimensions of the image in pixels

        for start_idx, end_idx in POSE_CONNECTIONS:
            p1 = landmarks[start_idx]
            p2 = landmarks[end_idx]

            if p1.visibility > 0.7 and p2.visibility > 0.7:     # if both landmarks are visible, draw the line
                cv2.line(
                    img,
                    (int(p1.x * w), int(p1.y * h)),
                    (int(p2.x * w), int(p2.y * h)),
                    (0, 255, 0),        # green color in BGR format
                    8
                )
        
        for lm in landmarks:
            if lm.visibility > 0.7:
                cv2.circle(
                    img, 
                    (int(lm.x * w), int(lm.y * h)),
                    8,
                    (255, 0, 0),        # blue color in BGR format
                    -1
                )
                
    def _draw_no_pose_warnings(self, img):
        # putText is used to draw text on an image
        cv2.putText(
            img,
            "NO POSE DETECTED",         # text to be drawn
            (30, 50),                   # location of the text in the image (x, y)
            cv2.FONT_HERSHEY_SIMPLEX,   # font type
            1,                          # font scale (size of the text) 
            (0, 255, 0),                # color of the text in BGR format (green in this case)
            2,                          # thickness of the text
            cv2.LINE_AA,                # type of the line used to draw the text (anti-aliased line)
        )

        cv2.putText(
            img,
            "PLEASE FACE THE CAMERA",
            (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

