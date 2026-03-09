from ultralytics import YOLO


class VehicleDetector:
    def __init__(self, model_path: str, vehicle_classes: set[str]):
        self.model = YOLO(model_path)
        self.vehicle_classes = vehicle_classes

    def detect_and_track(self, frame):
        """
        Возвращает список объектов:
        [
            {
                "track_id": int,
                "label": str,
                "confidence": float,
                "bbox": (x1, y1, x2, y2),
                "center": (cx, cy),
            }
        ]
        """
        results = self.model.track(frame, persist=True, verbose=False)[0]

        detections = []

        if results.boxes is None:
            return detections

        for box in results.boxes:
            if box.id is None:
                continue

            cls_id = int(box.cls[0].item())
            label = self.model.names[cls_id]

            if label not in self.vehicle_classes:
                continue

            track_id = int(box.id[0].item())
            confidence = float(box.conf[0].item())

            x1, y1, x2, y2 = box.xyxy[0].tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            detections.append({
                "track_id": track_id,
                "label": label,
                "confidence": confidence,
                "bbox": (x1, y1, x2, y2),
                "center": (cx, cy),
            })

        return detections