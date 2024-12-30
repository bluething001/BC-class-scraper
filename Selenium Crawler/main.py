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
    for class_name, section in classes:
        print(f"Checking availability for {class_name}, Section {section}...")
        filled, seats = selenium_crawler.scrape_class(class_name, section, USERNAME, PASSWORD)
        
        # Add logic to send an email if seats are available
        if seats is not None and filled is not None and seats > filled:
            print(f"Seats available for {class_name}, Section {section}!")
            email_sender.send_email(filled, seats, class_name, section)
        else:
            print(f"Seats for class {class_name}, section {section} are full")
        print()
        

if __name__ == "__main__":
    main()