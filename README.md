# Gesture Control Presenter 🎮🖐️

I built this project to control Google Slides presentations with hand gestures, using my laptop webcam, Computer Vision and AI.

---

# 📌 Project Overview

Gesture Control Presenter tracks my hand in real time using **MediaPipe**, counts the fingers I hold up with **OpenCV**, and turns each gesture into a keyboard shortcut using **PyAutoGUI**. No clicker or extra hardware is needed, only a webcam.

---

# ❓ Problem Statement

While presenting, I have to stay near the laptop or hold a clicker to change slides. I wanted a hands-free way to move through a presentation, so I built a system that recognises simple hand gestures and controls the slideshow for me.

---

# 🚀 Features

* Control Google Slides using gestures
* Real-time hand tracking using AI
* Works directly from the laptop webcam
* No additional hardware required
* Works on Windows and macOS

---

# 🧠 Gesture Controls

| Gesture          | Action          |
| ---------------- | --------------- |
| ✋ Open Palm      | Next Slide      |
| 🤟 Three Fingers | Previous Slide  |
| ✌️ Two Fingers   | Start Slideshow |
| ✊ Fist           | Exit Slideshow  |

---

# 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* PyAutoGUI

---

# 📦 Installation

## Step 1 — Clone the Project

```bash
git clone https://github.com/MohamedMusthafa07/gesture-control
cd gesture-control
```

## Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3 — Download the Hand Landmarker Model

```bash
python setup_models.py
```

---

# ▶️ Run the App

```bash
python main.py
```

Press **q** in the webcam window to quit.

---

# 💻 Platform Notes

**Windows:** the "Two Fingers" gesture sends `Ctrl + F5` (Google Slides present shortcut). No extra permissions are needed.

**macOS:** the "Two Fingers" gesture sends `Command + Enter`.

## macOS Permission Setup

Go to **System Settings → Privacy & Security** and enable **Accessibility**, **Input Monitoring** and **Camera** for Terminal, VS Code or PyCharm. Without these permissions, the app cannot control Google Slides.

---

# 🎯 How to Use

1. Open Google Slides in Chrome
2. Run the Python application
3. Click the Chrome window so it has keyboard focus
4. Show gestures in front of the webcam
5. Control slides hands-free

---

# 📂 Project Structure

```bash
gesture-control/
│
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
├── setup_models.py
└── models/
    └── hand_landmarker.task
```

---

# 🧩 How It Works

1. I capture the webcam feed using OpenCV
2. MediaPipe detects the hand landmarks
3. I check which fingertips are above their joints to count raised fingers
4. Each finger count is mapped to a keyboard shortcut
5. PyAutoGUI sends that shortcut to Google Slides

---

# 📚 What I Learned

* Real-time webcam processing with OpenCV
* Hand landmark detection using MediaPipe
* Turning landmark positions into simple gesture rules
* Automating keyboard control with Python
* Handling cooldowns so one gesture doesn't trigger repeatedly
* Making code work across Windows and macOS

---

# 🔮 Future Improvements

* Swipe gesture recognition
* Gesture-based laser pointer
* Volume control
* Zoom gestures
* Custom gesture training
* Multi-hand support

---

# ⚠️ Notes

* Make sure the lighting is good
* Keep your hand visible to the webcam
* Avoid cluttered backgrounds for better detection
* Works best at a moderate distance from the camera

---

# 🔗 Useful Links

* [MediaPipe Hand Landmarker Live Demo](https://google-ai-edge.github.io/mediapipe-samples-web/#/vision/hand_landmarker)
* [Google AI MediaPipe Guide](https://ai.google.dev/edge/mediapipe/solutions/guide)

---

# 🎓 Internship Information

* **Organization:** CodeAlpha
* **Project:** Gesture Control Presenter

---

# 👨‍💻 Author

**A. Mohamed Musthafa**

* GitHub: [MohamedMusthafa07](https://github.com/MohamedMusthafa07)
* LinkedIn: [mohamedmusthafa07](https://www.linkedin.com/in/mohamedmusthafa07)

---

# 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

