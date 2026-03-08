import cv2


def draw_points(frame, points: dict | None):
    if not points:
        return frame

    for _, point in points.items():
        cv2.circle(frame, point, 4, (0, 255, 0), -1)

    cv2.line(frame, points["left_eye"], points["right_eye"], (255, 0, 0), 2)
    cv2.line(frame, points["nose_tip"], (
        (points["left_eye"][0] + points["right_eye"][0]) // 2,
        (points["left_eye"][1] + points["right_eye"][1]) // 2,
    ), (0, 0, 255), 2)

    return frame


def draw_info(frame, analysis_result: dict, counter_result: dict):
    face_detected = analysis_result["face_detected"]
    looking = analysis_result["looking"]
    nose_offset_ratio = analysis_result["nose_offset_ratio"]

    cv2.putText(
        frame,
        f"Face detected: {face_detected}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"Looking: {looking}",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0) if looking else (0, 0, 255),
        2,
    )

    ratio_text = "None" if nose_offset_ratio is None else f"{nose_offset_ratio:.3f}"
    cv2.putText(
        frame,
        f"Nose offset ratio: {ratio_text}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"State: {counter_result['state']}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2,
    )

    cv2.putText(
        frame,
        f"Contacts: {counter_result['contacts_count']}",
        (20, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 255),
        2,
    )

    return frame