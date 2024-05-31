import sqlite3
import smtplib
#
# envs.py dodatak
#
from envs import SENDER_EMAIL, APP_PASSWORD, SMTP_SERVER, SMTP_PORT
#from email.mime.text import MIMEText
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


# connect to database
conn = sqlite3.connect('vodomjeri.db')
# curson
cursor = conn.cursor()
rows = cursor.execute("SELECT Kontakt_email FROM Zgrada")


subject = 'Email subject'
body = 'Neki tekst'

for row in rows:
    if row[0] is not None:
        
        # dodavanje priloga mailu ako nisu nađeni ne šalje se mail
        try:
            with open("Neki_pdf.pdf", "rb") as attachment:
                # Add the attachment to the message
                part_pdf = MIMEBase("application", "octet-stream")
                part_pdf.set_payload(attachment.read())
                encoders.encode_base64(part_pdf)
                part_pdf.add_header(
                    "Content-Disposition",
                    f"attachment; filename= Neki_pdf.pdf",
                )
        except FileNotFoundError:
            print(f"PDF file not found")
            continue
        
        try:
            with open("Neki_excel.xlsx", "rb") as attachment:
                # Add the attachment to the message
                part_xlsx = MIMEBase("application", "octet-stream")
                part_xlsx.set_payload(attachment.read())
                encoders.encode_base64(part_xlsx)
                part_xlsx.add_header(
                    "Content-Disposition",
                    f"attachment; filename= Neki_excel.xlsx",
                )
        except FileNotFoundError:
            print(f"XLSX file not found")
            continue
            
        addresses = row[0].split(";")
        #iteriranje po adresama u jednom redu
        for address in addresses:
            print(address)
            
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = SENDER_EMAIL
            msg['To'] = address
            msg.attach(MIMEText(body, 'plain'))
            msg.attach(part_pdf)
            msg.attach(part_xlsx)
            try:
                with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp_server:
                    smtp_server.login(SENDER_EMAIL, APP_PASSWORD)
                    smtp_server.sendmail(SENDER_EMAIL, address, msg.as_string())
                print(f'Email poruka je uspjesno poslana na {address}')
            except smtplib.SMTPAuthenticationError:
                print("SMTP Authentication Error")
            except smtplib.SMTPException as e:
                print(f"SMTP Exception: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
    else:
        print("Email adresa zgrade nije dostupna")
conn.close()
