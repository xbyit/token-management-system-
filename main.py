from flask import Flask, jsonify, request, render_template_string
import json
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key'

def generate_token():
    length = 12
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choices(characters, k=length))
    return token

def add_token(file, end_date):
    try:
        # Ensure end_date is a timedelta
        expiration_time = datetime.now() + timedelta(days=end_date)
        with open(file, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            token = generate_token()
            # Store the expiration time in ISO format
            data[token] = {"time": expiration_time.isoformat()}
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        return token
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")  # Add logging
        with open(file, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")  # Add logging
        return None

def check_tok(file, token):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            token_data = data.get(token, {})
            return token_data.get('time')
    except (FileNotFoundError, json.JSONDecodeError):
        return None
# Home Page
@app.route('/')
def home():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Token Management System</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 300px;
            }
            h1 {
                margin-bottom: 20px;
                color: #333;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                text-decoration: none;
                color: white;
                background-color: #4CAF50;
                border-radius: 5px;
                transition: background-color 0.3s ease;
                margin: 10px 0;
            }
            .button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Token Management System</h1>
            <a href="/generate_token" class="button">Generate Token</a>
            <a href="/check_token" class="button">Check Token</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/generate_token')
def gen():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Token Generator</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 300px;
            }
            h1 {
                margin-bottom: 20px;
            }
            input[type="number"] {
                padding: 10px;
                font-size: 16px;
                width: calc(100% - 20px);
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #45a049;
            }
            #result {
                margin-top: 20px;
                font-size: 18px;
                color: #333;
            }
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Token Generator</h1>
            <input type="number" id="lengthInput" placeholder="Enter token expiration (in days)" min="1">
            <button id="generateBtn">Generate Token</button>
            <div id="result"></div>
        </div>
        <script>
            document.getElementById('generateBtn').addEventListener('click', function() {
                const length = document.getElementById('lengthInput').value.trim();
                if (!length || length <= 0) {
                    document.getElementById('result').innerHTML = '<p class="error">Please enter a valid length.</p>';
                    return;
                }
                fetch(`/generate_token_res?length=${encodeURIComponent(length)}`)
                    .then(response => response.json())
                    .then(data => {
                        const resultDiv = document.getElementById('result');
                        if (data.token) {
                            resultDiv.innerHTML = `<p>Your Token: <strong>${data.token}</strong></p>`;
                        } else if (data.error) {
                            resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
                        } else {
                            resultDiv.innerHTML = '<p class="error">Unexpected error occurred.</p>';
                        }
                    });
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/generate_token_res')
def gen_res():
    file = 'info.json'
    days = request.args.get('length', type=int)

    if days <= 0:
        return jsonify({"error": "Invalid duration. Must be greater than 0."}), 400

    token = add_token(file, days)
    if token:
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Failed to generate token."}), 500

@app.route('/check_token')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Token Status</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 300px;
            }
            h1 {
                margin-bottom: 20px;
            }
            input[type="text"] {
                padding: 10px;
                font-size: 16px;
                width: calc(100% - 20px);
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #45a049;
            }
            #result {
                margin-top: 20px;
                font-size: 18px;
                color: #333;
            }
            .error {
                color: red;
            }
            .expired {
                color: orange;
            }
            .valid {
                color: green;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Check Token Status</h1>
            <input type="text" id="Token" placeholder="Enter Token">
            <button id="checkBtn">Check Token</button>
            <div id="result"></div>
        </div>
        <script>
            document.getElementById('checkBtn').addEventListener('click', function() {
                const token = document.getElementById('Token').value.trim();
                if (!token) {
                    document.getElementById('result').innerHTML = '<p class="error">Please enter a token.</p>';
                    return;
                }
                fetch(`/check_token_res?token=${encodeURIComponent(token)}`)
                    .then(response => response.json())
                    .then(data => {
                        const resultDiv = document.getElementById('result');
                        if (data.status === 'expired') {
                            resultDiv.innerHTML = `<p class="expired">${data.message}</p>`;
                        } else if (data.status === 'valid') {
                            resultDiv.innerHTML = `<p class="valid">${data.message}</p>`;
                        } else {
                            resultDiv.innerHTML = `<p class="error">${data.message}</p>`;
                        }
                    })
                    .catch(() => {
                        document.getElementById('result').innerHTML = '<p class="error">An error occurred while checking the token.</p>';
                    });
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/check_token_res', methods=['GET'])
def check_token():
    token = request.args.get('token')
    file_path = 'info.json'

    if not token:
        return jsonify({"status": "error", "message": "Token is missing."})

    end_time = check_tok(file_path, token)
    if end_time:
        try:
            end_date = datetime.fromisoformat(end_time)
            current_date = datetime.now()

            if current_date > end_date:
                return jsonify({"status": "expired", "message": "The token is expired."})
            elif current_date.date() == end_date.date():
                return jsonify({"status": "valid", "message": "Valid token for today."})
            else:
                return jsonify({"status": "valid", "message": "Valid token."})
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid date format in token data."})
    else:
        return jsonify({"status": "error", "message": "Token not found."})

if __name__ == '__main__':
    app.run(debug=True)