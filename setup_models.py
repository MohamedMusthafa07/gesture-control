import os
import urllib.request

URL = ("https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
       "hand_landmarker/float16/1/hand_landmarker.task")
folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
path = os.path.join(folder, "hand_landmarker.task")

os.makedirs(folder, exist_ok=True)
if os.path.exists(path):
    print("Model already exists:", path)
else:
    print("Downloading hand landmarker model...")
    urllib.request.urlretrieve(URL, path)
    print("Saved to", path)
