import os
import threading
import time
import login
import api_requester
import threading
import time
import os
import worker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from worker import ClassAddWorker
from utils import load_classes, save_classes, random_sleep_time
import api_requester

class MainWindow(QWidget):
    scraper_stopped = pyqtSignal()

    def closeEvent(self, event):
        if self.scraper_worker and self.scraper_thread.isRunning():
            self.stop_scraper()  # Emit stop signal

        # Wait for the thread to finish before proceeding
            self.scraper_thread.quit()
            self.scraper_thread.wait()  # Blocks until the thread fully exits
        event.accept()

    def __init__(self):
        super().__init__()

        # Holds our classes in memory
        # Each item: (class_name, [instructors], [schedule], apiID)
        self.classes = load_classes()
        
        # UI init
        self.initUI()

        # Thread handle if you want to do background scraping
        self.scraper_thread = None

    def initUI(self):
        """Set up all the PyQt widgets in the main window."""

        self.setWindowTitle("BC Class Availibility Checker")

         # Main vertical layout
        layout = QVBoxLayout()

        # Username
        self.username_label = QLabel("Username:")
        self.username_entry = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)

        # Password
        self.password_label = QLabel("Password:")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)

        # Class Name
        self.class_name_label = QLabel("Class Name:")
        self.class_name_entry = QLineEdit()
        layout.addWidget(self.class_name_label)
        layout.addWidget(self.class_name_entry)

        # Section
        self.section_label = QLabel("Section:")
        self.section_entry = QLineEdit()
        layout.addWidget(self.section_label)
        layout.addWidget(self.section_entry)

        # Add Class Button
        self.add_class_button = QPushButton("Add Class")
        self.add_class_button.clicked.connect(self.add_class)
        layout.addWidget(self.add_class_button)

        # The list widget to display classes
        self.class_listwidget = QListWidget()
        layout.addWidget(self.class_listwidget)

        # Populate the list with existing classes
        self.populate_list_widget()

        # Remove Selected Class Button
        self.remove_class_button = QPushButton("Remove Selected Class")
        self.remove_class_button.clicked.connect(self.remove_selected_class)
        layout.addWidget(self.remove_class_button)

        self.start_button = QPushButton("Start Scraper")
        self.start_button.clicked.connect(self.start_scraper)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Scraper")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_scraper)
        layout.addWidget(self.stop_button)

        # Label to display progress
        self.progress_label = QLabel("Progress: ")
        layout.addWidget(self.progress_label)

        self.setLayout(layout)



    def populate_list_widget(self):
        """Clear and re-populate the QListWidget based on self.classes."""
        self.class_listwidget.clear()
        for class_name, instructors, schedule, apiID in self.classes:
            item_text = (
                f"{class_name}\n"
                f"Instructors: {', '.join(instructors)}\n"
                f"Schedule: {', '.join(schedule)}\n"
            )
            self.class_listwidget.addItem(item_text)

    def on_add_class_finished(self, grabbed_name, instructors, schedule, apiID):
        # 1) Hide or remove the overlay
        self.hide_overlay()

        # 2) Update data
        self.classes.append((grabbed_name, instructors, schedule, apiID))
        save_classes(self.classes)

        # 3) Add item to QListWidget
        item_text = (
            f"{grabbed_name}\n"
            f"Instructors: {', '.join(instructors)}\n"
            f"Schedule: {', '.join(schedule)}\n"
        )
        self.class_listwidget.addItem(item_text)

        # 4) Clear inputs
        self.class_name_entry.clear()
        self.section_entry.clear()

    def on_add_class_error(self, error_msg):
        self.hide_overlay()
        QMessageBox.critical(self, "Error Adding Class", error_msg)

    def show_overlay(self, message="Working..."):
        if not hasattr(self, "overlay"):
            # Create overlay as a child widget
            self.overlay = QWidget(self)
            self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 128);")
            self.overlay.setGeometry(self.rect())
            self.overlay_label = QLabel(message, self.overlay)
            self.overlay_label.setStyleSheet("color: white; font-size: 16px;")
            # Center the label in the overlay
            self.overlay_label.move(
                (self.overlay.width() - self.overlay_label.width()) // 2,
                (self.overlay.height() - self.overlay_label.height()) // 2
            )
        else:
            # Just update text
            self.overlay_label.setText(message)

        self.overlay.show()
        self.overlay.raise_()  # bring to front

    def hide_overlay(self):
        if hasattr(self, "overlay"):
            self.overlay.hide()

    def add_class(self):
        class_name = self.class_name_entry.text().strip()
        section_str = self.section_entry.text().strip()

        if not class_name or not section_str:
            QMessageBox.critical(self, "Error", "Please enter both class name and section.")
            return

        try:
            section = int(section_str)
        except ValueError:
            QMessageBox.critical(self, "Error", "Section must be a number.")
            return

        username = self.username_entry.text().strip()
        password = self.password_entry.text().strip()

        # 1) Show an overlay or disable the UI
        self.show_overlay("Adding class...")  # you'll define show_overlay()

        # 2) Create a QThread and a worker object
        self.thread = QThread()  # keep a reference so it doesn't get GC'ed
        self.worker = worker.ClassAddWorker(class_name, section, username, password, self.classes)
        self.worker.moveToThread(self.thread)

        # 3) Connect signals/slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_add_class_finished)
        self.worker.error.connect(self.on_add_class_error)
        # We also want to clean up the thread
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)

        # 4) Start the thread
        self.thread.start()


    def remove_selected_class(self):
        """Remove the currently selected class from both the list and data."""
        selected_items = self.class_listwidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a class to remove.")
            return

        # We'll only handle removing one item at a time
        item = selected_items[0]
        row = self.class_listwidget.row(item)
        self.class_listwidget.takeItem(row)  # remove from UI
        self.classes.pop(row)                # remove from data
        save_classes(self.classes)

    def update_scraper_progress(self, message):
        """Update the progress label."""
        self.progress_label.setText(f"Progress: {message}")

    def scraper_show_error(self, error_message):
        """Display an error message."""
        QMessageBox.critical(self, "Error", error_message)

    def on_scraper_finished(self):
        """Re-enable UI when the scraper finishes."""
        self.reenable_ui()
        self.progress_label.setText("Progress: Class checking finished!")

    def start_scraper(self):
        """Start the background scraping (Selenium) in a thread."""
        username = self.username_entry.text().strip()
        password = self.password_entry.text().strip()

        if not username or not password:
            QMessageBox.critical(self, "Error", "Please enter both username and password.")
            return

        # Disable UI elements
        self.username_entry.setEnabled(False)
        self.password_entry.setEnabled(False)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.scraper_thread = QThread()
        self.scraper_worker = worker.ScraperWorker(username, password, self.classes)

        # Move the worker to the thread
        self.scraper_worker.moveToThread(self.scraper_thread)
        print(f"Worker thread: {self.scraper_worker.thread()}")

        # Connect signals and slots
        self.scraper_thread.started.connect(self.scraper_worker.run)  # Start the worker
        self.scraper_worker.progress.connect(self.update_scraper_progress)    # Handle progress updates
        self.scraper_worker.error.connect(self.scraper_show_error)            # Handle errors

        print("Connecting scraper_stopped to scraper_worker.stop...")
        self.scraper_stopped.connect(self.scraper_worker.stop_scraper_worker)  # Connect the signal
        print(f"Signal connected")
        self.scraper_worker.finished.connect(self.on_scraper_finished)  # Handle completion

        # Clean up thread and worker after it finishes
        self.scraper_worker.finished.connect(self.scraper_thread.quit)
        self.scraper_worker.finished.connect(self.scraper_worker.deleteLater)
        self.scraper_thread.finished.connect(self.scraper_thread.deleteLater)


        self.scraper_thread.start()
    def stop_scraper(self):
        """Signal the scraper thread to stop."""
        if self.scraper_worker:
            print("scraper stopped?")
            self.scraper_stopped.emit()  # Emit the signal to stop the worker
        self.stop_button.setEnabled(False)

    def reenable_ui(self):
        self.username_entry.setEnabled(True)
        self.password_entry.setEnabled(True)
        self.start_button.setEnabled(True)
        self.add_class_button.setEnabled(True)
        self.stop_button.setEnabled(False)


        # The re-enabling of UI elements will happen 
        # once the thread actually finishes in run_scraper's finally block.
