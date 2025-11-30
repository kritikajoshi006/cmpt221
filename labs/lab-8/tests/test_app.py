# TODO: add five more unit test cases

def test_home_page(client):
    """Test that home page loads"""
    response = client.get('/')
    assert response.status_code == 200

def test_login_page(client):
    """Test that home page loads"""
    response = client.get('/login')
    assert response.status_code == 200

def test_users_page(client):
    """Test that users page loads"""
    response = client.get('/users')
    assert response.status_code == 200

def test_invalid_first_name(client):
    """Test signup validation for invalid first name"""
    response = client.post('/signup', data={
        'FirstName': '123',  # invalid - contains numbers
        'LastName': 'Doe',
        'Email': 'test@test.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    assert b'First name can only contain letters' in response.data

def test_invalid_phone_number(client):
    """Test signup validation for invalid phone number"""
    response = client.post('/signup', data={
        'FirstName': 'John',
        'LastName': 'Doe',
        'Email': 'test@test.com',
        'PhoneNumber': '123',  # invalid - not 10 digits
        'Password': 'password123'
    })
    assert b'Phone number must be exactly 10 digits' in response.data

def test_wrong_password(client):
    """Test login fails with incorrect password"""
    response = client.post('/login', data={
        'Email': 'existinguser@test.com',
        'Password': 'wrongpassword'
    })
    assert b'Failed login attempt' in response.data or b'error' in response.data

def test_nonexistent_email(client):
    """Test login fails with an email that doesn't exist"""
    response = client.post('/login', data={
        'Email': 'nonexistent@test.com',
        'Password': 'password123'
    })
    assert b'Failed login attempt' in response.data or b'error' in response.data

def test_success_page_access(client):
    """Test that success page loads"""
    response = client.get('/success')
    assert response.status_code == 200
    assert b'Success' in response.data

def test_error_page_access(client):
    """Test that error page loads"""
    response = client.get('/error')
    assert response.status_code == 200
    assert b'Something went wrong' in response.data or b'error' in response.data