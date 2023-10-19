import os
import smtplib
import requests
from email.mime.text import MIMEText
import keyring
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAILS = [email.strip() for email in os.getenv("RECIPIENT_EMAILS").split(',')]
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def fetch_joke():
    url = "https://dad-jokes.p.rapidapi.com/random/joke"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # Extracting the joke's setup and punchline
    setup = data['body'][0]['setup']
    punchline = data['body'][0]['punchline']

    # Formatting the joke
    return f"{setup} ... {punchline}"

def send_email(joke, recipient_emails):
    
    # Retrieve the stored Gmail App Password from environment variable or macOS Keychain
    sender_password = GMAIL_APP_PASSWORD if GMAIL_APP_PASSWORD else keyring.get_password("daily_joke_sender", "GMAIL_APP_PASSWORD")

    subject = "Arefin's Daily Joke"
    
    html_template = """
    <html>
        <head></head>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #e9e9e9; padding: 20px;">
                <h2 style="color: #4a90e2;">Arefin's Daily Joke</h2>
                <p>Hey mate,</p>
                <p>This email serves as a token of appreciation I have for you. Here's your daily joke:</p>
                <p style="font-size: 18px; font-weight: bold; padding: 10px; background-color: #f9f9f9; border: 1px solid #e9e9e9;">{{joke}}</p>
                <p>Hope that brought a smile to your face! Stay tuned for more jokes tomorrow.</p>
                <p>Best,</p>
                <p>Arefin</p>
            </div>
        </body>
    </html>
    """
    
    html_content = html_template.replace("{{joke}}", joke)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER_EMAIL, sender_password)

    for email in recipient_emails:
        msg = MIMEMultipart("alternative")
        msg["From"] = SENDER_EMAIL
        msg["To"] = email
        msg["Subject"] = subject

        part = MIMEText(html_content, "html")
        msg.attach(part)

        server.sendmail(SENDER_EMAIL, email, msg.as_string())

    server.quit()

if __name__ == "__main__":
    joke = fetch_joke()
    send_email(joke, RECIPIENT_EMAILS)
