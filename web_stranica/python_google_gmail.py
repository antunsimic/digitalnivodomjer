import os
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from flask import jsonify, session
from envs import SENDER_EMAIL, APP_PASSWORD, SMTP_SERVER, SMTP_PORT

# samostalna funkcija za generiranje imena izvjestaja za zgrade
def generate_filename(adresa, najnovije_razdoblje):
    adresa = adresa.replace('/', '_')
    adresa_split = adresa.split()
    adresa_formatted = '_'.join([r[:6] for r in adresa_split])
    najnovije_razdoblje = str(najnovije_razdoblje)
    MM = najnovije_razdoblje[-2:]
    YYYY = najnovije_razdoblje[:4]

    return f"{adresa_formatted}_{MM}_{YYYY}.pdf"

# funkcija za izvršenje slanja emaila
def send_email(subject, body, to_address, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        part = MIMEBase('application', 'octet-stream')
        with open(attachment_path, 'rb') as attachment:
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp_server:
            smtp_server.login(SENDER_EMAIL, APP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, to_address, msg.as_string())
        print(f'Email poruka je uspješno poslana na {to_address}')
        return f'Izvjesce {os.path.basename(attachment_path)} je uspješno poslano na {to_address}'
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error")
        return f'SMTP Authentication Error'
    except smtplib.SMTPException as e:
        print(f"SMTP Exception: {e}")
        return f'SMTP Exception: {e}'
    except Exception as e:
        print(f"An error occurred: {e}")
        return f'An error occurred: {e}'

# funkcija za dohvaćanje kontakata zgrada, njima namijenjenim izvješcćima te proslijeđivanje funkciji send_email
def send_reports_for_zgrade():
    feedback_msg = []
    conn = sqlite3.connect(session.get("uploaded_file"))
    cursor = conn.cursor()
    rows = cursor.execute("SELECT Kontakt_email, Ulica_kbr FROM Zgrada").fetchall()
   
    subject = 'Izvještaj potrošnje za zgradu'
    body = 'Poštovani,\n\nU prilogu se nalazi izvještaj.'

    najnovije_razdoblje = cursor.execute('SELECT MAX(Razdoblje_obracun) FROM Obracun').fetchone()[0]
   
    for row in rows:
        
        email_address = row[0]
        ulica_kbr = row[1]
        
        filename = generate_filename(ulica_kbr, najnovije_razdoblje)  
        attachment_path = os.path.join('izvjestaji', 'zgrade', filename)
        print(attachment_path)
        if os.path.exists(attachment_path):
            feedback_msg.append(send_email(subject, body, email_address, attachment_path))
        else:
            feedback_msg.appendprint(f"Datoteka {attachment_path} ne postoji i nije uspješno poslana na {email_address}.")
            

    conn.close()
    return jsonify(feedback_msg)
    #return feedback_msg

def send_reports_for_vodovod():
    feedback_msg = []
    conn = sqlite3.connect(session.get("uploaded_file"))
    cursor = conn.cursor()
    rows = cursor.execute("SELECT Kontakt_email FROM Vodovod")

    subject = 'Izvještaj za vodovod'
    body = 'Poštovani,\n\nU prilogu se nalazi izvještaj za vodovod.'

    attachment_path = "izvjestaji/vodovod"

    for row in rows:
        email_address = row[0]
        feedback_msg.append(send_email(subject, body, email_address, attachment_path))

    conn.close()
    #return jsonify(feedback_msg)
    return feedback_msg

def send_both_mails():
    
    feedback_zgrade = send_reports_for_zgrade()
    print("amogus")
    feedback_vodovod = send_reports_for_vodovod()   
    print("sus")
    return feedback_zgrade + feedback_vodovod
    
