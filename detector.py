import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils


EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 20

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    "shape_predictor_68_face_landmarks.dat"
)

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


def eye_aspect_ratio(eye):
    """
    Calculate the Eye Aspect Ratio (EAR) for a given eye.

    EAR is used to detect blink and eye closure states.
    A value below 0.25 typically indicates a closed eye.

    Args:
        eye (numpy.ndarray): Array of 6 (x, y) landmark coordinates
                             representing the eye contour points.

    Returns:
        float: The Eye Aspect Ratio value. Lower values indicate
               more closed eyes.
    """
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


def draw_eye_contours(frame, left_eye, right_eye):
    """
    Draw convex hull contours around both eyes on the frame.

    Args:
        frame (numpy.ndarray): The video frame to draw on.
        left_eye (numpy.ndarray): Landmark coordinates for left eye.
        right_eye (numpy.ndarray): Landmark coordinates for right eye.

    Returns:
        numpy.ndarray: Frame with eye contours drawn.
    """
    left_hull = cv2.convexHull(left_eye)
    right_hull = cv2.convexHull(right_eye)
    cv2.drawContours(frame, [left_hull], -1, (0, 255, 0), 1)
    cv2.drawContours(frame, [right_hull], -1, (0, 255, 0), 1)
    return frame


def draw_face_box(frame, face):
    """
    Draw a bounding box around a detected face on the frame.

    Args:
        frame (numpy.ndarray): The video frame to draw on.
        face (dlib.rectangle): Dlib rectangle object for detected face.

    Returns:
        numpy.ndarray: Frame with face bounding box drawn.
    """
    x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    return frame


def detect_drowsiness(frame, counter):
    """
    Detect drowsiness in a video frame using EAR calculation.

    Converts frame to grayscale, detects faces and facial landmarks,
    calculates EAR for both eyes, draws contours and bounding box,
    and determines if drowsiness alert should be triggered.

    Args:
        frame (numpy.ndarray): The current video frame from webcam.
        counter (int): Number of consecutive frames with low EAR.

    Returns:
        tuple: (
            annotated_frame (numpy.ndarray),
            updated_counter (int),
            ear_value (float),
            alert_triggered (bool)
        )
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 0)
    alert = False
    ear = 0.0

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        left_eye = shape[lStart:lEnd]
        right_eye = shape[rStart:rEnd]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        frame = draw_eye_contours(frame, left_eye, right_eye)
        frame = draw_face_box(frame, face)

        if ear < EAR_THRESHOLD:
            counter += 1
            if counter >= CONSEC_FRAMES:
                alert = True
                cv2.putText(
                    frame,
                    "DROWSY!",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )
        else:
            counter = 0

        cv2.putText(
            frame,
            f"EAR: {ear:.3f}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    return frame, counter, ear, alert


def test_on_image(image_path):
    """
    Test the drowsiness detection on a static image file.

    Args:
        image_path (str): Path to the image file to test on.

    Returns:
        None
    """
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not load image from {image_path}")
        return

    result_frame, counter, ear, alert = detect_drowsiness(frame, 0)

    print(f"Image: {image_path}")
    print(f"EAR value: {ear:.3f}")
    print(f"Alert triggered: {alert}")
    print(f"Status: {'DROWSY' if alert else 'ALERT'}")

    cv2.imshow("Test Result", result_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    
    print("Testing with webcam...")
    cap = cv2.VideoCapture(0)
    counter = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame, counter, ear, alert = detect_drowsiness(frame, counter)
        cv2.imshow("Detector Test", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


