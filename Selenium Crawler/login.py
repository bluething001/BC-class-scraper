import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def slow_random_sleep_time():
    return random.random() * 5.0 + 10.0

def fast_random_sleep_time():
    return random.random() * 1.0 + 1.0

MAX_RETRIES = 10
def retry_find_element(driver, by, value, retries=MAX_RETRIES, sleep_time=0.5):
    for _ in range(retries):
        try:
            return driver.find_element(by, value)
        except NoSuchElementException:
            time.sleep(sleep_time)
    raise NoSuchElementException(f"Element not found: {value}")

def loginer(username, password, driver):
    url = "https://portal.bc.edu"
    driver.get(url)
    # time.sleep(fast_random_sleep_time())
    # Locate username field and input username
    username_field = retry_find_element(driver, By.ID, "username")
    username_field.send_keys(username)


    password_field = retry_find_element(driver, By.ID, "password")
    password_field.send_keys(password)

    login_button = retry_find_element(driver, By.XPATH, "//button[text()='Sign in']")
    login_button.click()

    time.sleep(fast_random_sleep_time())

    # Wait for the URL to change (or implement a simple URL check loop)
    final_url = "https://services.bc.edu/password/external/launcher/generic.do?id=eaPlanningRegistration"

    driver.get(final_url)

    time.sleep(slow_random_sleep_time())

    tab_element = retry_find_element(driver, By.ID, "mySchedule")
    tab_element.click()

