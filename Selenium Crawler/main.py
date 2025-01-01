import selenium_crawler  # Import the refactored scraper
import email_sender
import time
import random
# Define your class list (name, section)
classes = [
    ("MATH1103 Calculus II (Mathematics/Science Majors)", 1),
    ("ENGL1010 First Year Writing Seminar", 2),
    ("THEO1422 The Sacred Page: The Bible", 1),
]

USERNAME = "guoale"
PASSWORD = "j2dhdgt7"

def random_sleep_time():
    return random.random()*10.0 + 3.0

def main():
    iteration = 1
    while True:
        print(f"iteration #{iteration}")
        iteration += 1
        selenium_crawler.scrape_class(USERNAME, PASSWORD, classes)
        time.sleep(random_sleep_time())
        

if __name__ == "__main__":
    main()