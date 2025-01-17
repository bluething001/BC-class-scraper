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
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


def random_sleep_time():
    return random.random() * 1.0 + 2.0

def loginer(username, password, driver, wait):
    url = "https://portal.bc.edu"
    driver.get(url)
    
    username_field = wait.until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    time.sleep(random_sleep_time())
    username_field.send_keys(username)

    password_field = wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    time.sleep(random_sleep_time())
    password_field.send_keys(password)

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in']"))
    )
    time.sleep(random_sleep_time())
    login_button.click()

    wait.until(EC.url_contains("myservices.do"))
    final_url = "https://services.bc.edu/password/external/launcher/generic.do?id=eaPlanningRegistration"
    time.sleep(random_sleep_time())
    driver.get(final_url)

    while True:
        try:
            tab_element = wait.until(
                EC.element_to_be_clickable((By.ID, "mySchedule"))
            )
            tab_element.click()
            time.sleep(1)
            tab_element.click()
            break  # Exit loop if successful
        except StaleElementReferenceException:
            print("Element went stale, retrying...")

