"""app.py: render and route to webpages"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from db.query import get_all, insert, get_one
from db.server import init_database
from db.schema import Users


# load environment variables from .env
load_dotenv()


# database connection - values set in .env
db_name = os.getenv('db_name')
db_owner = os.getenv('db_owner')
db_pass = os.getenv('db_pass')
print(f"db_name={db_name}, db_owner={db_owner}, db_pass={db_pass}")
db_url = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

def create_app():
    """Create Flask application and connect to your DB"""
    # create flask app 
    app = Flask(__name__, 
                template_folder=os.path.join(os.getcwd(), 'templates'), 
                static_folder=os.path.join(os.getcwd(), 'static'))
    
    
    # connect to db
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    
    # Initialize database
    with app.app_context():
        if not init_database():
            print("Failed to initialize database. Exiting.")
            exit(1)

    # ===============================================================
    # routes
    # ===============================================================

    # create a webpage based off of the html in templates/index.html
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        """Sign up page: enables users to sign up"""
        if request.method == 'POST':
            user = Users(
                FirstName=request.form.get('FirstName'),
                LastName=request.form.get('LastName'),
                Email=request.form.get('Email'),
                Password=request.form.get('Password'),
                PhoneNumber=request.form.get('PhoneNumber')
            )

        error: str = None
        is_valid: bool = False

        if is_valid: 
            insert_stmt = insert(User).values(request.form)
            
        if request.method["FirstName"].isalpha():
            print(f'Input: {request.form["FirstName"]} is valid.')
            is_valid = True
        else:
            error_message = f'Input: {request.form["FirstName"]} is invalid. First Name can only contain letters.'
            print(f'Input: {request.form["FirstName"]} is invalid.')
            
            error = error_message

            insert(user)
            return redirect(url_for('success'))
        
        return render_template('signup.html')
    
    @app.route('/login', methods=['GET', 'POST']) 
    def login(): 
        if request.method == 'POST':
            email = request.form.get('Email')
            password = request.form.get('Password')
            user = get_one(Users, Users.Email, email)
            
            if user and user.Password == password:
                return redirect(url_for('success'))
            else: 
                return redirect(url_for('login'))

        return render_template('login.html')


    @app.route('/users')
    def users():
        """Users page: displays all users in the Users table"""
        all_users = get_all(Users)
        
        return render_template('users.html', users=all_users)

    @app.route('/success')
    def success():
        """Success page: displayed upon successful login"""

        return render_template('success.html')

    return app

if __name__ == "__main__":
    app = create_app()
   
    app.run(debug=True)
