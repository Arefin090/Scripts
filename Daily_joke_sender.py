import smtplib
import requests
from email.mime.text import MIMEText
import keyring
from email.mime.multipart import MIMEMultipart
def fetch_joke():
    url = "https://dad-jokes.p.rapidapi.com/random/joke"
    headers = {
        "X-RapidAPI-Key": "2d157e36ebmshb07e9adfee0dcb3p13048cjsnb3eb119c23de",
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # Extracting the joke's setup and punchline
    setup = data['body'][0]['setup']
    punchline = data['body'][0]['punchline']

    # Formatting the joke
    return f"{setup} ... {punchline}"

def send_email(joke, recipient_email):
    sender_email = "dailyjokesbyarefin@gmail.com"
    
    # Retrieve the stored Gmail App Password from macOS Keychain
    sender_password = keyring.get_password("daily_joke_sender", "GMAIL_APP_PASSWORD")
    
    subject = "Arefin's Daily Joke"
    
    html_template = """
    <html>
        <head></head>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #e9e9e9; padding: 20px;">
                <h2 style="color: #4a90e2;">Arefin's Daily Joke</h2>
                <p>Hey there,</p>
                <p style="font-size: 18px; font-weight: bold; padding: 10px; background-color: #f9f9f9; border: 1px solid #e9e9e9;">{{joke}}</p>
                <p>Hope that brought a smile to your face! Stay tuned for more jokes tomorrow.</p>
                <p>Best,</p>
                <p>Arefin</p>
            </div>
        </body>
    </html>
    """
    
    html_content = html_template.replace("{{joke}}", joke)

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    
    part = MIMEText(html_content, "html")
    msg.attach(part)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

if __name__ == "__main__":
    joke = fetch_joke()
    recipient = "arefin923@gmail.com"
    send_email(joke, recipient)
