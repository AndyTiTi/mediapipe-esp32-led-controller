# Hand Gesture LED Control

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Arduino](https://img.shields.io/badge/Arduino-ESP32-green.svg)](https://www.arduino.cc/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg)](https://mediapipe.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**English** | **[中文](README-zh.md)**

Real-time dual LED control system using hand gesture recognition. Control two LEDs independently with your left and right hand through webcam.

![Demo](demo.gif) *(Add your demo gif here)*

## Features

- **Dual Hand Detection** - Recognize left and right hand simultaneously
- **Independent LED Control** - Left hand controls LED1, right hand controls LED2
- **Skeleton Visualization** - Real-time hand skeleton rendering (spider-web style)
-  **Keyboard Control** - Manual LED control for testing
- **Real-time FPS Display** - Monitor performance
- **Serial Debug Output** - Separate debug port for logging

## 🎮 Demo

| Gesture | Action | LED |
|---------|--------|-----|
| Raise Left Hand | Hand above threshold line | LED1 ON |
| Lower Left Hand | Hand below threshold line | LED1 OFF |
| Raise Right Hand | Hand above threshold line | LED2 ON |
| Lower Right Hand | Hand below threshold line | LED2 OFF |

## Hardware Requirements

| Component | Description |
|-----------|-------------|
| ESP32 Dev Board | Or Arduino-compatible board |
| 2x LEDs | Any color |
| 2x 220Ω Resistors | For LED current limiting |
| USB Cable | For programming and serial communication |
| USB-TTL Module | Optional, for debug logging |
| Webcam | Any USB camera |

## Wiring

```
ESP32 Pin 8  ───────────► LED1 (+) ──► GND
ESP32 Pin 18 ───────────► LED2 (+) ──► GND
ESP32 Pin 17 ───────────► USB-TTL RX (debug output)
ESP32 GND   ────────────► USB-TTL GND
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hand-gesture-led-control.git
cd hand-gesture-led-control
```

### 2. Install Python Dependencies

```bash
# Option 1: Direct install
pip install opencv-python mediapipe pyserial numpy

# Option 2: Virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

pip install opencv-python mediapipe pyserial numpy
```

### 3. Download MediaPipe Model

```bash
# Windows PowerShell
curl -o hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

# Linux/Mac
wget https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
```

Or download directly: [hand_landmarker.task](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)

### 4. Upload Arduino Code

1. Open `mediapipe-esp32-led-controller.ino` in Arduino IDE
2. Select your board (ESP32 recommended)
3. Select the correct COM port
4. Click Upload

### 5. Run the Program

```bash
python main.py
```

##  Keyboard Controls

| Key | Action |
|-----|--------|
| `1` | Turn LED1 ON |
| `2` | Turn LED1 OFF |
| `3` | Turn LED2 ON |
| `4` | Turn LED2 OFF |
| `m` | Toggle display mode (simple/skeleton) |
| `q` | Quit program |

## Configuration

Edit `main.py` to customize:

```python
SERIAL_PORT = "COM14"          # Your Arduino COM port
HAND_RAISE_THRESH = 0.5        # Raise threshold (0-1, smaller = higher)
HAND_DISPLAY_MODE = "skeleton" # "skeleton" or "simple"
```

## Project Structure

```
hand-gesture-led-control/
├── main.py                                         # Python main program
├── mediapipe-esp32-led-controller.ino              # Arduino firmware
├── hand_landmarker.task                            # MediaPipe model file
├── README.md                                       # Documentation
└── blink_env/                                      # Python virtual environment
```

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Webcam    │────►│  MediaPipe   │────►│   Python    │
│             │     │ Hand Tracker │     │   Script    │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                    ┌───────────────────────────┘
                    │ Serial Communication
                    ▼
           ┌────────────────┐
           │    ESP32       │
           │  ┌────┐ ┌────┐ │
           │  │LED1│ │LED2│ │
           │  └────┘ └────┘ │
           └────────────────┘
```

1. **Capture** - OpenCV captures real-time video from webcam
2. **Detect** - MediaPipe detects 21 hand landmarks
3. **Identify** - Determine left/right hand by landmark positions
4. **Track** - Monitor hand position (raised/lowered)
5. **Control** - Send serial commands to Arduino
6. **Actuate** - Arduino toggles corresponding LED

## Hand Skeleton Visualization

The skeleton mode displays 21 hand landmarks:

```
Landmark Index:
0      - Wrist
1-4    - Thumb
5-8    - Index finger
9-12   - Middle finger
13-16  - Ring finger
17-20  - Pinky finger
```

## Troubleshooting

<details>
<summary><b>Serial port cannot be opened</b></summary>

- Check if Arduino is connected
- Verify the COM port in Device Manager (Windows) or `ls /dev/tty*` (Linux/Mac)
- Close Arduino Serial Monitor if open
- Make sure no other program is using the port
</details>

<details>
<summary><b>Hand detection not working</b></summary>

- Ensure `hand_landmarker.task` file exists in project directory
- Check webcam is working and not used by other applications
- Improve lighting conditions
- Keep hands within camera frame
</details>

<details>
<summary><b>LEDs not responding</b></summary>

- Verify wiring connections
- Check LED polarity (longer leg is positive)
- Confirm correct pins: LED1=Pin 8, LED2=Pin 18
- Check serial communication in Python console
</details>

<details>
<summary><b>No debug output on Serial2</b></summary>

- Verify USB-TTL connections: RX→Pin 17, GND→GND
- Check baud rate is 115200
- Try swapping RX/TX wires
- Ensure USB-TTL driver is installed
</details>

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) - Hand tracking solution
- [OpenCV](https://opencv.org/) - Computer vision library
- [Arduino](https://www.arduino.cc/) - Open-source hardware platform

## Contact

栈先锋 - [@栈先锋](https://space.bilibili.com/317356181)

Project Link: [https://github.com/AndyTiTi/mediapipe-esp32-led-controller](https://github.com/AndyTiTi/mediapipe-esp32-led-controller)

---

⭐ If this project helped you, please give it a star!
