from config import (
    CAMERA_INDEX,
    WINDOW_NAME,
    MODEL_PATH,
    NUM_FACES,
    MIN_FACE_DETECTION_CONFIDENCE,
    MIN_FACE_PRESENCE_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    FRAMES_TO_CONFIRM_LOOKING,
    FRAMES_TO_CONFIRM_NOT_LOOKING,
    MAX_NOSE_OFFSET_RATIO,
)

from core.camera_stream import CameraStream
from core.face_analyzer import FaceAnalyzer
from core.contact_counter import ContactCounter
from core.app import App


def main():
    camera_stream = CameraStream(camera_index=CAMERA_INDEX)

    face_analyzer = FaceAnalyzer(
        model_path=MODEL_PATH,
        num_faces=NUM_FACES,
        min_face_detection_confidence=MIN_FACE_DETECTION_CONFIDENCE,
        min_face_presence_confidence=MIN_FACE_PRESENCE_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        max_nose_offset_ratio=MAX_NOSE_OFFSET_RATIO,
    )

    contact_counter = ContactCounter(
        frames_to_confirm_looking=FRAMES_TO_CONFIRM_LOOKING,
        frames_to_confirm_not_looking=FRAMES_TO_CONFIRM_NOT_LOOKING,
    )

    app = App(
        camera_stream=camera_stream,
        face_analyzer=face_analyzer,
        contact_counter=contact_counter,
    )

    app.run()


if __name__ == "__main__":
    main()