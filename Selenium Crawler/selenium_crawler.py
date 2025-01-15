import os
import login
import time
import re
import email_sender
import class_seats
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def random_sleep_time():
    return random.random()*1.0 + 2.0

def scrape_class(username, password, classes, driver, wait):
    try:
        for class_name, section in classes:
            print(f"Checking availability for {class_name}, Section {section}...")
            elements = class_seats.find_availability(class_name, section, driver, wait)
            elements = elements.split(' ')
            del elements[1]
            filled = int(elements[0])
            seats = int(elements[1])
            # Add logic to send an email if seats are available
            if seats is not None and filled is not None and seats > filled:
                print(f"Seats available for {class_name}, Section {section}!")
                email_sender.send_email(filled, seats, class_name, section)
            else:
                print(f"Seats for class {class_name}, section {section} are full")
            print()
            
            clearfilter = wait.until(
                EC.element_to_be_clickable((By.ID, "seFacetedFiltersViewerClearAllFilters"))
            )
            time.sleep(random_sleep_time())
            clearfilter.click()
            time.sleep(random_sleep_time() + 1)

            

    except Exception as e:
        try: 
            clearfilter = wait.until(
                EC.element_to_be_clickable((By.ID, "seFacetedFiltersViewerClearAllFilters"))
            )
            time.sleep(random_sleep_time())
            clearfilter.click()
        except Exception as e:
            try:
                login.loginer(username, password, driver, wait)
            except Exception as e:
                print(f"An error occurred: {e}")
