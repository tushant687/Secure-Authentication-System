from pathlib import Path

# Define the code content for the Jupyter Notebook
notebook_code = """
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install Flask flask_sqlalchemy pyjwt bcrypt psycopg2-binary"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, request, jsonify\\n",
    "from flask_sqlalchemy import SQLAlchemy\\n",
    "import bcrypt\\n",
    "import jwt\\n",
    "import datetime"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Initialize Flask app\\n",
    "app = Flask(__name__)\\n",
    "\\n",
    "# Secret key for JWT\\n",
    "app.config['SECRET_KEY'] = 'your_secret_key'\\n",
    "# PostgreSQL configuration (Replace with actual credentials)\\n",
    "app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'\\n",
    "db = SQLAlchemy(app)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# User model\\n",
    "class User(db.Model):\\n",
    "    id = db.Column(db.Integer, primary_key=True)\\n",
    "    username = db.Column(db.String(80), unique=True, nullable=False)\\n",
    "    password = db.Column(db.LargeBinary, nullable=False)\\n",
    "\\n",
    "# Create tables\\n",
    "with app.app_context():\\n",
    "    db.create_all()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Register route\\n",
    "@app.route('/register', methods=['POST'])\\n",
    "def register():\\n",
    "    data = request.get_json()\\n",
    "    username = data['username']\\n",
    "    password = data['password'].encode('utf-8')\\n",
    "\\n",
    "    if User.query.filter_by(username=username).first():\\n",
    "        return jsonify({'message': 'Username already exists'}), 409\\n",
    "\\n",
    "    hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())\\n",
    "    new_user = User(username=username, password=hashed_pw)\\n",
    "\\n",
    "    db.session.add(new_user)\\n",
    "    db.session.commit()\\n",
    "\\n",
    "    return jsonify({'message': 'User registered successfully'}), 201"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Login route\\n",
    "@app.route('/login', methods=['POST'])\\n",
    "def login():\\n",
    "    data = request.get_json()\\n",
    "    username = data['username']\\n",
    "    password = data['password'].encode('utf-8')\\n",
    "\\n",
    "    user = User.query.filter_by(username=username).first()\\n",
    "\\n",
    "    if user and bcrypt.checkpw(password, user.password):\\n",
    "        token = jwt.encode({\\n",
    "            'user_id': user.id,\\n",
    "            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)\\n",
    "        }, app.config['SECRET_KEY'], algorithm='HS256')\\n",
    "\\n",
    "        return jsonify({'token': token}), 200\\n",
    "    else:\\n",
    "        return jsonify({'message': 'Invalid credentials'}), 401"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Protected route\\n",
    "@app.route('/protected', methods=['GET'])\\n",
    "def protected():\\n",
    "    token = request.headers.get('Authorization')\\n",
    "\\n",
    "    if not token:\\n",
    "        return jsonify({'message': 'Token is missing!'}), 403\\n",
    "\\n",
    "    try:\\n",
    "        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])\\n",
    "        user = User.query.get(data['user_id'])\\n",
    "    except:\\n",
    "        return jsonify({'message': 'Token is invalid or expired!'}), 403\\n",
    "\\n",
    "    return jsonify({'message': f'Welcome {user.username}!'}), 200"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Run Flask app\\n",
    "from threading import Thread\\n",
    "\\n",
    "def run_app():\\n",
    "    app.run(port=5000)\\n",
    "\\n",
    "thread = Thread(target=run_app)\\n",
    "thread.start()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": ""
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
"""

# Save to .ipynb file
file_path = Path("secure_auth_system.ipynb")
file_path.write_text(notebook_code)

file_path

