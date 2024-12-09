import os
from flask import Flask, render_template, request, redirect, url_for
import pymongo
import gridfs
from dotenv import load_dotenv
import flask_login
from login import init_login, create_login_routes
from bson.objectid import ObjectId 

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)

# mongodb
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
db_name = os.getenv("DB_NAME", "bookkeeping")
client = pymongo.MongoClient(mongo_uri)
db = client[db_name]
users = db["users"]
fs = gridfs.GridFS(db)

# Initialize login
init_login(app)
create_login_routes(app)

@app.route('/')
@flask_login.login_required
def home():
    books = list(db.books.find({}, {"_id": 0, "title": 1, "author": 1, "description": 1}))
    return render_template('home.html', books=books)

@app.route('/search', methods=['GET'])
@flask_login.login_required
def search():
    query = request.args.get('query', '')
    # Search books by title, genre, or author
    books = list(db.books.find(
        {"$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"author": {"$regex": query, "$options": "i"}}
        ]}, 
        {"_id": 0, "title": 1, "author": 1, "description": 1}
    ))
    return render_template('home.html', books=books)

@app.route('/user')
@flask_login.login_required
def user():
    user_id = flask_login.current_user.id

    user = db.users.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "name": 1, "wishlist": 1, "inventory": 1})
    if not user:
        return "User not found", 404

    inventory = list(
        db.books.find(
            {"_id": {"$in": [ObjectId(book_id) for book_id in user.get("inventory", [])]}},
            {"_id": 0, "title": 1, "author": 1, "description": 1}
        )
    )

    wishlist = list(
        db.books.find(
            {"_id": {"$in": [ObjectId(book_id) for book_id in user.get("wishlist", [])]}},
            {"_id": 0, "title": 1, "author": 1, "description": 1}
        )
    )

    return render_template('user.html', name=user["name"], inventory=inventory, wishlist=wishlist)

@app.route('/matches')
@flask_login.login_required
def matches():
    return render_template('matches.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
