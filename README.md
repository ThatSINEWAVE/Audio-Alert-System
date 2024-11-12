<div align="center">

# Audio Alerts System

This repository contains a **Proof of Concept** for the *Audio Alerts System*, an interactive GUI-based application designed to test and manage audio alerts across different categories. The system was developed using Python with `tkinter` and `pygame` to create an intuitive interface for testing audio notifications. The project is currently in a prototype stage, intended for evaluation and improvement.

![Audio-Alerts-System](https://raw.githubusercontent.com/ThatSINEWAVE/Audio-Alert-System/refs/heads/main/assets/Audio%20Alert%20Tester.png?token=GHSAT0AAAAAACSGFGDFLO4MKW5RO3DH6XZSZZT242Q)

</div>

## Features

- **GUI-based Testing Interface**: Built with `tkinter` and `customtkinter`, the interface lets users test various audio alerts by selecting categories and playing predefined sounds.
- **Alert Categories**: Alerts are organized into three main categories:
  - **Warnings**: Critical system alerts.
  - **Messages**: Status updates for program states.
  - **Reasons**: Additional information about system events.
- **Logging System**: Logs audio playback events for easy monitoring and debugging.
- **Real-time Audio Playback**: Uses `pygame`'s mixer to play `.mp3` files directly from the application.

<div align="center">

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

</div>

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/Audio-Alerts-System.git
    cd Audio-Alerts-System
    ```

2. **Install dependencies**:
    ```bash
    pip install pygame customtkinter
    ```

3. **Ensure the following directories and files are present** under `audio/`:
    - `Messages`: Contains alert sounds for program states.
    - `Reasons`: Holds sounds for possible event explanations.
    - `Warnings`: Includes critical system warnings.

4. **Run the application**:
    ```bash
    python main.py
    ```

## Usage

- **Select Alerts**: Open the app and select audio files under *Messages*, *Reasons*, or *Warnings*.
- **Test Alert Sequence**: Click "Test Alert Sequence" to play the selected alerts in order.
- **View Logs**: Check `logs/log.txt` to review all played alerts and application events.

## Directory Structure

```plaintext
Audio-Alerts-System/
├── audio/
│   ├── Messages/
│   ├── Reasons/
│   └── Warnings/
├── logs/
│   └── log.txt
└── system.py
```

## Requirements

- Python 3.8+
- `pygame`
- `customtkinter`

## Future Plans

- **Expand Alert Categories**: More categories and audio variations.
- **Enhanced Error Handling**: Improve robustness in audio file playback.
- **Modular Design**: Refine code structure for easier customization.

This system is a work-in-progress designed for hands-on testing with potential for integration into broader projects like notification systems or alert monitoring tools.