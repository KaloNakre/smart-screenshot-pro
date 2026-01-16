import pyautogui
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from winotify import Notification
import keyboard
import pygetwindow as gw
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
INDEX_FILE = os.path.join(SCREENSHOT_DIR, "index.txt")

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ---------------- UTILITIES ----------------

def get_active_window():
    try:
        win = gw.getActiveWindow()
        return win.title if win else "Unknown_App"
    except:
        return "Unknown_App"

def safe_name(text):
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in text)

def log_entry(data):
    with open(INDEX_FILE, "a", encoding="utf-8") as f:
        f.write(data + "\n" + "-"*60 + "\n")

def open_folder(path):
    subprocess.Popen(f'explorer "{path}"')

# ---------------- SCREENSHOT CORE ----------------

def take_screenshot(region=False):
    app = app_entry.get().strip() or get_active_window()
    page = page_entry.get().strip()
    note = note_entry.get("1.0", tk.END).strip()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    app_folder = os.path.join(SCREENSHOT_DIR, safe_name(app))
    os.makedirs(app_folder, exist_ok=True)

    filename = f"{safe_name(app)}_{timestamp}.png"
    filepath = os.path.join(app_folder, filename)

    if region:
        messagebox.showinfo("Region Select", "Drag to select screen area")
        img = pyautogui.screenshot(region=pyautogui.selectRegion())
        img.save(filepath)
    else:
        pyautogui.screenshot(filepath)

    log_entry(
        f"Time: {timestamp}\n"
        f"App/Website: {app}\n"
        f"Page/ID: {page}\n"
        f"Note: {note}\n"
        f"File: {filepath}"
    )

    Notification(
        app_id="Smart Screenshot Pro",
        title="Screenshot Saved",
        msg=f"{app}",
        duration="short"
    ).show()

    messagebox.showinfo("Success", "Screenshot saved with memory ✅")

# ---------------- SEARCH ----------------

def search_logs():
    keyword = search_entry.get().lower()
    if not os.path.exists(INDEX_FILE):
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = f.read().lower()

    if keyword in data:
        messagebox.showinfo("Found", "Keyword found in screenshot history")
    else:
        messagebox.showwarning("Not Found", "No match found")

# ---------------- HOTKEY ----------------
keyboard.add_hotkey("ctrl+shift+s", lambda: take_screenshot(False))

# ---------------- GUI ----------------

root = tk.Tk()
root.title("Smart Screenshot Pro")
root.geometry("520x520")
root.resizable(False, False)

tk.Label(root, text="App / Website (auto if empty)").pack()
app_entry = tk.Entry(root, width=60)
app_entry.pack(pady=3)

tk.Label(root, text="Page / Path / ID").pack()
page_entry = tk.Entry(root, width=60)
page_entry.pack(pady=3)

tk.Label(root, text="Why did you take this screenshot?").pack()
note_entry = tk.Text(root, height=6, width=58)
note_entry.pack(pady=5)

tk.Button(root, text="📸 Full Screenshot", bg="#0078D7", fg="white",
          font=("Segoe UI", 10, "bold"),
          command=lambda: take_screenshot(False)).pack(pady=5)

tk.Button(root, text="✂️ Region Screenshot", bg="#2D7D46", fg="white",
          font=("Segoe UI", 10, "bold"),
          command=lambda: take_screenshot(True)).pack(pady=5)

tk.Label(root, text="Search Screenshot History").pack(pady=(10, 0))
search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=3)

tk.Button(root, text="🔍 Search", command=search_logs).pack(pady=4)
tk.Button(root, text="📂 Open Screenshot Folder",
          command=lambda: open_folder(SCREENSHOT_DIR)).pack(pady=6)

tk.Label(root, text="Hotkey: Ctrl + Shift + S\nScreenshots with memory, not confusion.",
         fg="gray").pack(pady=10)

root.mainloop()
