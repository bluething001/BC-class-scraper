import selenium_crawler  # Import the refactored scraper
import email_sender
# Define your class list (name, section)
classes = [
    ("MATH1103 Calculus II (Mathematics/Science Majors)", 1),
    ("ENGL1010 First Year Writing Seminar", 2),
    ("THEO1422 The Sacred Page: The Bible", 1),
]

USERNAME = "guoale"
PASSWORD = "j2dhdgt7"

def main():
    selenium_crawler.scrape_class(USERNAME, PASSWORD, classes)
        

if __name__ == "__main__":
    main()