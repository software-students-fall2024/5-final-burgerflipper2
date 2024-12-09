import os
from flask import Flask, render_template
import pymongo
import gridfs
from dotenv import load_dotenv
import flask_login
from login import init_login, create_login_routes
from bson import ObjectId

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

@app.route('/user')
@flask_login.login_required
def user():
    # HARDCODED! CHANGE LATER
    # WHEN LOGIN/LOGOUT FUNCTION IS ADDED
    user_id = "user1"

    user = db.users.find_one({"id": user_id}, {"_id": 0, "name": 1, "wishlist": 1, "inventory": 1})
    if not user:
        print("User not found for ID:", user_id)
        return "User not found", 404

    inventory = list(
        db.books.find(
            {"id": {"$in": user["inventory"]}},
            {"_id": 0, "title": 1, "author": 1, "description": 1}
        )
    )

    wishlist = list(
        db.books.find(
            {"id": {"$in": user["wishlist"]}},
            {"_id": 0, "title": 1, "author": 1, "description": 1}
        )
    )

    return render_template('user.html', name=user["name"], inventory=inventory, wishlist=wishlist)


@app.route('/matches')
@flask_login.login_required
def matches():
    # HARDCODED! CHANGE LATER
    # WHEN LOGIN/LOGOUT FUNCTION IS ADDED
    current_user_id = "user1"

    user = db.users.find_one({"id": current_user_id}, {"_id": 0, "name": 1, "wishlist": 1, "inventory": 1})
    
    if not user:
        print(f"User not found for ID: {current_user_id}")
        return "User not found", 404

    inventory = list(
        db.books.find(
            {"id": {"$in": user["inventory"]}},
            {"_id": 0, "title": 1, "author": 1, "description": 1}
        )
    )

    wishlist = list(
        db.books.find(
            {"id": {"$in": user["wishlist"]}},
            {"_id": 0, "title": 1, "author": 1, "description": 1}
        )
    )

    matches = []

    for other_user in db.users.find({"id": {"$ne": current_user_id}}):
        other_inventory = set(other_user.get("inventory", []))
        other_wishlist = set(other_user.get("wishlist", []))

        give_books = set(user["inventory"]).intersection(other_wishlist)
        receive_books = set(user["wishlist"]).intersection(other_inventory)

        if give_books and receive_books:
            matches.append({
                "name": other_user["name"],
                "give_books": list(db.books.find({"id": {"$in": list(give_books)}}, {"_id": 0, "title": 1, "author": 1})),
                "receive_books": list(db.books.find({"id": {"$in": list(receive_books)}}, {"_id": 0, "title": 1, "author": 1}))
            })

    if not matches:
        print("No matches found!")
        message = "No swaps were found with other users!"
        return render_template('matches.html', matches=None, message=message, inventory=inventory, wishlist=wishlist)

    print(f"Found {len(matches)} matches")
    
    return render_template('matches.html', matches=matches, inventory=inventory, wishlist=wishlist)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
