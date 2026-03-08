import cv2

from config import WINDOW_NAME
from utils.drawing import draw_info, draw_points


class App:
    def __init__(self, camera_stream, face_analyzer, contact_counter):
        self.camera_stream = camera_stream
        self.face_analyzer = face_analyzer
        self.contact_counter = contact_counter

    def run(self):
        while True:
            frame = self.camera_stream.read()
            if frame is None:
                print("Не удалось получить кадр")
                break

            analysis_result = self.face_analyzer.analyze(frame)
            counter_result = self.contact_counter.update(analysis_result["looking"])

            draw_points(frame, analysis_result["points"])
            draw_info(frame, analysis_result, counter_result)

            if counter_result["new_contact"]:
                print(f"[EVENT] Новый контакт. Всего: {counter_result['contacts_count']}")

            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord("q"):
                break

        self.close()

    def close(self):
        self.camera_stream.release()
        self.face_analyzer.close()
        cv2.destroyAllWindows()