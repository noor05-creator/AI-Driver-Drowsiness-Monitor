"""
main.py

Entry point for the real-time Driver Drowsiness Monitor.
Integrates webcam feed, EAR detection, CNN classification,
dual-confirmation alerts, audio alarm, HUD overlay, and
CSV session logging into one unified pipeline.
"""

import os
import csv
import datetime
import cv2
import numpy as np
import pygame
from tensorflow.keras.models import load_model
from detector import detect_drowsiness


# --- Constants ---
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 20
CNN_THRESHOLD = 0.5
MODEL_PATH = os.path.join("model", "drowsiness_cnn.h5")
ALARM_PATH = os.path.join("assets", "alarm.wav")
LOG_PATH = os.path.join("logs", "session_log.csv")
DAT_PATH = "shape_predictor_68_face_landmarks.dat"


def init_csv():
    """
    Initialize the session log CSV file with headers.

    Creates the logs directory if it does not exist.
    Writes the header row if the file does not exist yet.

    Args:
        None

    Returns:
        None
    """
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["timestamp", "ear", "cnn_conf", "status"]
            )


def log_event(ear, cnn_conf, status):
    """
    Log a single detection event to the session CSV file.

    Args:
        ear (float): Eye Aspect Ratio value for the frame.
        cnn_conf (float): CNN confidence score (0.0 to 1.0).
        status (str): Either 'DROWSY' or 'ALERT'.

    Returns:
        None
    """
    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, ear, cnn_conf, status])


def preprocess_eye(eye_region):
    """
    Preprocess an eye region for CNN classification.

    Resizes the eye ROI to 24x24 pixels, converts to
    grayscale, normalizes pixel values, and reshapes
    for model input.

    Args:
        eye_region (numpy.ndarray): Cropped eye image
            from the webcam frame.

    Returns:
        numpy.ndarray: Preprocessed eye array of shape
            (1, 24, 24, 1) ready for CNN input.
    """
    eye = cv2.resize(eye_region, (24, 24))
    eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
    eye = eye / 255.0
    eye = eye.reshape(1, 24, 24, 1)
    return eye

def draw_hud(frame, ear, cnn_conf, status, elapsed):
    """
    Draw the HUD overlay on the video frame.

    Displays EAR value, CNN confidence, session timer,
    and current drowsiness status on the frame.

    Args:
        frame (numpy.ndarray): Current video frame.
        ear (float): Current Eye Aspect Ratio value.
        cnn_conf (float): CNN confidence score.
        status (str): Either 'DROWSY' or 'ALERT'.
        elapsed (str): Session time elapsed as string.

    Returns:
        numpy.ndarray: Frame with HUD overlay drawn.
    """
    h = frame.shape[0]
    color = (0, 0, 255) if status == "DROWSY" else (0, 255, 0)
    label = "DROWSY! ⚠" if status == "DROWSY" else "ALERT ✓"

    cv2.putText(
        frame, label, (10, h - 90),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2
    )
    cv2.putText(
        frame, f"CNN: {cnn_conf:.2f}", (10, h - 60),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
    )
    cv2.putText(
        frame, f"Time: {elapsed}", (10, h - 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
    )
    return frame


def run_detection():
    """
    Run the main real-time drowsiness detection pipeline.

    Opens the webcam, loads the CNN model and alarm sound,
    processes each frame for EAR and CNN-based drowsiness
    detection, triggers dual-confirmation alerts, logs
    events to CSV, and displays the HUD overlay.
    Exits cleanly when 'q' is pressed.

    Args:
        None

    Returns:
        None
    """
    # --- Initialize ---
    init_csv()
    pygame.mixer.init()

    if not os.path.exists(ALARM_PATH):
        print(f"Warning: alarm file not found at {ALARM_PATH}")
        alarm = None
    else:
        alarm = pygame.mixer.Sound(ALARM_PATH)

    if not os.path.exists(MODEL_PATH):
        print(f"Error: model not found at {MODEL_PATH}")
        print("Please run model_train.py first.")
        return

    print("Loading CNN model...")
    model = load_model(MODEL_PATH)

    print("Opening webcam...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        print("Check webcam connection and try again.")
        return

    counter = 0
    alarm_on = False
    start_time = datetime.datetime.now()

    print("Detection started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to read from webcam.")
            break

        # --- EAR Detection ---
        frame, counter, ear, ear_alert = detect_drowsiness(
            frame, counter
        )

        # --- CNN Detection ---
        cnn_conf = 0.0
        cnn_alert = False
        h, w = frame.shape[:2]
        eye_region = frame[0:h//3, 0:w]

        try:
            eye_input = preprocess_eye(eye_region)
            cnn_conf = float(model.predict(
                eye_input, verbose=0
            )[0][0])
            cnn_alert = cnn_conf > CNN_THRESHOLD
        except Exception:
            cnn_conf = 0.0
            cnn_alert = False

        # --- Dual Confirmation ---
        drowsy = ear_alert and cnn_alert

        if drowsy:
            status = "DROWSY"
            if alarm and not alarm_on:
                alarm.play(-1)
                alarm_on = True
            log_event(ear, cnn_conf, status)
        else:
            status = "ALERT"
            if alarm_on:
                pygame.mixer.stop()
                alarm_on = False

        # --- HUD Overlay ---
        elapsed = str(
            datetime.datetime.now() - start_time
        ).split(".")[0]
        frame = draw_hud(frame, ear, cnn_conf, status, elapsed)

        cv2.imshow("Driver Drowsiness Monitor", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()
    print("Session ended.")


if __name__ == "__main__":
    run_detection()