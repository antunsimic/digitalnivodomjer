from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = "secretkey"

users = {
    'ritehvodomjer@gmail.com': 'sotb sfva lpms adqr'
}

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route("/api/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if email in users and users[email] == password:
        session['email'] = email
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'})
    
@app.route("/api/logout")
def logout():
    session.pop('email', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

if __name__ == "__main__":
    app.run(debug=True)