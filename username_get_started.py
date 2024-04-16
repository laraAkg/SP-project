from flask import Flask, request, render_template, redirect, session
from general_database_operations import create_database
from user_database_operations import insert_user, check_username_exists
from country import get_random_countries
import random

# connection aufbau für DB dann mitgeben

# Create or connect to the SQLite database and create the Users table if it doesn't exist
create_database("users.db", '''CREATE TABLE IF NOT EXISTS Users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE NOT NULL)
                        ''')

app = Flask(__name__)

app.secret_key = 'BAD_SECRET_KEY'

def get_shuffled_country(first_option_country, second_option_country, third_option_country):
    """
    Shuffle the countries so that the correct answer is not always in the same position.
    """
    countries = [first_option_country, second_option_country, third_option_country]
    random.shuffle(countries)
    return countries[0]


@app.route('/quiz')
def quiz():
    """
    Render the quiz page.
    """
    username = session['username']
    random_countries = get_random_countries()
    first_option_country = random_countries[0]
    second_option_country = random_countries[1]
    third_answer_country =  random_countries[2]
    correct_country = get_shuffled_country(first_option_country, second_option_country, third_answer_country)
    # check the correct_country with user input
    return render_template('quiz.html', correct_country = correct_country ,first_option = first_option_country, second_option = second_option_country, third_option = third_answer_country, username=username)

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Render the home page where users can input their name.
    Save user's name to the database and redirect to the quiz page upon submission.
    """
    if request.method == 'POST':
        username = request.form['name']
        try:
            if check_username_exists(username):
                return render_template('user.html', message="User already exists!")

            else:
                insert_user(username)
                session['username'] = request.form['name']
                return redirect('/quiz')
        except Exception as e:
            return f'Error saving user: {str(e)}'
    return render_template('user.html')


if __name__ == '__main__':
    app.run(debug=True)


# Regex for username
# Session to know User

# read all user inputs from quiz.html and store into db