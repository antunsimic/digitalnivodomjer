from flask import session
import os
from uuid import uuid4
import shutil

def prepare_user_directory():
    session['user_id'] = str(uuid4())  
   
    user_dir = os.path.join(session['user_id'])
    os.makedirs(user_dir, exist_ok=True)
    
    # kreiranje potrebnih direktorija u user_direktoriju
    directories_to_create = [
        os.path.join(user_dir, 'izvjestaji', 'zgrade'),
        os.path.join(user_dir, 'izvjestaji', 'vodovod'),
        os.path.join(user_dir, 'uploads')
    ]

    for directory in directories_to_create:
        os.makedirs(directory, exist_ok=True)   
    
    # OVAJ DIO NIJE ZAPRAVO POTREBAN -> Kako su podatci spremljeni u session mozemo samo SMTP_PORT i SMTP_SERVER stavit kao varijable
    envs_file_path = os.path.join(user_dir, 'envs.py')
    email = session.get('email')
    password = session.get('password')
    if not os.path.exists(envs_file_path):  # Only create the file if it doesn't exist
        with open(envs_file_path, 'w') as f:
            f.write(f"""SENDER_EMAIL = '{email}'\n"""
                    f"""APP_PASSWORD = '{password}'\n"""
                    f"""SMTP_SERVER = 'smtp.gmail.com'\n"""
                    f"""SMTP_PORT = 465\n""")

# fukncije za dogvaćanje putanja
def get_user_dir_path():
    return os.path.join(session['user_id'])

def get_user_izvjestaji_zgrade_path():
    return os.path.join(get_user_dir_path(), 'izvjestaji', 'zgrade')

def get_user_izvjestaji_vodovod_path():
    return os.path.join(get_user_dir_path(), 'izvjestaji', 'vodovod')

def get_user_upload_path():
    return os.path.join(get_user_dir_path(), 'uploads')

def delete_user_dir():
    user_id = session.get('user_id')
    if user_id:
        user_dir = os.path.join(user_id)
        if os.path.exists(user_dir):
            shutil.rmtree(user_dir)
            # Optionally, you can also remove the user_id from the session
            session.pop('user_id', None)
            