from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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

    def __init__(self, username, password, classes, parent=None):
        super().__init__(parent)
        self.username = username
        self.password = password
        self.classes = classes
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
            chromeDriverPath = os.environ.get("CHROMEDRIVER")
            options = webdriver.ChromeOptions()
            service = Service(chromeDriverPath)
            driver = webdriver.Chrome(service=service, options=options)
            wait = WebDriverWait(driver, 30)
            iteration = 1
            while not self.stop_thread:
                # Emit progress
                self.progress.emit(f"BC Availbility Checker is currently running!")
                # Replace this with your scraper logic
                time.sleep(1)  # Simulating work
                if iteration % 10 == 1:
                    # self.progress.emit("Refreshing session...")
                    driver.quit()
                    driver = webdriver.Chrome(service=service, options=options)
                    wait = WebDriverWait(driver, 30)
                    try:
                        login.loginer(self.username, self.password, driver, wait)
                    except Exception as e:
                        self.error.emit("Invalid BC Login")
                        break

                iteration += 1

                api_requester.scrape_class(self.classes, driver)

                # Emit progress for scraping success
                # self.progress.emit(f"Iteration #{iteration}: Scraping completed.")

                # Simulate scraping delay
                stopped = False
                for _ in range(10):
                    QApplication.processEvents()
                    if self.stop_thread:
                        stopped = True
                        break
                    time.sleep(0.1)
                if stopped:
                    break

        except Exception as e:
            self.error.emit(str(e))  # Emit error signal if something goes wrong
        finally:
            driver.quit()
            self.finished.emit()  # Emit finished signal when done