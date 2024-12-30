import os
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
    return random.random()

def scrape_class(class_name, section, username, password):
    chromeDriverPath = "/opt/homebrew/bin/chromedriver"

    options = Options()
    
    service = Service(chromeDriverPath)

    driver = webdriver.Chrome(service=service, options=options)

    wait = WebDriverWait(driver, 20)  # 20 seconds timeout

    try:
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

        tab_element = wait.until(
            EC.element_to_be_clickable((By.ID, "mySchedule"))
        )
        time.sleep(random_sleep_time() + 3)
        tab_element.click()

        #currently in courses, nothing searched yet
        elements = class_seats.find_availability(class_name, section, driver, wait)
        elements = elements.split(' ')
        del elements[1]
        return elements

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()