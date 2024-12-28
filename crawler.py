import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import re

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -----------------------------------------
# Configuration
# -----------------------------------------
PORTAL_PAGE = "https://portal.bc.edu/"
REGISTRATION_LINK = "https://services.bc.edu/password/external/launcher/generic.do?id=eaPlanningRegistration"

CLASS_PAGE_URL = "https://eaen.bc.edu/student-registration/#/"
USERNAME = "guoale"
PASSWORD = "j2dhdgt7"

# The selector or pattern used to identify classes on the page
CLASS_CONTAINER_SELECTOR = "div.class-item"  # Example CSS selector
CLASS_NAME_SELECTOR = "h3.class-title"       # Example CSS selector inside the container
CLASS_AVAILABILITY_SELECTOR = "span.availability" # Example CSS selector inside the container

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "alexguo05@gmail.com"
EMAIL_PASSWORD = "Iam@gm159669"  # Consider using an app password or environment variable
EMAIL_RECIPIENT = "alexguo05@gmail.com"
EMAIL_SUBJECT = "Class Availability Notification"

# -----------------------------------------
# Helper Functions
# -----------------------------------------
def login(session, username, password):

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    # 1) First GET - portal.bc.edu
    portal_resp = session.get(PORTAL_PAGE, allow_redirects=False)
    print("resp1 status:", portal_resp.status_code)  # likely 302
    print("resp1 location:", portal_resp.headers.get('Location'))

    # 2) Follow the redirect from resp1 manually
    service_link = portal_resp.headers.get('Location')
    service_resp = session.get(service_link, allow_redirects=False)
    print("resp2 status:", service_resp.status_code)  # likely 302
    print("resp2 location:", service_resp.headers.get('Location'))

    # 3) Next redirect
    plogin_link = service_resp.headers.get('Location')
    plogin_resp = session.get(plogin_link, allow_redirects=False)
    print("resp3 status:", plogin_resp.status_code)  # might be 302 again or maybe 200
    print("resp3 location:", plogin_resp.headers.get('Location'))

    # 4th get
    login_get_link = plogin_resp.headers.get('Location')
    login_get_resp = session.get(login_get_link)
    print("resp4 status:", login_get_resp.status_code)
    print("resp4 location:", login_get_resp.headers.get('Location'))
    print("resp4 text:")
    print(login_get_resp.text)

    # get next link from form data
    login_get_text = login_get_resp.text
    login_get_soup = BeautifulSoup(login_get_text, 'html.parser')
    login_get_form = login_get_soup.find('form', attrs={'method': 'POST'})
    print(login_get_form)
    login_get_action = login_get_form.get('action')
    login_page_link = urljoin(login_get_resp.url, login_get_action)
    
    # 1st post to login page (response is the page)
    login_page_resp = session.post(login_page_link)
    print("resp5 status:", login_page_resp.status_code)
    print("resp5 location:", login_page_resp.headers.get('Location'))
    print("resp5 text:")
    print(login_page_resp.text)
    
    # parse for next link
    login_page_text = login_page_resp.text
    login_page_soup = BeautifulSoup(login_page_text, 'html.parser')

    login_page_form = login_page_soup.find('form', attrs={'method': 'POST'})
    if not login_page_form:
        print("No POST form found on login page. Check if there's an error or different HTML structure.")
        return
    
    login_page_action = login_page_form.get('action')
    send_payload_link = urljoin(login_page_resp.url, login_page_action)

    print("send_payload_link")
    print(send_payload_link)
    # Build a dictionary of ALL inputs in the form (hidden or visible)
    payload = {}
    all_inputs = login_page_form.find_all('input')
    for inp in all_inputs:
        name = inp.get('name')
        value = inp.get('value', '')
        if name:  
            payload[name] = value
    
    # Now add your username/password fields 
    # (in your code, they are 'Ecom_User_ID' and 'Ecom_Password')
    payload['Ecom_User_ID'] = username
    payload['Ecom_Password'] = password
    
    # Print payload for debugging
    print("Form submission payload:", payload)

    after_login_resp = session.post(send_payload_link, data=payload, allow_redirects=False)
    print("after_login_resp status:", after_login_resp.status_code)
    print("after_login_resp location:", after_login_resp.headers.get('Location'))
    print("after_login_resp text:", after_login_resp.text)


    # get request after payload
    after_login_get = session.get(send_payload_link, allow_redirects=False)
    print("after_login_get status:", after_login_get.status_code)
    print("after_login_get location:", after_login_get.headers.get('Location'))
    print("after_login_get text:", after_login_get.text)

    # get next link with form
    after_login_get_text = after_login_get.text
    after_login_get_soup = BeautifulSoup(after_login_get_text, 'html.parser')
    after_login_get_form = after_login_get_soup.find('form', attrs={'method': 'POST'})
    print(after_login_get_form)
    after_login_get_action = after_login_get_form.get('action')
    after_login_page_link = urljoin(after_login_get.url, login_get_action)
    print("after_login_page_link")
    print(after_login_page_link)

    #FINAL POST

    final_post_resp = session.post(after_login_page_link, allow_redirects=False)
    print("final_post_resp status:", final_post_resp.status_code)
    print("final_post_resp location:", final_post_resp.headers.get('Location'))
    print("final_post_resp text:", final_post_resp.text)

    #To the Finish!
    js_redirect_page = after_login_resp.text
    pattern = r"window.location.href\s*=\s*'([^']+)'"
    match = re.search(pattern, js_redirect_page)
    if match:
        redirect_url = match.group(1)
        print("Found JavaScript redirect:", redirect_url)
    else:
        print("No JavaScript redirect found.")
    
    final_page = session.post(redirect_url, allow_redirects=True)
    print("final_page status:", final_page.status_code)
    print("final_page location:", final_page.headers.get('Location'))
    print("final_page text:", final_page.text)

    registration_page = session.get(REGISTRATION_LINK)
    print("registration_page status:", registration_page.status_code)
    print("registration_page location:", registration_page.headers.get('Location'))
    print("registration_page text:", registration_page.text)
    
    class_page = session.get(CLASS_PAGE_URL)
    print("class_page status:", class_page.status_code)
    print("class_page location:", class_page.headers.get('Location'))
    print("class_page text:", class_page.text)
    #
    #
    
# -----------------------------------------
# Main Execution
# -----------------------------------------
if __name__ == "__main__":
    with requests.Session() as session:
        # Login first
        login(session, USERNAME, PASSWORD)
