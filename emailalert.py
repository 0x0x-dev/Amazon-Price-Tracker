import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert(email, subject, body):
    sender = 'example@gmail.com'  # Replace with actual email
    password = 'your_app_password'       # Replace with actual app password

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = subject

    # Attach body with UTF-8 encoding
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        # Send the properly formatted message
        server.send_message(msg)
