import cv2
from pathlib import Path


class VideoFileSource:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = None

        self.cap = self._open_video_with_fallback(self.video_path)

        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError(
                f"Не удалось открыть видео. Проверенные варианты: {self._candidate_paths(self.video_path)}"
            )

    def _candidate_paths(self, original_path: str):
        """
        Возвращает список возможных вариантов файла:
        .mov -> .mp4 -> .avi -> .mkv
        """
        path = Path(original_path)

        candidates = [
            path,
            path.with_suffix(".mp4"),
            path.with_suffix(".mov"),
            path.with_suffix(".avi"),
            path.with_suffix(".mkv"),
        ]

        return candidates

    def _open_video_with_fallback(self, original_path: str):
        candidates = self._candidate_paths(original_path)

        for candidate in candidates:
            if not candidate.exists():
                continue

            print(f"Пробуем открыть видео: {candidate}")

            cap = cv2.VideoCapture(str(candidate))

            if cap.isOpened():
                print(f"Видео успешно открыто: {candidate}")
                return cap

        return None

    def read(self):
        success, frame = self.cap.read()
        if not success:
            return None
        return frame

    def release(self):
        if self.cap:
            self.cap.release()