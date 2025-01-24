import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException

def slow_random_sleep_time():
    return random.random() * 1.0 + 5.0

def fast_random_sleep_time():
    return random.random() + 1.0

def loginer(username, password, driver, wait):
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

    # time.sleep(fast_random_sleep_time())
    wait.until(EC.url_contains("myservices.do"))
    final_url = "https://services.bc.edu/password/external/launcher/generic.do?id=eaPlanningRegistration"
    driver.get(final_url)
    
    time.sleep(slow_random_sleep_time())
    while True:
        try:
            tab_element = wait.until(
                EC.element_to_be_clickable((By.ID, "mySchedule"))
            )
            tab_element.click()
            break  # Exit loop if successful
        except StaleElementReferenceException:
            print("Element went stale, retrying...")


