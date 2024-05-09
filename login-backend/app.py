from flask import Flask, request, jsonify
import os

def create_file(email, password):
    file_path = 'login-backend/podaci.txt'
    with open(file_path, 'w') as f:
        f.write(f"{email}\n{password}")

def delete_file():
    file_path = 'login-backend/podaci.txt'
    if os.path.exists(file_path):
        os.remove(file_path)




app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    create_file(email, password)
    return jsonify({'success': True, 'message': 'Login successful'})
    
@app.route('/logout')
def logout():
    delete_file()
    return jsonify({'success': True, 'message': 'Logout successful'})

if __name__ == '__main__':
    app.run(debug=True)
