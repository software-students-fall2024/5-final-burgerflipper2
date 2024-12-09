import pytest
from unittest.mock import Mock, patch
from mongodb.database import get_users, add_user, get_books, add_book, get_matches, add_match

# Mock data for testing
mock_users = [
    {"id": "user1", "name": "Maddy", "wishlist": ["book1", "book2"], "inventory": ["book3", "book4"]},
    {"id": "user2", "name": "John", "wishlist": ["book5", "book3"], "inventory": ["book1", "book6"]}
]

mock_books = [
    {"id": "book1", "title": "No Longer Human", "author": "Osamu Dazai"},
    {"id": "book2", "title": "Gulliver's Travels", "author": "Jonathan Swift"}
]

mock_matches = [
    {"user1": "user1", "user2": "user2", "book1": "book1", "book2": "book3"}
]

@pytest.fixture
def mock_db():
    with patch('mongodb.database.db') as mock_db:
        # Configure mock collections
        mock_db.users.find.return_value = mock_users
        mock_db.books.find.return_value = mock_books
        mock_db.matches.find.return_value = mock_matches
        yield mock_db

def test_get_users(mock_db):
    users = get_users()
    assert len(users) == 2
    assert users[0]["name"] == "Maddy"
    assert users[1]["name"] == "John"
    mock_db.users.find.assert_called_once()

def test_add_user(mock_db):
    new_user = {"id": "user3", "name": "Alice", "wishlist": [], "inventory": []}
    add_user(new_user)
    mock_db.users.insert_one.assert_called_once_with(new_user)

def test_get_books(mock_db):
    books = get_books()
    assert len(books) == 2
    assert books[0]["title"] == "No Longer Human"
    assert books[1]["title"] == "Gulliver's Travels"
    mock_db.books.find.assert_called_once()

def test_add_book(mock_db):
    new_book = {"id": "book7", "title": "New Book", "author": "New Author"}
    add_book(new_book)
    mock_db.books.insert_one.assert_called_once_with(new_book)

def test_get_matches(mock_db):
    matches = get_matches()
    assert len(matches) == 1
    assert matches[0]["user1"] == "user1"
    assert matches[0]["user2"] == "user2"
    mock_db.matches.find.assert_called_once()

def test_add_match(mock_db):
    new_match = {"user1": "user1", "user2": "user3", "book1": "book2", "book2": "book4"}
    add_match(new_match)
    mock_db.matches.insert_one.assert_called_once_with(new_match)
