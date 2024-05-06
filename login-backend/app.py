from flask import Flask, render_template, request, jsonify, send_from_directory
app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Page</title>
    </head>
    <body>
        <div id="root"></div>
        <script src="/static/bundle.js"></script>
    </body>
    </html>
    """

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email == 'example@example.com' and password == 'password':
        print(email)
        print(password)
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        print(email)
        print(password)
        return jsonify({'success': False, 'message': 'Login unsuccessful'})

@app.route('/static/bundle.js') #u bundle.js su spojene sve komponente(App.js i LoginPage.js)
def serve_bundle():
    return send_from_directory('static', 'bundle.js')

if __name__ == '__main__':
    app.run(debug=True)