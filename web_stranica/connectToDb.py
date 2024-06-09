from flask import request, jsonify, session
import sqlite3

def connect_to_db():
    filepath = session.get("uploaded_file")
    conn = sqlite3.connect(filepath)    
    cursor = conn.cursor()
    return conn, cursor