# BC Class Availibility Checker  
Created a Selenium driver based web crawler that utilizes api requests to retrieve class availibility information and sends an email notification if there are seats available.  

**How it's made:**  

Selenium Chrome driver to automate login.  
Http API requests to retrie JSONs of class data.  
Tinkered with multiple guis, including Tkinter, React Frontend with FastAPI backend and SQLite database (was unable to host the web application on a cloud server for technical reasons), and PyQt (Final GUI).  
Implemented automated email notification with SMTP.  

## Optimizations  

Switched from Http requests to a Selenium driver.  
Implemented API requests instead of parsing the entire html webpage.  
Used multithreading to allow user to simultaneously add/remove classes while the checker is running.  

## Lessons Learned:  

This being my first real standalone project that I worked on myself, I found that coding is a continual repeated process of learning, applying, and tinkering around with my project. Utilizing the full extent of resources available to me has also been a journey, whether it be consulting experienced programmers or ChatGPT to help give me ideas or make progress in my project.  
