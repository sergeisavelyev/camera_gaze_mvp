CAMERA_INDEX = 0

WINDOW_NAME = "Camera Gaze MVP"

MODEL_PATH = "models/face_landmarker.task"

# Новый MediaPipe Tasks API
NUM_FACES = 1
MIN_FACE_DETECTION_CONFIDENCE = 0.5
MIN_FACE_PRESENCE_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Пороги логики контакта
FRAMES_TO_CONFIRM_LOOKING = 8
FRAMES_TO_CONFIRM_NOT_LOOKING = 5

# Эвристика "смотрит в сторону камеры"
MAX_NOSE_OFFSET_RATIO = 0.20

# ===== VEHICLE MODE =====
VIDEO_PATH = "test_data/road_video.mov"
VEHICLE_WINDOW_NAME = "Vehicle Counter MVP"

YOLO_MODEL_PATH = "yolov8n.pt"

# Считаем только эти классы
VEHICLE_CLASSES = {"car", "bus", "truck"}

# ROI для встречной полосы: (x1, y1, x2, y2)
ROI_X1 = 0
ROI_Y1 = 500
ROI_X2 = 980
ROI_Y2 = 1070

# Линия подсчёта
COUNT_LINE_Y = 1000

# Показывать ли окно
SHOW_VIDEO = True