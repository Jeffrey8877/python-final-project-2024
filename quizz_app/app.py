from xmlrpc.client import DateTime

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from functools import wraps  # Used for creating decorators
import os

from IPBlocking import check_ip
from models.quiz import Quiz
from models.user import User
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)
# Load configuration from config.py file
app.config.from_object('config')

def get_db_connection():
    """
    Create and return a database connection.

    SQLite3 Connection object has a row_factory attribute that determines how rows are returned.
    sqlite3.Row allows us to access columns by name instead of just index.
    """
    conn = sqlite3.connect('database/quiz.db')
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    return conn

def login_required(f):
    """
    A decorator function that checks if a user is logged in before allowing access to a route.

    Args:
        f: The function to be decorated (will be a route function)

    How this works:
    1. This is a decorator - a function that wraps another function to add functionality
    2. When applied using @login_required above a route, this code runs before the route
    3. *args and **kwargs allow the decorator to work with any route function regardless
       of what arguments it takes
       - *args collects all positional arguments into a tuple
       - **kwargs collects all keyword arguments into a dictionary
    """
    @wraps(f)  # This preserves the original function's metadata
    def decorated_function(*args, **kwargs):
        # Check if 'user_id' exists in the session
        # Session is like a dictionary that persists across requests
        if 'user_id' not in session:
            # If no user_id in session, the user isn't logged in
            flash('Please log in first.', 'error')  # Show error message to user
            return redirect(url_for('login'))  # Redirect to login page
        # If user is logged in, call the original route function
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """
    Home page route.
    The @app.route decorator tells Flask what URL should trigger this function.
    """

    conn = get_db_connection()
    quizzes = Quiz.get_all(conn)
    # quiz = Quiz.get_by_id(conn, 1) # TODO: Remove Magic Number 1, Get all quizzes instead
    conn.close()
    return render_template('index.html', quizzes=quizzes, session=session)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.

    This route handles both:
    - GET requests: Display the registration form
    - POST requests: Process the form submission

    The methods=['GET', 'POST'] in the decorator specifies which HTTP methods are allowed.
    """
    if request.method == 'POST':
        # Get form data from request.form (similar to a dictionary)
        username = request.form['username']
        # TODO: Student task - Add password hashing here
        password = request.form['password']
        email = request.form['email']

        # Get database connection
        conn = get_db_connection()

        # Check if username already exists
        if User.get_by_username(conn, username):
            flash('Username already exists. Please sign in.', 'error')
            conn.close()
            return redirect(url_for('login'))

        try:
            # Attempt to create new user
            User.create(conn, username, password, email)
            # If successful, commit the transaction
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            # If any error occurs, rollback the transaction
            conn.rollback()
            flash('Registration failed. Please try again.', 'error')
        finally:
            # Always close the connection, whether successful or not
            conn.close()

    # If it's a GET request, just show the registration form
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    Similar to register:
    - GET request shows the login form
    - POST request processes the login attempt

    Session is used to keep track of logged-in users:
    - When a user logs in successfully, we store their user_id in the session
    - This session data persists across requests until they log out
    """
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # TODO: Student will implement password hashing

        conn = get_db_connection()
        user = User.get_by_username(conn, username)
        conn.close()

        # Basic password check
        # TODO: Student task - Replace with secure password comparison
        if not user:
            return render_template('login.html')

        if user['password'] != password:
            flash('Invalid credentials.', 'error')
            return render_template('login.html')

        # Store user info in session to keep them logged in
        session['user_id'] = user['id']
        session['username'] = user['username']
        flash('Welcome back!', 'success')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """
    Handle user logout.

    session.clear() removes all data from the session, effectively logging the user out.
    """
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/quiz/<int:quiz_id>')
@login_required  # This decorator ensures only logged-in users can access this route
def take_quiz(quiz_id):
    """
    Route for taking a specific quiz.

    The <int:quiz_id> in the route is a URL parameter:
    - Flask converts it to an integer
    - Passes it to the function as quiz_id
    - Example URL: /quiz/1 would set quiz_id = 1
    """
    conn = get_db_connection()
    quiz = Quiz.get_by_id(conn, quiz_id)
    conn.close()

    if not quiz:
        flash('Quiz not found.', 'error')
        return redirect(url_for('index'))

    return render_template('quiz.html', quiz=quiz)

@app.route('/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """
    Handle quiz submission.

    request.form.to_dict() converts form data to a Python dictionary:
    - Keys are the form field names
    - Values are what the user submitted
    Example: {'question1': 'selected_answer', 'question2': 'selected_answer'}
    """
    print('submit quizz')
    answers = request.form.to_dict()
    conn = get_db_connection()
    quiz = Quiz.get_by_id(conn, quiz_id)
    score = Quiz.grade_submission(conn,quiz_id,answers)

    # Save results to database
    user_id = session['user_id']  # Get current user's ID from session
    Quiz.save_result(conn, user_id, quiz_id, score)
    conn.close()

    flash(f'Quiz submitted! Your score: {score}%', 'success')
    return redirect(url_for('results', quiz_id=quiz_id))

@app.route('/results/<int:quiz_id>')
@login_required
def results(quiz_id):
    """
    Show quiz results.

    This route:
    1. Gets the quiz from the database
    2. Gets the user's result for this quiz
    3. Displays both using the results.html template
    """
    print('results')
    conn = get_db_connection()
    quiz = Quiz.get_by_id(conn, quiz_id)
    user_id = session['user_id']
    # result = Quiz.get_user_result(conn, user_id)
    conn.close()

    result = {
        'score': session.get('score', 0),
        'completed_at': datetime.now()
    }
    return render_template('result.html', result=result, quiz=quiz)

@app.route('/api/your-endpoint', methods=['GET'])
@check_ip
def your_route():
    # Your normal route code here
    return jsonify({'error': 'blocked'}), 403

if __name__ == '__main__':
    """
    This block only runs if you execute this file directly
    (not if you import it as a module)
    """
    # Create the database directory if it doesn't exist
    os.makedirs('database', exist_ok=True)

    conn2 = get_db_connection()
    cursor = conn2.cursor()
    with open('schema.sql','r') as f:
        cursor.executescript(f.read())

    # Start the Flask development server in debug mode
    app.run(debug=True)