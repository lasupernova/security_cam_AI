import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.message import EmailMessage

from dotenv import load_dotenv  
load_dotenv()                    

import imghdr  # And imghdr to find the types of our images

import os 

# get email password from .env-file
password = os.environ.get('PASSWORD')

subject = "FOTO: OMG, la camara captura a alguien entrando a tu casa!!!!!"
body = "Aqui esta la foto del ladron..."
sender_email = os.environ.get("SENDER")
# receiver_email = "karina@mosicom.de"
receiver_email = os.environ.get("RECIPIENT")


# Create a multipart message and set headers
message = EmailMessage()  #multipart in order to attach picture
message["From"] = sender_email
message["To"] = receiver_email
message.preamble = subject
# message["Bcc"] = receiver_email  # Recommended for mass emails

# # Add body to email
# message.attach(MIMEText(body, "plain"))
 
filename = f"media{os.sep}test.jpg"  # In same directory as script
with open(filename, 'rb') as fp:
    img_data = fp.read()
# image = MIMEImage(img_data, name=os.path.basename(filename))
message.add_attachment(img_data, maintype='image',
                                 subtype=imghdr.what(None, img_data))


# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.send_message(message)