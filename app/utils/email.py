import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, sender_email, recipient_email, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Configure your SMTP server and port here
    server = smtplib.SMTP('smtp.your-email-provider.com', 587)
    server.starttls()
    server.login(sender_email, "your-email-password")
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()
