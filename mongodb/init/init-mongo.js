db = db.getSiblingDB('bookkeeping');

// creating collections
db.createCollection('users');
db.createCollection('books');

// sample data
db.users.insertMany([
    {id: "user1", name: "Maddy", email: "maddy@example.com", password: "password123", wishlist:["book1", "book2"], inventory:["book3", "book4"]},
    {id: "user2", name: "John", email: "john@example.com", password: "password123", wishlist:["book5", "book3"], inventory:["book1", "book6"]},
])

db.books.insertMany([
    {id: "book1", title: "No Longer Human", author: "Osamu Dazai"},
    {id: "book2", title: "Gulliver's Travels", author: "Jonathan Swift"},
    {id: "book3", title: "To Kill a Mockingbird", author: "Harper Lee"},
    {id: "book4", title: "1984", author: "George Orwell"},
    {id: "book5", title: "War & Peace", author: "Leo Tolstoy"},
    {id: "book6", title: "Great Expectations", author: "Charles Dickens"},
])