import cv2


class CameraStream:
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            raise RuntimeError(f"Не удалось открыть камеру с индексом {self.camera_index}")

    def read(self):
        success, frame = self.cap.read()
        if not success:
            return None
        return frame

    def release(self):
        if self.cap:
            self.cap.release()