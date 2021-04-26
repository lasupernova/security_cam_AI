import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv  
load_dotenv()                    

import os 

# get email password from .env-file
password = os.environ.get('PASSWORD')

subject = ">>>OMG, la camara captura a alguien entrando a tu casa!!!!!"
body = "Aqui esta la foto del ladron..."
sender_email = os.environ.get("SENDER")
# receiver_email = "karina@mosicom.de"
receiver_email = os.environ.get("RECIPIENT")


# Create a multipart message and set headers
message = MIMEMultipart()  #multipart in order to attach picture
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
# message["Bcc"] = receiver_email  # Recommended for mass emails

# # Add body to email
# message.attach(MIMEText(body, "plain"))

filename = f"media{os.sep}test.jpg"  # In same directory as script
img_data = open(filename, 'rb').read()


text = "This is a test!"

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)