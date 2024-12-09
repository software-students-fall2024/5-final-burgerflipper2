from __init__ import app, db
from login import init_login, create_login_routes
from flask import Flask, render_template
import flask_login

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
    return render_template('matches.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
