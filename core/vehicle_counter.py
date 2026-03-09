class VehicleCounter:
    def __init__(self, roi: tuple[int, int, int, int], count_line_y: int):
        self.roi = roi
        self.count_line_y = count_line_y

        self.total_count = 0

        self.count_by_type = {
            "car": 0,
            "bus": 0,
            "truck": 0,
        }

        # История последних центров по track_id
        self.track_last_centers = {}

        # Уже посчитанные track_id
        self.counted_track_ids = set()

    def update(self, detections: list[dict]):
        new_count = 0
        new_count_by_type = {
            "car": 0,
            "bus": 0,
            "truck": 0,
        }

        for detection in detections:
            track_id = detection["track_id"]
            label = detection["label"]
            cx, cy = detection["center"]

            if not self._is_in_roi(cx, cy):
                continue

            previous_center = self.track_last_centers.get(track_id)
            self.track_last_centers[track_id] = (cx, cy)

            if previous_center is None:
                continue

            _, prev_y = previous_center

            crossed_down = prev_y < self.count_line_y <= cy

            if crossed_down and track_id not in self.counted_track_ids:
                self.counted_track_ids.add(track_id)

                self.total_count += 1
                new_count += 1

                if label in self.count_by_type:
                    self.count_by_type[label] += 1
                    new_count_by_type[label] += 1

        return {
            "total_count": self.total_count,
            "count_by_type": self.count_by_type.copy(),
            "new_count": new_count,
            "new_count_by_type": new_count_by_type,
        }

    def _is_in_roi(self, x: int, y: int) -> bool:
        x1, y1, x2, y2 = self.roi
        return x1 <= x <= x2 and y1 <= y <= y2