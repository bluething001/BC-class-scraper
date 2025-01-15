import selenium_crawler  # Import the refactored scraper
import login
import tkinter as tk
from tkinter import messagebox
import threading
import random
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException


# Define the file to save classes
CLASSES_FILE = "classes.json"

# Global variable to control the scraper thread
stop_thread = False

def random_sleep_time():
    return random.random() * 1.0 + 2.0

def load_classes():
    """Load classes from a JSON file."""
    if os.path.exists(CLASSES_FILE):
        with open(CLASSES_FILE, "r") as file:
            return json.load(file)
    return []

def save_classes():
    """Save classes to a JSON file."""
    with open(CLASSES_FILE, "w") as file:
        json.dump(classes, file, indent=4)

def run_scraper(username, password):
    global stop_thread

    chromeDriverPath = os.environ.get("CHROMEDRIVER")

    options = Options()

    service = Service(chromeDriverPath)

    driver = webdriver.Chrome(service=service, options=options)

    wait = WebDriverWait(driver, 30)

    

    # time.sleep(50)
    iteration = 1
    while not stop_thread:
        if iteration%10 == 1:
            login.loginer(username, password, driver, wait)
        print(f"Iteration #{iteration}")
        iteration += 1
        selenium_crawler.scrape_class(username, password, classes, driver, wait)
        time.sleep(random_sleep_time())
    driver.quit()
    print("Scraper stopped.")

def start_scraper():
    global stop_thread
    stop_thread = False  # Reset the stop flag

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    # Disable the input fields and button after starting the scraper
    username_entry.config(state="disabled")
    password_entry.config(state="disabled")
    start_button.config(state="disabled")
    add_class_button.config(state="disabled")
    stop_button.config(state="normal")  # Enable stop button

    # Start the scraper in a separate thread
    scraper_thread = threading.Thread(target=run_scraper, args=(username, password))
    scraper_thread.daemon = True  # Ensure the thread exits when the main program ends
    scraper_thread.start()

def stop_scraper():
    global stop_thread
    stop_thread = True

    # Re-enable input fields and buttons
    username_entry.config(state="normal")
    password_entry.config(state="normal")
    start_button.config(state="normal")
    add_class_button.config(state="normal")
    stop_button.config(state="disabled")  # Disable stop button

    print("Stopping the scraper...")

def add_class():
    class_name = class_name_entry.get().strip()
    section = section_entry.get().strip()

    if not class_name or not section:
        messagebox.showerror("Error", "Please enter both class name and section.")
        return

    try:
        section = int(section)
    except ValueError:
        messagebox.showerror("Error", "Section must be a number.")
        return

    classes.append((class_name, section))
    class_listbox.insert(tk.END, f"{class_name} (Section {section})")

    # Save the updated classes list
    save_classes()

    # Clear input fields
    class_name_entry.delete(0, tk.END)
    section_entry.delete(0, tk.END)

def remove_selected_class():
    selected_index = class_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Warning", "Please select a class to remove.")
        return

    # Remove class from the list and listbox
    classes.pop(selected_index[0])
    class_listbox.delete(selected_index)

    # Save the updated classes list
    save_classes()

# Load classes from the file
classes = load_classes()

# Create the main Tkinter window
window = tk.Tk()
window.title("Class Scraper Login")

# Username label and entry
username_label = tk.Label(window, text="Username:")
username_label.pack(pady=5)
username_entry = tk.Entry(window, width=30)
username_entry.pack(pady=5)

# Password label and entry
password_label = tk.Label(window, text="Password:")
password_label.pack(pady=5)
password_entry = tk.Entry(window, show="*", width=30)
password_entry.pack(pady=5)

class_name_label = tk.Label(window, text="Class Name:")
class_name_label.pack(pady=5)
class_name_entry = tk.Entry(window, width=30)
class_name_entry.pack(pady=5)

section_label = tk.Label(window, text="Section:")
section_label.pack(pady=5)
section_entry = tk.Entry(window, width=30)
section_entry.pack(pady=5)

add_class_button = tk.Button(window, text="Add Class", command=add_class)
add_class_button.pack(pady=5)

# Class listbox
class_listbox = tk.Listbox(window, width=50, height=10)
class_listbox.pack(pady=5)

# Populate the listbox with saved classes
for class_name, section in classes:
    class_listbox.insert(tk.END, f"{class_name} (Section {section})")

# Remove selected class button
remove_class_button = tk.Button(window, text="Remove Selected Class", command=remove_selected_class)
remove_class_button.pack(pady=5)

# Start button
start_button = tk.Button(window, text="Start Scraper", command=start_scraper)
start_button.pack(pady=10)

stop_button = tk.Button(window, text="Stop Scraper", command=stop_scraper, state="disabled")
stop_button.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()