"""
This module contains a Flask application that allows users to enter their name and email address.
"""
from flask import Flask, request, render_template
from general_database_operations import create_database
from countries_database_operations import get_country_entry_by_random_number
from user_database_operations import insert_user, check_email_exists


create_database("users.db",'''CREATE TABLE IF NOT EXISTS Users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            email TEXT UNIQUE)
                        ''')


app = Flask(__name__)
@app.route('/quiz')
def quiz():
    """
    Renders the quiz.html template.

    Returns:
        The rendered quiz.html template.
    """

    country_entry = get_country_entry_by_random_number()
    return render_template('quiz.html', country_entry=country_entry)

@app.route('/')
def home():
    """
    Renders the user.html template.

    Returns:
        The rendered user.html template.
    """
    return render_template('user.html')

@app.route('/save_user', methods=['POST'])
def save_user():
    """
    Saves a user's name and email to the database.

    Returns:
        str: A success message indicating that the user has been saved successfully.
    """
    name = request.form['name']
    email = request.form['email']
    try:
        # Check if user already exists in the database
        if check_email_exists("users.db", email):
            return "User already exists"
        else:
            insert_user("users.db", name, email)
            return quiz()  # Show the quiz.html template

    except Exception as e:
        return f'Error saving user: {str(e)}'

@app.route('/user_form', methods=['GET'])
def user_form():
    """
    Renders the user_form.html template.

    Returns:
        The rendered user_form.html template.
    """
    return render_template('user_form.html')

if __name__ == '__main__':
    app.run()


# TODO 1: check if email is already in db if yes return error message
# TODO 2: navigate to quiz.html if user is saved successfully
# TODO 3: use REGEX to validate email address & username