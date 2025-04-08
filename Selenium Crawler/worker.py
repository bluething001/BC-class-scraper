from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService  # Renamed
from webdriver_manager.chrome import ChromeDriverManager  # Import
from selenium.webdriver.support.ui import WebDriverWait
import os
import login
import api_requester
import time
from PyQt5.QtWidgets import QApplication
class ClassAddWorker(QObject):
    finished = pyqtSignal(str, list, list, str)  # We emit the results: (grabbed_name, instructors, schedule, apiID)
    error = pyqtSignal(str)  # Optionally signal errors

    def __init__(self, class_name, section, username, password, existing_classes, parent=None):
        super().__init__(parent)        
        self.class_name = class_name
        self.section = section
        self.username = username
        self.password = password
        self.existing_classes = existing_classes

    @pyqtSlot()
    def run(self):
        """Long-running operation: calls class_id_grabber.get_all_info()."""
        try:
            import class_id_grabber  # or from your code
            grabbed_name, instructors, schedule, apiID = class_id_grabber.get_all_info(
                self.username, self.password, self.class_name, self.section
            )
            if any(apiID == existing_apiID for _, _, _, existing_apiID in self.existing_classes):
                self.error.emit("Class already exists")
            else:
                self.finished.emit(grabbed_name, instructors, schedule, apiID)
        except Exception as e:
            # Emit an error signal with the error message
            self.error.emit(str(e))

class ScraperWorker(QObject):
    progress = pyqtSignal(str)  # Signal to send progress messages
    error = pyqtSignal(str)     # Signal to send error messages
    finished = pyqtSignal()     # Signal when the scraper finishes

    def __init__(self, username, password, email, classes, emailsSent, parent=None):
        super().__init__(parent)
        self.username = username
        self.password = password
        self.email = email
        self.classes = classes
        self.emailsSent = emailsSent
        self.stop_thread = False

    # @pyqtSlot()
    def stop_scraper_worker(self):
        """Stop the worker gracefully."""
        self.stop_thread = True
        print("stop_thread set to true")

    def run(self):
        """Run the scraping logic in this thread."""
        try:
            # Set up Selenium
            options = webdriver.ChromeOptions()
            # options.add_argument("--headless")
            # options.add_argument("--disable-gpu")  # Disable GPU (recommended for headless mode)
            # options.add_argument("--no-sandbox")  # Bypass OS security model (useful in some environments)
            # options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems in some containers
            options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # Enable performance logs
            service = ChromeService(ChromeDriverManager().install())  # Use ChromeDriverManager
            driver = webdriver.Chrome(service=service, options=options)
            wait = WebDriverWait(driver, 10)
            
            iteration = 1
            while not self.stop_thread:
                print()
                print(f"iteration: {iteration}")
                # Emit progress
                self.progress.emit(f"BC Availbility Checker is currently running!")
                # Replace this with your scraper logic
                time.sleep(1)  # Simulating work
                if iteration % 10 == 1:
                    # self.progress.emit("Refreshing session...")
                    driver.quit()
                    service = ChromeService(ChromeDriverManager().install())  # New driver!
                    driver = webdriver.Chrome(service=service, options=options)
                    wait = WebDriverWait(driver, 10)
                    try:
                        login.loginer(self.username, self.password, driver, wait)
                    except Exception as e:
                        self.error.emit(str(e))
                        break

                iteration += 1
                try:
                    api_requester.scrape_class(self.classes, self.emailsSent, self.email, driver)
                except Exception:
                    driver.quit()
                    driver = webdriver.Chrome(service=service, options=options)
                    wait = WebDriverWait(driver, 10)
                    try:
                        login.loginer(self.username, self.password, driver, wait)
                    except Exception as e:
                        self.error.emit(str(e))
                        break
                    
                # Emit progress for scraping success
                # self.progress.emit(f"Iteration #{iteration}: Scraping completed.")

                # Simulate scraping delay
                stopped = False
                for _ in range(60):
                    QApplication.processEvents()
                    if self.stop_thread:
                        stopped = True
                        break
                    time.sleep(1)
                if stopped:
                    break

        except Exception as e:
            self.error.emit(str(e))  # Emit error signal if something goes wrong
        finally:
            if driver:  # Ensure driver is quit even if initialization fails
                driver.quit()
            self.finished.emit()  # Emit finished signal when done