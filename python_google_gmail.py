import sqlite3
import smtplib
#
# envs.py dodatak
#
from envs import APP_PASSWORD
#from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


# connect to database
conn = sqlite3.connect('vodomjeri.db')
# curson
cursor = conn.cursor()
address = cursor.execute("SELECT Kontakt_email FROM Zgrada")

sender = 'ritehvodomjer@gmail.com'
#recipients = [sender, "dorotea376@gmail.com"]
subject = 'Email subject'
body = 'Neki tekst'


with open("Neki_pdf.pdf", "rb") as attachment:
    # Add the attachment to the message
    part_pdf = MIMEBase("application", "octet-stream")
    part_pdf.set_payload(attachment.read())
encoders.encode_base64(part_pdf)
part_pdf.add_header(
    "Content-Disposition",
    f"attachment; filename= Neki_pdf.pdf",
)

with open("Neki_excel.xlsx", "rb") as attachment:
    # Add the attachment to the message
    part_xlsx = MIMEBase("application", "octet-stream")
    part_xlsx.set_payload(attachment.read())
encoders.encode_base64(part_xlsx)
part_xlsx.add_header(
    "Content-Disposition",
    f"attachment; filename= Neki_excel.xlsx",
)


for row in address:
    if row[0] is not None:

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = '; '.join(row[0])
        msg.attach(part_pdf)
        msg.attach(part_xlsx)
    
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, APP_PASSWORD)
            smtp_server.sendmail(sender, row[0], msg.as_string())
        print('Msg sent')

  




    
    
