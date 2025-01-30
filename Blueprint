
---

### Project Structure with Blueprints
```
token-management-system/
├── app/
│   ├── __init__.py       # Initialize the Flask app and register blueprints
│   ├── auth/             # Blueprint for token generation and validation
│   │   ├── __init__.py
│   │   ├── routes.py     # Routes for token generation and validation
│   │   ├── utils.py      # Helper functions (e.g., generate_token, check_tok)
│   ├── templates/        # HTML templates
│   │   ├── base.html     # Base template for consistent layout
│   │   ├── home.html     # Home page template
│   │   ├── generate_token.html
│   │   ├── check_token.html
│   ├── static/           # Static files (CSS, JS, etc.)
├── info.json             # JSON file to store tokens
├── run.py                # Entry point to run the application
├── README.md             # Project documentation
```

---

### Code Implementation

#### 1. `app/__init__.py`
This file initializes the Flask app and registers the blueprints.

```python
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secure_secret_key'

    # Register Blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
```

---

#### 2. `app/auth/__init__.py`
This file initializes the `auth` blueprint.

```python
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from app.auth import routes
```

---

#### 3. `app/auth/routes.py`
This file contains the routes for token generation and validation.

```python
from flask import render_template, jsonify, request
from datetime import datetime, timedelta
import json
import random
import string
from .utils import generate_token, check_tok
from app.auth import auth_bp

# Home Page
@auth_bp.route('/')
def home():
    return render_template('home.html')

# Token Generation Page
@auth_bp.route('/generate_token')
def gen():
    return render_template('generate_token.html')

# Token Generation Response
@auth_bp.route('/generate_token_res')
def gen_res():
    file = 'info.json'
    days = request.args.get('length', type=int)

    if days <= 0:
        return jsonify({"error": "Invalid duration. Must be greater than 0."}), 400

    token = generate_token(file, days)
    if token:
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Failed to generate token."}), 500

# Token Check Page
@auth_bp.route('/check_token')
def index():
    return render_template('check_token.html')

# Token Check Response
@auth_bp.route('/check_token_res', methods=['GET'])
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
```

---

#### 4. `app/auth/utils.py`
This file contains helper functions for token generation and validation.

```python
from datetime import datetime, timedelta
import json
import random
import string

def generate_token(file, end_date):
    try:
        expiration_time = datetime.now() + timedelta(days=end_date)
        with open(file, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            data[token] = {"time": expiration_time.isoformat()}
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        return token
    except (FileNotFoundError, json.JSONDecodeError):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def check_tok(file, token):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            token_data = data.get(token, {})
            return token_data.get('time')
    except (FileNotFoundError, json.JSONDecodeError):
        return None
```

---

#### 5. `app/templates/base.html`
A base template for consistent layout across all pages.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Token Management System</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>Token Management System</h1>
            <nav>
                <a href="{{ url_for('auth.home') }}">Home</a>
                <a href="{{ url_for('auth.gen') }}">Generate Token</a>
                <a href="{{ url_for('auth.index') }}">Check Token</a>
            </nav>
        </header>
        <main>
            {% block content %}{% endblock %}
        </main>
    </div>
</body>
</html>
```

---

#### 6. `app/templates/home.html`
Home page template.

```html
{% extends "base.html" %}

{% block content %}
    <h2>Welcome to the Token Management System</h2>
    <p>Use the navigation links above to generate or check tokens.</p>
{% endblock %}
```

---

#### 7. `app/templates/generate_token.html`
Token generation page template.

```html
{% extends "base.html" %}

{% block content %}
    <h2>Generate Token</h2>
    <input type="number" id="lengthInput" placeholder="Enter token expiration (in days)" min="1">
    <button id="generateBtn">Generate Token</button>
    <div id="result"></div>
    <script src="{{ url_for('static', filename='generate_token.js') }}"></script>
{% endblock %}
```

---

#### 8. `app/templates/check_token.html`
Token validation page template.

```html
{% extends "base.html" %}

{% block content %}
    <h2>Check Token</h2>
    <input type="text" id="Token" placeholder="Enter Token">
    <button id="checkBtn">Check Token</button>
    <div id="result"></div>
    <script src="{{ url_for('static', filename='check_token.js') }}"></script>
{% endblock %}
```

---

#### 9. `run.py`
Entry point to run the application.

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

---

### How to Run the Project
1. Navigate to the project directory:
   ```bash
   cd token-management-system
   ```

2. Run the application:
   ```bash
   python run.py
   ```

3. Open your browser and navigate to `http://127.0.0.1:5000`.

---
