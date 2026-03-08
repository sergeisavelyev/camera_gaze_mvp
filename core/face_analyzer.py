from __future__ import annotations

import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceAnalyzer:
    """
    Ищет лицо через новый MediaPipe Tasks API
    и грубо определяет: смотрит человек в сторону камеры или нет.
    """

    LEFT_EYE_IDX = 33
    RIGHT_EYE_IDX = 263
    NOSE_TIP_IDX = 1

    def __init__(
        self,
        model_path: str,
        num_faces: int = 1,
        min_face_detection_confidence: float = 0.5,
        min_face_presence_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
        max_nose_offset_ratio: float = 0.20,
    ):
        self.model_path = model_path
        self.max_nose_offset_ratio = max_nose_offset_ratio

        base_options = python.BaseOptions(model_asset_path=self.model_path)

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_faces=num_faces,
            min_face_detection_confidence=min_face_detection_confidence,
            min_face_presence_confidence=min_face_presence_confidence,
            min_tracking_confidence=min_tracking_confidence,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
        )

        self.landmarker = vision.FaceLandmarker.create_from_options(options)
        self.frame_index = 0

    def analyze(self, frame):
        """
        Возвращает словарь:
        {
            "face_detected": bool,
            "looking": bool,
            "nose_offset_ratio": float | None,
            "points": dict | None
        }
        """
        self.frame_index += 1
        timestamp_ms = self.frame_index * 33  # грубо под ~30 FPS

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame,
        )

        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        if not result.face_landmarks:
            return {
                "face_detected": False,
                "looking": False,
                "nose_offset_ratio": None,
                "points": None,
            }

        face_landmarks = result.face_landmarks[0]
        h, w, _ = frame.shape

        left_eye = self._landmark_to_pixel(face_landmarks[self.LEFT_EYE_IDX], w, h)
        right_eye = self._landmark_to_pixel(face_landmarks[self.RIGHT_EYE_IDX], w, h)
        nose_tip = self._landmark_to_pixel(face_landmarks[self.NOSE_TIP_IDX], w, h)

        nose_offset_ratio = self._compute_nose_offset_ratio(left_eye, right_eye, nose_tip)
        looking = nose_offset_ratio is not None and nose_offset_ratio <= self.max_nose_offset_ratio

        return {
            "face_detected": True,
            "looking": looking,
            "nose_offset_ratio": nose_offset_ratio,
            "points": {
                "left_eye": left_eye,
                "right_eye": right_eye,
                "nose_tip": nose_tip,
            },
        }

    def _landmark_to_pixel(self, landmark, width: int, height: int):
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        return (x, y)

    def _compute_nose_offset_ratio(self, left_eye, right_eye, nose_tip):
        eye_line_width = abs(right_eye[0] - left_eye[0])
        if eye_line_width == 0:
            return None

        eye_center_x = (left_eye[0] + right_eye[0]) / 2
        nose_offset = abs(nose_tip[0] - eye_center_x)

        return nose_offset / eye_line_width

    def close(self):
        self.landmarker.close()