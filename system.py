import tkinter as tk
from tkinter import ttk, messagebox
from pydub import AudioSegment
from pydub.playback import play
import os
import time
import logging
from threading import Thread
from datetime import datetime

# Define audio paths and descriptions
AUDIO_DIR = {
    'Messages': 'audio/Messages',
    'Reasons': 'audio/Reasons',
    'Warnings': 'audio/Warnings'
}

# Map files to descriptive names
DESCRIPTIONS = {
    'Messages': {
        'Program completed.m4a': 'PROGRAM COMPLETED',
        'Program stopped.m4a': 'PROGRAM STOPPED',
        'Program crashed.m4a': 'PROGRAM FAILED',
        'Program started.m4a': 'PROGRAM STARTED'
    },
    'Reasons': {
        'Potential crash.m4a': 'POTENTIAL CRASH',
        'Stopped by user.m4a': 'STOPPED BY USER',
        'System error.m4a': 'SYSTEM ERROR',
        'Task completed.m4a': 'TASK COMPLETED',
        'Task failed.m4a': 'TASK FAILED',
        'Unknown.m4a': 'UNKNOWN ISSUE'
    },
    'Warnings': {
        'Abnormal_activity.m4a': 'ABNORMAL ACTIVITY',
        'Critical_error.m4a': 'CRITICAL ERROR',
        'Execution_error.m4a': 'EXECUTION ERROR',
        'Fatal_error.m4a': 'FATAL ERROR',
        'System_warning.m4a': 'SYSTEM WARNING',
        'Unusual_activity.m4a': 'UNUSUAL ACTIVITY',
        'Warning.m4a': 'GENERAL WARNING'
    }
}

# Delay between audio files (in milliseconds)
PLAY_DELAY = 500

# Setup logging
LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'log.txt')
os.makedirs(LOG_DIR, exist_ok=True)  # Create logs directory if it doesn't exist

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Log a message
def log_event(message):
    logging.info(message)


# Load audio files by category
def load_audio_files():
    audio_files = {}
    for category, path in AUDIO_DIR.items():
        try:
            files = [f for f in os.listdir(path) if f.endswith('.m4a')]
            audio_files[category] = files
        except FileNotFoundError:
            messagebox.showerror("Error", f"Directory not found: {path}")
            audio_files[category] = []
    return audio_files


audio_files = load_audio_files()


# Function to play audio alerts in sequence using pydub
def play_alert_sequence(selected_files):
    for category, file in selected_files.items():
        if file:
            filepath = os.path.join(AUDIO_DIR[category], file)
            try:
                audio = AudioSegment.from_file(filepath)
                play(audio)
                log_event(f"Playing {category} alert: {DESCRIPTIONS[category][file]}")
                time.sleep(PLAY_DELAY / 1000)  # Delay in seconds
            except Exception as e:
                log_event(f"Error playing {file}: {e}")
                messagebox.showerror("Playback Error", f"Could not play {file}: {e}")


# UI function to handle button click
def on_test_alert():
    selected_files = {
        'Messages': message_var.get(),
        'Reasons': reason_var.get(),
        'Warnings': warning_var.get()
    }
    if all(selected_files.values()):
        # Create a combination description based on selected files
        combination = ", ".join(DESCRIPTIONS[category][file] for category, file in selected_files.items())
        log_event(f"Test Alert triggered with combination: {combination}")

        # Start playback in a separate thread
        Thread(target=play_alert_sequence, args=(selected_files,)).start()
    else:
        log_event("Selection Error: Not all categories selected")
        messagebox.showwarning("Selection Error", "Please select one alert from each category.")


# Create the main application window
root = tk.Tk()
root.title("Audio Alert Tester - Proof of Concept")
root.geometry("500x600")
root.configure(bg="#333333")

# Style configuration for a dark theme
style = ttk.Style(root)
style.theme_use('clam')
style.configure("TLabel", foreground="white", background="#333333")
style.configure("TCheckbutton", foreground="white", background="#444444", font=('Helvetica', 10))
style.configure("TButton", background="#555555", foreground="white", font=('Helvetica', 12, 'bold'))

# Category frames and variables
message_var = tk.StringVar(value="")
reason_var = tk.StringVar(value="")
warning_var = tk.StringVar(value="")


def create_category_frame(category, options, variable):
    frame = ttk.LabelFrame(root, text=category, style="TLabel")
    for option in options:
        ttk.Radiobutton(frame, text=DESCRIPTIONS[category][option], value=option, variable=variable,
                        style="TCheckbutton").pack(anchor='w', padx=10, pady=2)
    frame.pack(pady=15, fill='x', padx=20)


# Populate the frames with audio options
create_category_frame("Messages", audio_files['Messages'], message_var)
create_category_frame("Reasons", audio_files['Reasons'], reason_var)
create_category_frame("Warnings", audio_files['Warnings'], warning_var)

# TEST ALERT button
ttk.Button(root, text="TEST ALERT", command=on_test_alert, style="TButton").pack(pady=20)

# Start the application
root.mainloop()
