import random
import requests
import time
import email_sender
from selenium.webdriver.support import expected_conditions as EC

API_URL = "https://eaen.bc.edu/en-services/services/rest/oauth/activityseatcountservice/activityseatcounts"
def random_sleep_time():
    return random.random()*1.0 + 1.0
def scrape_class(classInfo, emailsSent, email, driver):
    # class_name = "Topics in this course include vectors in two"
    # keyword_field = wait.until(
    #     EC.visibility_of_element_located((By.ID, "seFacetedFiltersViewersearchTextForFilters"))
    # )
    # time.sleep(random_sleep_time())
    # keyword_field.send_keys(class_name)
    # keyword_field.send_keys(Keys.RETURN)
    # time.sleep(2 + random_sleep_time())
    try:

        print (emailsSent)
        for classname, instructors, schedules, id in classInfo:
            time.sleep(random_sleep_time())
            params = {
                "principalId": "guoale",
                "activityOfferingId": id,
                "context.applicationId": "angular1x.student-registration",
                "context.moduleId": "en",
                "context.screenId": "student-registration.",
            }
            cookies = driver.get_cookies()
            cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            API_response = requests.get(API_URL, cookies=cookies_dict, params=params)
            if API_response.status_code == 200:
                data = API_response.json()  # Assuming the API returns JSON
                for item in data:
                    grabbed_name = item.get("name")
                    available_seats = int(item.get("available"))
                    print(f"Course: {grabbed_name}, Available Seats: {available_seats}")
                    # print(f"id: {id}")
                    if available_seats > 0 and not emailsSent[id]:
                        email_sender.send_email(email, available_seats, classname, instructors, schedules, True)
                        emailsSent[id] = True
                    if available_seats <= 0 and emailsSent[id]:
                        email_sender.send_email(email, available_seats, classname, instructors, schedules, False)
                        emailsSent[id] = False
    except Exception as e:
        print(f"Error in API request. {e}")
        return