import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

URL = "https://xmdocumentation.bloomreach.com/about/release-notes/release-notes-overview.html"

def get_current_version():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    cell = soup.select_one("table tbody tr:nth-child(2) td:nth-child(1) a")
    return cell.text.strip()

def get_last_version():
    try:
        with open("last_version.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_version(version):
    with open("last_version.txt", "w") as f:
        f.write(version)

def send_email(new_version):
    msg = MIMEText(f"New Bloomreach version detected: {new_version}\n\n{URL}")
    msg["Subject"] = f"Bloomreach Update: {new_version}"
    msg["From"] = os.environ["EMAIL_FROM"]
    msg["To"] = os.environ["EMAIL_TO"]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ["EMAIL_FROM"], os.environ["EMAIL_PASSWORD"])
        server.send_message(msg)

current = get_current_version()
last = get_last_version()

if last is None:
    print(f"First run. Current version: {current}")
    save_version(current)
elif current != last:
    print(f"New version found: {current} (was {last})")
    send_email(current)
    save_version(current)
else:
    print(f"No update. Still on {current}")
