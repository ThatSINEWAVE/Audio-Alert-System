import tkinter as tk
from tkinter import ttk, messagebox
import os
import time
import logging
from threading import Thread
from pygame import mixer
import customtkinter as ctk

# Constants
AUDIO_DIR = {
    'Messages': 'audio/Messages',
    'Reasons': 'audio/Reasons',
    'Warnings': 'audio/Warnings'
}

DESCRIPTIONS = {
    'Messages': {
        'Program completed.mp3': 'PROGRAM COMPLETED',
        'Program stopped.mp3': 'PROGRAM STOPPED',
        'Program crashed.mp3': 'PROGRAM FAILED',
        'Program started.mp3': 'PROGRAM STARTED'
    },
    'Reasons': {
        'Potential crash.mp3': 'POTENTIAL CRASH',
        'Stopped by user.mp3': 'STOPPED BY USER',
        'System error.mp3': 'SYSTEM ERROR',
        'Task completed.mp3': 'TASK COMPLETED',
        'Task failed.mp3': 'TASK FAILED',
        'Unknown.mp3': 'UNKNOWN ISSUE'
    },
    'Warnings': {
        'Abnormal_activity.mp3': 'ABNORMAL ACTIVITY',
        'Critical_error.mp3': 'CRITICAL ERROR',
        'Execution_error.mp3': 'EXECUTION ERROR',
        'Fatal_error.mp3': 'FATAL ERROR',
        'System_warning.mp3': 'SYSTEM WARNING',
        'Unusual_activity.mp3': 'UNUSUAL ACTIVITY',
        'Warning.mp3': 'GENERAL WARNING'
    }
}

PLAY_DELAY = 500

# Logging
LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'log.txt')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def log_event(message):
    logging.info(message)


mixer.init()


def load_audio_files():
    audio_files = {}
    for category, path in AUDIO_DIR.items():
        try:
            files = [f for f in os.listdir(path) if f.endswith('.mp3')]
            audio_files[category] = files
        except FileNotFoundError:
            messagebox.showerror("Error", f"Directory not found: {path}")
            audio_files[category] = []
    return audio_files


class ModernAudioTester:
    def __init__(self):
        self.audio_files = load_audio_files()
        self.setup_window()
        self.create_variables()
        self.create_ui()

    def setup_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Audio Alert Tester")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.root.grid_columnconfigure((0, 1, 2), weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def create_variables(self):
        self.message_var = tk.StringVar(value="")
        self.reason_var = tk.StringVar(value="")
        self.warning_var = tk.StringVar(value="")

        # Store the last selected values
        self.last_selected = {'Messages': "", 'Reasons': "", 'Warnings': ""}

    def create_ui(self):
        # Title
        title_label = ctk.CTkLabel(
            self.root, text="Audio Alert Tester", font=("Helvetica", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(20, 30), padx=20, sticky="ew")

        # Create category frames side by side
        self.create_category_frame("Warnings", self.audio_files['Warnings'], self.warning_var, "#FF6B6B", 0)
        self.create_category_frame("Messages", self.audio_files['Messages'], self.message_var, "#4ECDC4", 1)
        self.create_category_frame("Reasons", self.audio_files['Reasons'], self.reason_var, "#45B7D1", 2)

        # Controls frame at the bottom
        controls_frame = ctk.CTkFrame(self.root)
        controls_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=(20, 10))
        controls_frame.grid_columnconfigure(0, weight=1)

        # Test button
        self.test_button = ctk.CTkButton(
            controls_frame,
            text="Test Alert Sequence", font=("Helvetica", 16, "bold"), command=self.on_test_alert, height=40, width=200)
        self.test_button.grid(row=0, column=0, pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(
            controls_frame, text="Select alerts to test", font=("Helvetica", 12))
        self.status_label.grid(row=1, column=0, pady=(0, 10))

    def handle_radio_click(self, category, variable, value):
        # If clicking the same radio button that's already selected, deselect it
        if self.last_selected[category] == value:
            variable.set("")
            self.last_selected[category] = ""
        else:
            self.last_selected[category] = value

    def create_category_frame(self, category, options, variable, color, column):
        # Create main frame for category with reduced width
        frame = ctk.CTkFrame(self.root)
        frame.grid(row=1, column=column, pady=10, padx=5, sticky="nsew")  # Reduced padx from 10 to 5

        # Category header
        header = ctk.CTkLabel(frame, text=category, font=("Helvetica", 18, "bold"), text_color=color)
        header.grid(row=0, pady=(10, 5), padx=10)

        # Add radio buttons
        for idx, option in enumerate(sorted(options)):
            radio = ctk.CTkRadioButton(frame, text=DESCRIPTIONS[category][option], variable=variable, value=option, font=("Helvetica", 12), command=lambda c=category, v=variable, o=option: self.handle_radio_click(c, v, o))
            radio.grid(row=idx+1, column=0, pady=5, padx=8, sticky="w")  # Reduced padx from 10 to 8

    def play_alert_sequence(self, selected_files):
        play_order = ['Warnings', 'Messages', 'Reasons']
        self.test_button.configure(state="disabled", text="Playing...")
        self.status_label.configure(text="Playing sequence...")

        # Only play selected categories
        played_count = 0
        for category in play_order:
            file = selected_files.get(category)
            if file:
                filepath = os.path.join(AUDIO_DIR[category], file)
                try:
                    sound = mixer.Sound(filepath)
                    log_event(f"Playing {category} alert: {DESCRIPTIONS[category][file]}")
                    sound.play()
                    played_count += 1
                    while mixer.get_busy():
                        time.sleep(0.1)
                    time.sleep(PLAY_DELAY / 1000)
                except Exception as e:
                    log_event(f"Error playing {file}: {e}")
                    messagebox.showerror("Playback Error", f"Could not play {file}: {e}")

        self.test_button.configure(state="normal", text="Test Alert Sequence")
        self.status_label.configure(text=f"Played {played_count} alert{'s' if played_count != 1 else ''}")

    def on_test_alert(self):
        selected_files = {'Messages': self.message_var.get(), 'Reasons': self.reason_var.get(), 'Warnings': self.warning_var.get()}

        # Check if at least one category is selected
        if not any(selected_files.values()):
            self.status_label.configure(text="Please select at least one alert")
            return

        # Filter out unselected categories
        selected_files = {k: v for k, v in selected_files.items() if v}

        combination = ", ".join(DESCRIPTIONS[category][file]
                                for category, file in selected_files.items())
        log_event(f"Test Alert triggered with combination: {combination}")
        Thread(target=self.play_alert_sequence, args=(selected_files,)).start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernAudioTester()
    app.run()
