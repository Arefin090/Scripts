import smtplib
import requests
from email.mime.text import MIMEText

def fetch_joke():
    response = requests.get("https://v2.jokeapi.dev/joke/Any")
    data = response.json()
    
    if data['type'] == 'single':
        return data['joke']
    else:
        return f"{data['setup']} ... {data['delivery']}"

def send_email(joke, recipient_email):
    sender_email = "dailyjokesbyarefin@gmail.com"
    sender_password = "fjzr omyd hbml wsqb"
    
    subject = "Arefin's Daily Joke"
    body = joke
    
    msg = MIMEText(body)
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

if __name__ == "__main__":
    joke = fetch_joke()
    recipient = "arefin923@gmail.com"
    send_email(joke, recipient)
