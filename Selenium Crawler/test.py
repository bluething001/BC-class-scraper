import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import class_seats


def scrape_class(class_name, section, username, password):
    # Path to ChromeDriver
    chromeDriverPath = "/opt/homebrew/bin/chromedriver"

    # Set up Chrome options
    options = Options()

    # Create a Service object
    service = Service(chromeDriverPath)

    # Launch Chrome
    driver = webdriver.Chrome(service=service, options=options)

    # Initialize WebDriverWait
    wait = WebDriverWait(driver, 20)

    try:
        # Navigate to the login URL
        url = "https://portal.bc.edu"
        driver.get(url)

        # Wait for the username field and input credentials
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
        username_field.send_keys(username)

        password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password_field.send_keys(password)

        # Click the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in']")))
        time.sleep(2)
        login_button.click()

        # Navigate to the courses page
        wait.until(EC.url_contains("myservices.do"))
        final_url = "https://services.bc.edu/password/external/launcher/generic.do?id=eaPlanningRegistration"
        time.sleep(2)
        driver.get(final_url)

        # Wait for the courses tab and click it
        tab_element = wait.until(EC.element_to_be_clickable((By.ID, "mySchedule")))
        time.sleep(2)
        tab_element.click()

        # Search for the class and get availability
        elements = class_seats.find_availability(class_name, section, driver, wait)

        seats = int(elements[2])
        filled = int(elements[0])
        print(f"Class: {class_name}, Section: {section} -> Filled: {filled}, Seats: {seats}")

        return filled, seats

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

    finally:
        time.sleep(2)
        driver.quit()