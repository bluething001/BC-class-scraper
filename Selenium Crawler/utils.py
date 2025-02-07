import os
import json
import random

CLASSES_FILE = "classes.json"

def load_classes():
    if os.path.exists(CLASSES_FILE):
        with open(CLASSES_FILE, "r") as file:
            return json.load(file)
    return []

def init_emailsSent(classes):
    return {class_entry[3]: False for class_entry in classes}

def save_classes(classes):
    with open(CLASSES_FILE, "w") as file:
        json.dump(classes, file, indent=4)

def random_sleep_time():
    return random.random() * 1.0 + 2.0