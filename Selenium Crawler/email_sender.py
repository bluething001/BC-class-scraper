import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(available_seats, class_name, instructors, schedules):
    # Email Configuration
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_SENDER = "alexguo05@gmail.com"  # Replace with your email
    EMAIL_PASSWORD = "otur ftut gdfx ofdl"  # Replace with your email password (use app password for Gmail)
    EMAIL_RECIPIENT = "alexguo05@gmail.com"  # Replace with recipient's email

    # Email Content
    subject = "Seat Availability Alert"
    body = f"Seats Available in {class_name}!\n\nAvailable Seats: {available_seats}\nRegister soon!\n\nClass Details:\nInstructors: {', '.join(instructors)}\nSchedule: {', '.join(schedules)}"

    # Create email
    message = MIMEMultipart()
    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECIPIENT
    message["Subject"] = subject

    # Add body text
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to SMTP server and send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Start TLS encryption
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(message)
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
    finally:
        server.quit()

