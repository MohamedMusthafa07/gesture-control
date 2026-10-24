# Gesture Control Presenter

A small Python project that lets me change Google Slides with hand gestures. It uses the laptop webcam, so there is no clicker or other hardware.

## About this project

I attended an online AI bootcamp where hand tracking was covered. After that I wanted to try it on something useful, so I built this myself to control my slides while presenting. The gesture rules, the cooldown logic and the speed fixes came from testing it on my own laptop.

## Why I made it

When presenting, I either have to stay next to the laptop or hold a clicker to change slides. I wanted to just show a hand sign to the camera instead.

## Gestures

| Gesture | Action |
| --- | --- |
| Open palm (4 fingers) | Next slide |
| Three fingers | Previous slide |
| Two fingers | Start slideshow |
| Fist | Exit slideshow |

## Tech used

- Python
- OpenCV (webcam capture and drawing on the frame)
- MediaPipe (hand landmark detection)
- PyAutoGUI (sends the keyboard shortcuts)

## How it works

1. OpenCV reads frames from the webcam.
2. MediaPipe finds the 21 landmarks of the hand in each frame.
3. For the index, middle, ring and pinky fingers, I check whether the fingertip is above its middle joint. If it is, that finger counts as up.
4. The number of fingers up is matched to an action.
5. PyAutoGUI sends the matching key press to the active window.

To avoid wrong triggers, a gesture has to stay the same for a few frames before it counts, and there is a cooldown after every action so one gesture does not fire again and again.

## Setup

```bash
git clone https://github.com/MohamedMusthafa07/gesture-control
cd gesture-control
pip install -r requirements.txt
python setup_models.py
```

`setup_models.py` downloads the MediaPipe hand landmarker model into the `models` folder.

## Run

```bash
python main.py
```

Press `q` in the webcam window to quit.

## How to use

1. Open your slides in Google Slides in Chrome.
2. Run `python main.py`.
3. Click the Chrome window so it has keyboard focus. The key presses go to whichever window is active.
4. Hold your hand upright in front of the webcam, palm facing the camera, and use the gestures.

## Platform notes

- **Windows:** two fingers sends `Ctrl + F5`. No extra permissions needed.
- **macOS:** two fingers sends `Command + Enter`. Allow Accessibility, Input Monitoring and Camera for your terminal or editor in System Settings, under Privacy & Security.

## Tips

- Use good lighting and keep your hand clearly visible.
- A plain background works better than a cluttered one.
- Stay at a moderate distance from the camera.
- The finger count only works when the hand is upright. A tilted or sideways hand gives wrong counts.
- If it feels slow, plug in the charger and close extra browser tabs. The window shows the current FPS.
- If gestures trigger too easily, increase `STABLE_FRAMES` in `main.py`.

## Project structure

```
gesture-control/
├── main.py
├── setup_models.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── models/
    └── hand_landmarker.task   (downloaded by setup_models.py)
```

## What I learned

- Reading and processing webcam frames in real time with OpenCV
- Getting hand landmarks from MediaPipe and turning them into simple gesture rules
- Why running detection in video mode is much faster than detecting from scratch every frame
- Reading the camera in a separate thread to reduce lag
- Using cooldowns and frame checks so one gesture triggers one action

## Future improvements

These are things I noticed while using it that would make it better in a real presentation.

- **Activate and lock gesture.** Right now any hand that enters the camera view can trigger a slide change, even when I am just waving my hands while talking. I want a gesture that locks and unlocks the controls.
- **Swipe left and right.** Swiping feels more natural than holding up fingers, and it avoids accidental triggers while the hand is opening or closing.
- **Settings file.** Keep the gesture mapping, cooldown and camera number in a config file, so these can be changed without editing the code.
- **Other presentation software.** Support PowerPoint and PDF viewers, which use different shortcuts.

## Author

A. Mohamed Musthafa

- GitHub: [MohamedMusthafa07](https://github.com/MohamedMusthafa07)
- LinkedIn: [mohamedmusthafa07](https://www.linkedin.com/in/mohamedmusthafa07)

## License

MIT License. See the `LICENSE` file.