import cv2


class VehicleApp:
    def __init__(self, source, detector, counter, window_name: str, show_video: bool = True):
        self.source = source
        self.detector = detector
        self.counter = counter
        self.window_name = window_name
        self.show_video = show_video

    def run(self):
        while True:
            frame = self.source.read()
            if frame is None:
                print("Видео завершено")
                self._print_final_stats()
                break

            detections = self.detector.detect_and_track(frame)
            counter_result = self.counter.update(detections)

            self._draw(frame, detections, counter_result)

            if counter_result["new_count"] > 0:
                self._print_event(counter_result)

            if self.show_video:
                cv2.imshow(self.window_name, frame)
                key = cv2.waitKey(1) & 0xFF
                if key == 27 or key == ord("q"):
                    print("Остановка по запросу пользователя")
                    self._print_final_stats()
                    break

        self.close()

    def close(self):
        self.source.release()
        cv2.destroyAllWindows()

    def _print_event(self, counter_result: dict):
        count_by_type = counter_result["count_by_type"]
        new_count_by_type = counter_result["new_count_by_type"]

        print(
            f"[EVENT] +{counter_result['new_count']} | "
            f"car:+{new_count_by_type['car']} "
            f"bus:+{new_count_by_type['bus']} "
            f"truck:+{new_count_by_type['truck']} | "
            f"TOTAL={counter_result['total_count']} "
            f"(car={count_by_type['car']}, bus={count_by_type['bus']}, truck={count_by_type['truck']})"
        )

    def _print_final_stats(self):
        print("\n=== ИТОГОВАЯ СТАТИСТИКА ===")
        print(f"TOTAL: {self.counter.total_count}")
        print(f"car:   {self.counter.count_by_type['car']}")
        print(f"bus:   {self.counter.count_by_type['bus']}")
        print(f"truck: {self.counter.count_by_type['truck']}")

    def _draw(self, frame, detections, counter_result):
        x1, y1, x2, y2 = self.counter.roi

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.line(frame, (x1, self.counter.count_line_y), (x2, self.counter.count_line_y), (0, 0, 255), 3)

        for detection in detections:
            bbox = detection["bbox"]
            cx, cy = detection["center"]
            track_id = detection["track_id"]
            label = detection["label"]

            if not self.counter._is_in_roi(cx, cy):
                continue

            bx1, by1, bx2, by2 = bbox

            cv2.rectangle(frame, (bx1, by1), (bx2, by2), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)

            text = f"{label} ID:{track_id}"
            cv2.putText(
                frame,
                text,
                (bx1, max(20, by1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

        count_by_type = counter_result["count_by_type"]

        cv2.putText(
            frame,
            f"Total: {counter_result['total_count']}",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"car: {count_by_type['car']}",
            (30, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"bus: {count_by_type['bus']}",
            (30, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"truck: {count_by_type['truck']}",
            (30, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )