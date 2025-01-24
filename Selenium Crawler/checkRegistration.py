import random
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

def slow_random_sleep_time():
    return random.random() * 1.0 + 5.0

def fast_random_sleep_time():
    return random.random() + 1.0

def is_valid_email(email):
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_regex, email) is not None

def checkBCLogin(username, password):
    chromeDriverPath = "/opt/homebrew/bin/chromedriver"

    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--disable-gpu")  # Disable GPU (recommended for headless mode)
    options.add_argument("--no-sandbox")  # Bypass OS security model (useful in some environments)
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems in some containers
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # Enable performance logs

    # Service setup
    service = Service(chromeDriverPath)
    driver = webdriver.Chrome(service=service, options=options)

    wait = WebDriverWait(driver, 30)

    url = "https://portal.bc.edu"
    driver.get(url)
    # time.sleep(fast_random_sleep_time())
    username_field = wait.until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    username_field.send_keys(username)

    # time.sleep(fast_random_sleep_time())
    password_field = wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password_field.send_keys(password)

    # time.sleep(fast_random_sleep_time())
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in']"))
    )
    login_button.click()
    time.sleep(fast_random_sleep_time())
    if "https://services.bc.edu/commoncore/myservices.do" in driver.current_url:
        driver.quit()
        return 1  # Logged in successfully
    else:
        driver.quit()
        return 0
    


