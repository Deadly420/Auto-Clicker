import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import pyautogui
import threading
import time
import keyboard  # For hotkey functionality

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class AutoClickerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto Clicker")
        self.geometry("300x250")
        self.resizable(False, False)

        self.clicking = False
        self.click_interval = 1.0  # Default interval in seconds

        # Create GUI elements
        self.label = ctk.CTkLabel(self, text="Auto Clicker", font=("Arial", 16))
        self.label.pack(pady=10)

        self.interval_label = ctk.CTkLabel(self, text="Click Interval (seconds):")
        self.interval_label.pack()

        self.interval_entry = ctk.CTkEntry(self)
        self.interval_entry.insert(0, "1.0")
        self.interval_entry.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="Start (F6)", command=self.start_clicking)
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self, text="Stop (F7)", command=self.stop_clicking, state=ctk.DISABLED)
        self.stop_button.pack(pady=10)

        self.hotkey_label = ctk.CTkLabel(self, text="Hotkeys: F6 to Start, F7 to Stop", font=("Arial", 12))
        self.hotkey_label.pack(pady=10)

        # Set up hotkeys
        keyboard.add_hotkey("F6", self.start_clicking)
        keyboard.add_hotkey("F7", self.stop_clicking)

    def start_clicking(self):
        try:
            self.click_interval = float(self.interval_entry.get())
            if self.click_interval <= 0:
                raise ValueError("Interval must be greater than 0")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        if not self.clicking:
            self.clicking = True
            self.start_button.configure(state=ctk.DISABLED)
            self.stop_button.configure(state=ctk.NORMAL)

            # Start the auto-clicker in a separate thread
            self.click_thread = threading.Thread(target=self.auto_click)
            self.click_thread.start()

    def stop_clicking(self):
        if self.clicking:
            self.clicking = False
            self.start_button.configure(state=ctk.NORMAL)
            self.stop_button.configure(state=ctk.DISABLED)

    def auto_click(self):
        while self.clicking:
            pyautogui.click()
            time.sleep(self.click_interval)

if __name__ == "__main__":
    app = AutoClickerApp()
    app.mainloop()
