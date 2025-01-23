import login
import api_requester
import class_id_grabber
import tkinter as tk
from tkinter import messagebox
import threading
import random
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait


def random_sleep_time():
    return random.random() * 1.0 + 2.0

classInfo = ["PHYS2201 Introductory Physics II (Calculus)", 1]

# def run_scraper(username, password):

#     chromeDriverPath = "/opt/homebrew/bin/chromedriver"

#     options = Options()

#     service = Service(chromeDriverPath)
#     driver = webdriver.Chrome(service=service, options=options)
#     wait = WebDriverWait(driver, 30)
#     login.loginer(username, password, driver, wait)
#     # time.sleep(50)
#     iteration = 1
#     while True:
#         if iteration%10 == 0:
#             print("REFRESHING...")
#             driver.quit()
#             time.sleep(random_sleep_time())
#             driver = webdriver.Chrome(service=service, options=options)
#             wait = WebDriverWait(driver, 30)
#             login.loginer(username, password, driver, wait)

#         print(f"Iteration #{iteration}")
#         iteration += 1
#         api_requester.scrape_class(classes, driver, wait)
#         time.sleep(random_sleep_time()+150)
#     driver.quit()
#     print("Scraper stopped.")

classdata = class_id_grabber.get_all_info("guoale", "j2dhdgt7", classInfo)
print(classdata)