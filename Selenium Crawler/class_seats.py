import os
import time
import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

BASE_SECTION_ID = "courseOfferingSearchCtrl.tableIdAOName"
BASE_AVAILABLE_ID = "courseOfferingSearchCtrl.tableIdRegistered-"
BASE_FULL_ID = "courseOfferingSearchCtrl.tableIdPopover-"

def random_sleep_time():
    return random.random()*1.0 + 2.0

def find_availability(class_name, section, driver, wait):
    keyword_field = wait.until(
        EC.visibility_of_element_located((By.ID, "seFacetedFiltersViewersearchTextForFilters"))
    )
    time.sleep(random_sleep_time())
    keyword_field.send_keys(class_name)
    keyword_field.send_keys(Keys.RETURN)
    time.sleep(4 + random_sleep_time())
    # hit dropdown
    dropdown_icon = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.pull-right.glyphicon.glyphicon-chevron-right"))
    )
    dropdown_icon.click()
    time.sleep(random_sleep_time())

    zero_indexed_section = section-1
    section_id = f"{BASE_SECTION_ID}{zero_indexed_section}{zero_indexed_section}"
    availabile_id = f"{BASE_AVAILABLE_ID}{zero_indexed_section}{zero_indexed_section}"
    full_id = f"{BASE_FULL_ID}{zero_indexed_section}{zero_indexed_section}"


    try:
        section = wait.until(
            EC.visibility_of_element_located((By.ID, section_id))
        )
        section_text = section.text
    except Exception:
        print(f"No class found with ID: {section_id}.")
        
    try:
        available_class_element = wait.until(
            EC.visibility_of_element_located((By.ID, availabile_id))
        )
        available_class_text = available_class_element.text # maybe add .strip() if needed
        # print(f"Found availability: {available_class_text}.")
        return available_class_text
    except Exception:
        try: 
            full_class_element = wait.until(
                EC.visibility_of_element_located((By.ID, full_id))
            )
            full_class_text = full_class_element.text
            # print(f"Class is full: {full_class_text}")
            return full_class_text
        except Exception:
            print(f"Error: unable to grab availability")
    
    
        
