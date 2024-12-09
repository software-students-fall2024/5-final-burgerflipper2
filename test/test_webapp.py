import pytest
from app.main import app

@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_app_exists():
    """Test that the app exists."""
    assert app is not None

def test_home_redirect(client):
    """Test that the home page redirects to login when not authenticated."""
    response = client.get('/')
    assert response.status_code == 302  # Redirect status code
    assert '/login' in response.headers['Location']

def test_login_page(client):
    """Test that the login page loads."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_signup_page(client):
    """Test that the signup page loads."""
    response = client.get('/signup')
    assert response.status_code == 200
    assert b'Sign up' in response.data
