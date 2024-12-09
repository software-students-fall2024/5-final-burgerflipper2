from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId #to handle mongodb's objectid type
import flask_login
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

login_manager = flask_login.LoginManager()
login_manager.login_view = 'login'

# Database connection
MONGO_URI = os.getenv('MONGO_URI', "mongodb://localhost:27017")
db_name = os.getenv("DB_NAME", "bookkeeping")
client = MongoClient(MONGO_URI)
db = client[db_name]
users = db["users"]

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user_data = users.find_one({'_id': ObjectId(user_id)})
    if not user_data:
        return None
    
    user = User()
    user.id = str(user_data["_id"])
    return user

def init_login(app):
    login_manager.init_app(app)
    app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
    
def create_login_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if flask_login.current_user.is_authenticated:
            return redirect(url_for('protected'))
        
        if request.method == 'GET':
            return render_template('login.html')
        
        email = request.form['email'].strip().lower()
        data = users.find_one({'email': email})
        
        if data and request.form['password'].strip() == data['password']:
            user = User()
            user.id = str(data["_id"])
            flask_login.login_user(user)
            return redirect(url_for('protected'))
        return render_template('login.html', error = 'Invalid username or password')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            email = request.form['email'].strip().lower()
            password = request.form['password']
            
            if users.find_one({'email': email}):
                return render_template('signup.html', error='Email already exists')
            
            users.insert_one({'email': email, 'password': password})
            return redirect(url_for('login'))
        return render_template('signup.html')
    
    @app.route('/protected')
    @flask_login.login_required
    def protected():
        print(f'Logged in: {flask_login.current_user.id}')
        return redirect(url_for('home'))
    
    @app.route('/logout')
    @flask_login.login_required
    def logout():
        print(f'Logged out: {flask_login.current_user.id}')
        flask_login.logout_user()
        return redirect(url_for('login'))
    
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))