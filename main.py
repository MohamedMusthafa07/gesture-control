import os
import platform
import threading
import time

import cv2
import mediapipe as mp
import pyautogui
from mediapipe.tasks.python import vision

pyautogui.PAUSE = 0  # remove PyAutoGUI's default delay after each action

# Resolve the hand landmark model relative to this script so execution is cwd-independent.
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "hand_landmarker.task")

if not os.path.exists(model_path):
    print(f"Error: Model file not found at {model_path}")
    print("Please run: python setup_models.py")
    raise SystemExit(1)

# Google Slides "present from start" shortcut differs per OS.
IS_WINDOWS = platform.system() == "Windows"
if platform.system() == "Darwin":
    START_KEYS = ("command", "enter")
else:
    START_KEYS = ("ctrl", "f5")

# VIDEO mode tracks the hand between frames instead of re-detecting every frame (much faster).
base_options = mp.tasks.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.6,
    min_hand_presence_confidence=0.6,
    min_tracking_confidence=0.6,
)
hand_landmarker = vision.HandLandmarker.create_from_options(options)


class Camera:
    """Reads frames in a background thread so the main loop always gets the newest frame."""

    def __init__(self, index=0):
        backend = cv2.CAP_DSHOW if IS_WINDOWS else cv2.CAP_ANY
        self.cap = cv2.VideoCapture(index, backend)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.frame = None
        self.lock = threading.Lock()
        self.running = True
        if self.cap.isOpened():
            threading.Thread(target=self._loop, daemon=True).start()

    def isOpened(self):
        return self.cap.isOpened()

    def _loop(self):
        while self.running:
            ok, frame = self.cap.read()
            if ok:
                with self.lock:
                    self.frame = frame

    def read(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

    def release(self):
        self.running = False
        time.sleep(0.1)
        self.cap.release()


# Open the default webcam (index 0). Change to 1 if you have several cameras.
cap = Camera(0)
if not cap.isOpened():
    print("Error: Could not open the webcam. Try changing Camera(0) to Camera(1).")
    raise SystemExit(1)

last_time = 0
# Prevent repeated key presses when a gesture is held across multiple frames.
cooldown = 1.2
# A gesture must stay the same for this many frames before it fires (avoids accidental triggers).
STABLE_FRAMES = 5

CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),             # Thumb
    (5, 6), (6, 7), (7, 8),                     # Index
    (9, 10), (10, 11), (11, 12),                # Middle
    (13, 14), (14, 15), (15, 16),               # Ring
    (17, 18), (18, 19), (19, 20),               # Pinky
    (0, 5), (5, 9), (9, 13), (13, 17), (0, 17)  # Palm
]


def fingers_up(hand_landmarks):
    """Return [index, middle, ring, pinky] as 1 (up) or 0 (down)."""
    tips = [8, 12, 16, 20]   # Fingertip indices
    pips = [6, 10, 14, 18]   # PIP joint indices

    fingers = []
    for tip, pip in zip(tips, pips):
        # If tip is above pip (smaller y), finger is up
        fingers.append(1 if hand_landmarks[tip].y < hand_landmarks[pip].y else 0)
    return fingers


gesture = "Waiting..."
gesture_shown_at = 0
last_fingers = None
stable_count = 0
last_ts = 0
prev_frame_time = time.time()

try:
    while True:
        frame = cap.read()
        if frame is None:
            time.sleep(0.01)
            continue

        # Mirror the frame so hand movement feels natural to the person on camera.
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # VIDEO mode needs a strictly increasing timestamp in milliseconds.
        ts = int(time.monotonic() * 1000)
        if ts <= last_ts:
            ts = last_ts + 1
        last_ts = ts

        detection_result = hand_landmarker.detect_for_video(mp_image, ts)

        if detection_result.hand_landmarks:
            hand_landmarks = detection_result.hand_landmarks[0]

            # Draw connections between landmarks
            for start_idx, end_idx in CONNECTIONS:
                start = hand_landmarks[start_idx]
                end = hand_landmarks[end_idx]
                cv2.line(
                    frame,
                    (int(start.x * w), int(start.y * h)),
                    (int(end.x * w), int(end.y * h)),
                    (0, 255, 0),
                    1,
                )

            # Draw hand landmarks
            for landmark in hand_landmarks:
                cv2.circle(frame, (int(landmark.x * w), int(landmark.y * h)), 3, (0, 255, 0), -1)

            # Reduce detailed landmarks into a simple "how many fingers are up" signal.
            total = fingers_up(hand_landmarks).count(1)

            # Require the same finger count for a few frames in a row.
            stable_count = stable_count + 1 if total == last_fingers else 1
            last_fingers = total

            current_time = time.time()

            if stable_count >= STABLE_FRAMES and current_time - last_time > cooldown:
                # OPEN PALM -> NEXT SLIDE (4 fingers up)
                if total == 4:
                    pyautogui.press("right")
                    gesture = "Next Slide"
                    last_time = current_time
                    gesture_shown_at = current_time

                # THREE FINGERS -> PREVIOUS SLIDE
                elif total == 3:
                    pyautogui.press("left")
                    gesture = "Previous Slide"
                    last_time = current_time
                    gesture_shown_at = current_time

                # TWO FINGERS -> START PRESENTATION
                elif total == 2:
                    pyautogui.hotkey(*START_KEYS)
                    gesture = "Start Slideshow"
                    last_time = current_time
                    gesture_shown_at = current_time

                # FIST -> EXIT PRESENTATION (0 fingers up)
                elif total == 0:
                    pyautogui.press("esc")
                    gesture = "Exit Slideshow"
                    last_time = current_time
                    gesture_shown_at = current_time
        else:
            last_fingers = None
            stable_count = 0

        # Keep the last action visible for 1.5 seconds instead of flashing for one frame.
        if time.time() - gesture_shown_at > 1.5:
            gesture = "Waiting..."

        # FPS counter
        now = time.time()
        fps = 1 / max(now - prev_frame_time, 1e-6)
        prev_frame_time = now

        cv2.putText(frame, gesture, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"FPS: {int(fps)}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow("Google Slides Gesture Control", frame)

        # Press q in the preview window to stop the app.
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    cap.release()
    hand_landmarker.close()
    cv2.destroyAllWindows()