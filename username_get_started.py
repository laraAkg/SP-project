"""
This file contains the code for the username_get_started.py file.
It is a simple Flask application that allows users to input their name and start a quiz.
The quiz is about countries and their capitals.
The user's name is saved to a database and the quiz data is fetched from another database.
The user's score is displayed at the end of the quiz.
"""
import sqlite3
import re
from flask import Flask, request, render_template, redirect, session
from user_database_operations import insert_user, check_username_exists, create_tables_for_user_db
from countries_database_setup import create_tables_for_country_db, fetch_and_insert_data
from help_services import get_random_quiz_data

app = Flask(__name__, static_folder='static')
app.secret_key = 'BAD_SECRET_KEY'


@app.route('/quiz/capital', methods=['GET'])
def render_capital_quiz_page():
    """
    Renders the capital quiz page.

    This function connects to the 'countries.db' SQLite database and retrieves random quiz data
    for the capital quiz. It sets the session variables for the options and correct answer,
    and then renders the 'quiz_capital.html' template with the retrieved data.

    Returns:
        The rendered template for the capital quiz page.
    """
    country_connection = sqlite3.connect("database/countries.db")

    first_option_country, second_option_country, third_option_country, correct_country = get_random_quiz_data(
        country_connection, 'capital')
    session['first_option_country'] = first_option_country.capital
    session['second_option_country'] = second_option_country.capital
    session['third_option_country'] = third_option_country.capital
    session['correct_country'] = correct_country.capital
    return render_template('quiz_capital.html', first_option=first_option_country, second_option=second_option_country, third_option=third_option_country, correct_country=correct_country)


@app.route('/quiz/capital', methods=['POST'])
def process_capital_quiz_submission():
    """
    Process the submission of a capital quiz answer.

    This function retrieves the user's input from the form, compares it with the correct country stored in the session,
    and redirects the user to the appropriate page based on the correctness of the answer.

    Returns:
        A redirect response to either '/quiz/continent' or '/quiz/score' based on the correctness of the answer.
    """
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    print(correct_country_from_session, user_input)
    if user_input in correct_country_from_session:
        return redirect('/quiz/continent')
    else:
        return redirect('/quiz/score')


@app.route('/quiz/continent', methods=['GET'])
def render_continent_quiz_page():
    """
    Renders the continent quiz page.

    This function connects to the 'countries.db' SQLite database and retrieves random quiz data
    for the continent quiz. It sets the session variables for the options and correct country,
    and then renders the 'quiz_continent.html' template with the retrieved data.

    Returns:
        The rendered template for the continent quiz page.
    """
    country_connection = sqlite3.connect("database/countries.db")

    first_option_country, second_option_country, third_option_country, correct_country = get_random_quiz_data(
        country_connection, 'continent')
    session['first_option_country'] = first_option_country.continent
    session['second_option_country'] = second_option_country.continent
    session['third_option_country'] = third_option_country.continent
    session['correct_country'] = correct_country.continent
    return render_template('quiz_continent.html', first_option=first_option_country, second_option=second_option_country, third_option=third_option_country, correct_country=correct_country)

@app.route('/quiz/continent', methods=['POST'])
def process_continent_quiz_submission():
    """
    Render the quiz page for continents.
    """
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    if user_input in correct_country_from_session:
        return redirect('/quiz/population')
    else:
        return redirect('/quiz/score')


@app.route('/quiz/population', methods=['GET', 'POST'])
def quiz_population():
    """
    Render the quiz page for population.
    """
    country_connection = sqlite3.connect("database/countries.db")

    if request.method == 'GET':
        first_option_country, second_option_country, third_option_country, correct_country = get_random_quiz_data(
            country_connection, 'population')
        session['first_option_country'] = first_option_country.population
        session['second_option_country'] = second_option_country.population
        session['third_option_country'] = third_option_country.population
        session['correct_country'] = correct_country.population
        return render_template('quiz_population.html', first_option=first_option_country, second_option=second_option_country, third_option=third_option_country, correct_country=correct_country)

    if request.method == 'POST':
        user_input = request.form['option']
        correct_country_from_session = session['correct_country']
        if int(user_input) == correct_country_from_session:
            return redirect('/quiz/area')
        else:
            return redirect('/quiz/score')


@app.route('/quiz/area', methods=['GET', 'POST'])
def quiz_area():
    """
    Render the quiz page for area.
    """
    country_connection = sqlite3.connect("database/countries.db")

    if request.method == 'GET':
        first_option_country, second_option_country, third_option_country, correct_country = get_random_quiz_data(
            country_connection, 'area')
        session['first_option_country'] = first_option_country.area
        session['second_option_country'] = second_option_country.area
        session['third_option_country'] = third_option_country.area
        session['correct_country'] = correct_country.area
        return render_template('quiz_area.html', first_option=first_option_country, second_option=second_option_country, third_option=third_option_country, correct_country=correct_country)

    if request.method == 'POST':
        user_input = request.form['option']
        correct_country_from_session = session['correct_country']
        if user_input in correct_country_from_session:
            return redirect('/quiz/population')
        else:
            return redirect('/quiz/score')


@app.route('/quiz/score', methods=['GET', 'POST'])
def quiz_score():
    """
    Render the score page.
    """
    session.clear()
    return render_template('score.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Render the home page where users can input their name.
    Save user's name to the database and redirect to the quiz page upon submission.
    """

    user_connection = sqlite3.connect("database/user.db")

    create_tables_for_user_db(user_connection)
    country_connection = sqlite3.connect("database/countries.db")
    create_tables_for_country_db(country_connection)
    fetch_and_insert_data(country_connection)

    if request.method == 'POST':
        username = request.form['name']
        if not re.match(r'^[a-zA-Z0-9_]{4,8}', username):
            return render_template('index.html', message="Invalid username! Username must be 4-8 characters long and can only contain letters, numbers, and underscores.")
        if check_username_exists(user_connection, username):
            return render_template('index.html', message="User already exists!")
        else:
            insert_user(user_connection, username)
            session['username'] = username
            return redirect('/quiz/capital')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


# todo: trennen von get post
# random number logic into new file
# username file rename
# html for languge and boarder
# currency display?
# give score to user
