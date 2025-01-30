import os
import json
import random

CLASSES_FILE = "classes.json"

def load_classes():
    if os.path.exists(CLASSES_FILE):
        with open(CLASSES_FILE, "r") as file:
            return json.load(file)
    return []

def save_classes(classes):
    with open(CLASSES_FILE, "w") as file:
        json.dump(classes, file, indent=4)

def random_sleep_time():
    return random.random() * 1.0 + 2.0