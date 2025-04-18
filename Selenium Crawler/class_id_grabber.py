import login
import json
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
from urllib.parse import urlparse, parse_qs
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService  # Changed

CLASS_API_URL = "https://eaen.bc.edu/en-services/services/rest/oauth/activityseatcountservice/activityseatcounts"
SCHEDULE_API_URL = "https://eaen.bc.edu/en-services/services/rest/oauth/schedulingservice/scheduledisplays"
COURSEOFFERING_URL = "https://eaen.bc.edu/en-services/services/rest/oauth/courseofferingservice/activityofferings"
def random_sleep_time():
    return random.random() + 1


def clear_logs(driver):
    """Reads and discards logs to clear the log buffer."""
    _ = driver.get_log("performance")

def extract_courseOffering_from_url(url):
    parsed_url = urlparse(url)  # Parse the URL into components
    query_params = parse_qs(parsed_url.query)  # Parse the query parameters
    return query_params.get("courseOfferingId", [None])[0]  # Get the first value or None

def extract_classid_from_url(url):
    parsed_url = urlparse(url)  # Parse the URL into components
    query_params = parse_qs(parsed_url.query)  # Parse the query parameters
    return query_params.get("activityOfferingId", [None])[0]  # Get the first value or None

def extract_scheduleid_from_url(url):
    parsed_url = urlparse(url)  # Parse the URL into components
    query_params = parse_qs(parsed_url.query)  # Parse the query parameters
    return query_params.get("scheduleIds", [None])[0]  # Get the first value or None

def check_availability(driver, classid, username):
    params = {
        "principalId": username,
        "activityOfferingId": classid,
        "context.applicationId": "angular1x.student-registration",
        "context.moduleId": "en",
        "context.screenId": "student-registration.",
    }
    cookies = driver.get_cookies()
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    API_response = requests.get(CLASS_API_URL, cookies=cookies_dict, params=params)
    if API_response.status_code == 200:
        data = API_response.json()  # Assuming the API returns JSON
        for item in data:
            grabbed_name = item.get("name")
            available_seats = int(item.get("available"))
            
    return grabbed_name, available_seats

def check_schedule(driver, classid, username):
    params = {
        "principalId": username,
        "context.applicationId": "angular1x.student-registration",
        "context.moduleId": "en",
        "context.screenId": "student-registration.",
        "scheduleIds":  classid,
    }
    cookies = driver.get_cookies()
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    API_response = requests.get(SCHEDULE_API_URL, cookies=cookies_dict, params=params)
    if API_response.status_code == 200:
        data = API_response.json()  # Assuming the API returns JSON
        # print(data)
        for item in data:
            place_time = item.get("name")
            

    return place_time

def get_info(driver, courseOfferingId, section, username):
    params = {
        "principalId": username,
        "context.applicationId": "angular1x.student-registration",
        "context.moduleId": "en",
        "context.screenId": "student-registration.",
        "courseOfferingId": courseOfferingId,
    }
    cookies = driver.get_cookies()
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    full_response = requests.get(COURSEOFFERING_URL, cookies=cookies_dict, params=params)
    class_index = section-1
    specific_class = full_response.json()[class_index]

    # Extract the desired fields
    class_id = specific_class.get("id")
    instructors = specific_class.get("instructors", [])
    schedule_ids = specific_class.get("scheduleIds", [])

    class_name, available_seats = check_availability(driver, class_id, username)
    schedule = []
    for times in schedule_ids:
        schedule.append(check_schedule(driver, times, username))
    # Extract the personName of all instructors (if there are multiple)
    instructor_names = [instructor.get("personName") for instructor in instructors]
    return class_name, instructor_names, schedule, class_id

def get_logs(driver, section, username):
    logs = driver.get_log("performance")
    for log in logs:
        try:
            # Parse the log message
            message = json.loads(log["message"])
            message_data = message.get("message")

            # Filter for relevant network events
            if message_data["method"] == "Network.requestWillBeSent":
                request_url = message_data["params"]["request"]["url"]

                # Look for the desired API endpoint
                if "courseofferingservice/activityofferings" in request_url:
                    # print(f"requestURL: {request_url}")
                    courseOfferingId = extract_courseOffering_from_url(request_url).strip()
                    classinfo = get_info(driver, courseOfferingId, section, username)
                    return classinfo
                    # activity_ids.append(courseOfferingId)
        except Exception as e:
            print("Error processing log:", e)

def get_all_info(username, password, className, section):

    # Set up Chrome options
    options = Options()
    # options.add_argument("--headless")  # Enable headless mode
    # options.add_argument("--disable-gpu")  # Disable GPU (recommended for headless mode)
    # options.add_argument("--no-sandbox")  # Bypass OS security model (useful in some environments)
    # options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems in some containers
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # Enable performance logs


    # Service setup
    service = ChromeService(ChromeDriverManager().install())  # Changed
    driver = webdriver.Chrome(service=service, options=options)  # Changed

    try:
        wait = WebDriverWait(driver, 30)

        # Log in to the system
        login.loginer(username, password, driver, wait)

        # Search for the class
        keyword_field = wait.until(
            EC.visibility_of_element_located((By.ID, "seFacetedFiltersViewersearchTextForFilters"))
        )
        keyword_field.send_keys(className)
        keyword_field.send_keys(Keys.RETURN)

        # Expand dropdown
        clear_logs(driver)
        try:
            dropdown_icon = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "i.pull-right.glyphicon.glyphicon-chevron-right"))
            )
            time.sleep(2 + random_sleep_time())
            dropdown_icon.click()
            time.sleep(random_sleep_time())
        except Exception as e:
            raise Exception(f"Class: {className} not found")

        # Get activity offering IDs
        all_class_info = get_logs(driver, section, username)

        if not all_class_info:
            raise Exception(f"Invalid section '{section}' for class '{className}'. Please check the section number.")

        driver.quit()
        return all_class_info

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        raise  # Re-raise the exception after logging

    finally:
        # Ensure the driver is closed
        driver.quit()