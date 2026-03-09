from config import (
    VIDEO_PATH,
    VEHICLE_WINDOW_NAME,
    YOLO_MODEL_PATH,
    VEHICLE_CLASSES,
    ROI_X1,
    ROI_Y1,
    ROI_X2,
    ROI_Y2,
    COUNT_LINE_Y,
    SHOW_VIDEO,
)

from core.video_file_source import VideoFileSource
from core.vehicle_detector import VehicleDetector
from core.vehicle_counter import VehicleCounter
from core.vehicle_app import VehicleApp


def main():
    source = VideoFileSource(video_path=VIDEO_PATH)

    detector = VehicleDetector(
        model_path=YOLO_MODEL_PATH,
        vehicle_classes=VEHICLE_CLASSES,
    )

    counter = VehicleCounter(
        roi=(ROI_X1, ROI_Y1, ROI_X2, ROI_Y2),
        count_line_y=COUNT_LINE_Y,
    )

    app = VehicleApp(
        source=source,
        detector=detector,
        counter=counter,
        window_name=VEHICLE_WINDOW_NAME,
        show_video=SHOW_VIDEO,
    )

    app.run()


if __name__ == "__main__":
    main()