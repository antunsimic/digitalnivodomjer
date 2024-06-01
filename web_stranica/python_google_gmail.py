import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import zipfile # za kreiranje vodovod_reports.zip datoteke
from godisnjaPotrosnjaFunct import connect_to_db
from flask import session, jsonify
from envs import SMTP_SERVER, SMTP_PORT


# samostalna funkcija za generiranje imena izvjestaja za zgrade
def generate_filename(adresa, najnovije_razdoblje, tip):
    adresa = adresa.replace('/', '_')
    adresa_split = adresa.split()
    adresa_formatted = '_'.join([r[:6] for r in adresa_split])
    najnovije_razdoblje = str(najnovije_razdoblje)
    MM = najnovije_razdoblje[5:7]  # Extract month
    if len(MM) == 1:
        MM = '0' + MM  # Ensure month is two digits
    YYYY = najnovije_razdoblje[:4]

    return f"{adresa_formatted}_{MM}_{YYYY}.pdf"

# funkcija za izvršenje slanja emaila
def send_email(subject, body, to_address, attachment_path=None):
    #dobivanje imena i lozinke sendera preko sessions
    SENDER_EMAIL = session.get("email")
    APP_PASSWORD = session.get("password")

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # dodavanje priloga izvjestaja za zgradu ili zip datoteka sa izvjestajima za vodovod
    if attachment_path:
        part = MIMEBase('application', 'octet-stream')
        with open(attachment_path, 'rb') as attachment:
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp_server:
            # login sendera i slanje emaila
            smtp_server.login(SENDER_EMAIL, APP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, to_address, msg.as_string())
            
        print(f'Email poruka je uspješno poslana na {to_address}')
        return f'Na {to_address} USPJEŠNO slanje izvještaja {os.path.basename(attachment_path)}'
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error")
        return f'Na {to_address} NIJE uspješno slanje izvještaja {os.path.basename(attachment_path)}: SMTP Authentication Error'
    except smtplib.SMTPException as e:
        print(f"SMTP Exception: {e}")
        return f'Na {to_address} NIJE uspješno slanje izvještaja {os.path.basename(attachment_path)}: SMTP Exception - {e}'
    except Exception as e:
        print(f"An error occurred: {e}")
        return f'Na {to_address} NIJE uspješno slanje izvještaja {os.path.basename(attachment_path)}: {e}'


# funkcija za dohvaćanje kontakata zgrada, njima namijenjenim izvješcćima te proslijeđivanje funkciji send_email
def send_reports_for_zgrade(cursor):
    feedback_msg = []
    tip = 'pdf'
    rows = cursor.execute("SELECT Kontakt_email, Ulica_kbr FROM Zgrada").fetchall()
   
    subject = 'Izvještaj potrošnje za zgradu'
    body = 'Poštovani,\n\nU prilogu se nalazi izvještaj.'

    najnovije_razdoblje = cursor.execute('SELECT MAX(Razdoblje_obracun) FROM Obracun').fetchone()[0]

    for row in rows:  
        email_address = row[0]
        ulica_kbr = row[1]
        # generiranje naziva datoteke iz Ulica_kbr i Razdoblje obracun vrijednosti
        filename = generate_filename(ulica_kbr, najnovije_razdoblje, tip)  
        # kreiranje putanje do izvjestaja cije ime je generirano
        attachment_path = os.path.join('izvjestaji', 'zgrade', filename)
        # ako navedena datoteka/putanja i email zgrade postoje pošalji mail
        if os.path.exists(attachment_path) and email_address is not None:
            # u feedback_msg listu se nadodaju odgovori na slanje svakog emaila radi prikaza na frontendu
            feedback_msg.append(send_email(subject, body, email_address, attachment_path))
        else:
            feedback_msg.append(f'Na {email_address} NIJE uspješno slanje izvještaja {os.path.basename(attachment_path)}')
    return feedback_msg


def create_zip(zip_name, directory):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))
    return zip_name

# funkcija za dohvaćanje kontakata u Vodovod tablici, sakupljanje izvjesaja za vodovod u jednu datoteku i proslijeđivanje funkciji send_email
def send_reports_for_vodovod(cursor):
    feedback_msg = []
    rows = cursor.execute("SELECT Kontakt_email FROM Vodovod").fetchall()

    subject = 'Izvještaj za vodovod'
    body = 'Poštovani,\n\nU prilogu se nalazi izvještaj za vodovod.'
    
    # za slanje izvještaji se stavljaju u jeednu zip datoteku
    attachment_dir = "izvjestaji/vodovod"
    zip_name = 'vodovod_reports.zip'
    zip_path = create_zip(zip_name, attachment_dir)

    # za svaki email u Vodovod pošalji email (ako postoji zip)
    for row in rows:
        email_address = row[0]
        if os.path.exists(zip_path):
            feedback_msg.append(send_email(subject, body, email_address, zip_path))
        else:
            feedback_msg.append(f'Na {email_address} NIJE uspješno slanje izvještaja {zip_name}')

    os.remove(zip_path)  # brisanje zip datoteke
    return feedback_msg

def send_both_mails():
    # povezivanje na bazu podataka preko funkcije u godisnjaPotrosnjaFunck.py
    conn, cursor = connect_to_db()
    
    if session.get("logged_in"):
        feedback_zgrade = send_reports_for_zgrade(cursor)
        #print(feedback_zgrade)
        feedback_vodovod = send_reports_for_vodovod( cursor)   
        #print(feedback_vodovod)
        combined_feedback = feedback_zgrade + feedback_vodovod
    else:
        combined_feedback = "Potrebno je ulogirati se sa validnom email adresom i lozinkom/app password"
    
    conn.close()
    return jsonify(combined_feedback)

def get_report_list():
    if session.get("uploaded_file"):
        try:
            files_vodovod = os.listdir('izvjestaji/vodovod')
            files_zgrade = os.listdir('izvjestaji/zgrade')
            files = files_zgrade + files_vodovod
            
            return jsonify(files)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Baza podataka nije uploadana'})
    
