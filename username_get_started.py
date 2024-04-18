"""
This file contains the code for the username_get_started.py file.
It is a simple Flask application that allows users to input their name and start a quiz.
The quiz is about countries and their capitals.
The user's name is saved to a database and the quiz data is fetched from another database.
The user's score is displayed at the end of the quiz.
"""
import random
import sqlite3
import re
from flask import Flask, request, render_template, redirect, session
from user_database_operations import insert_user, check_username_exists, create_tables_for_user_db,get_user_score
from countries_database_operations import get_random_countries
from countries_database_setup import create_tables_for_country_db, fetch_and_insert_data

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'


def get_shuffled_country(first_option_country, second_option_country, third_option_country):
    """
    Shuffle the countries so that the correct answer is not always in the same position.
    """
    countries = [first_option_country, second_option_country, third_option_country]
    random.shuffle(countries)
    return countries[0]


def get_random_quiz_data(country_connection, quiz_type):
    """
    Generates random quiz data for a country quiz game.

    Parameters:
    - country_connection: The connection to the country database.

    Returns:
    - first_option_country: The first option country for the quiz.
    - second_option_country: The second option country for the quiz.
    - third_answer_country: The third answer country for the quiz.
    - correct_country: The correct country for the quiz.

    """
    random_countries = get_random_countries(country_connection)

    # Ensure no duplicate countries
    while True:
        first_option_country, second_option_country, third_answer_country = random.sample(random_countries, 3)
        if(quiz_type == 'capital'):
            if first_option_country.capital != second_option_country.capital != third_answer_country.capital:
                break
        elif(quiz_type == 'continent'):
            if first_option_country.continent != second_option_country.continent != third_answer_country.continent:
                break
        elif(quiz_type == 'area'):
            if first_option_country.area != second_option_country.area != third_answer_country.area:
                break
        else:
            if first_option_country != second_option_country != third_answer_country:
                break

    correct_country = get_shuffled_country(first_option_country, second_option_country, third_answer_country)
    return first_option_country, second_option_country, third_answer_country, correct_country


@app.route('/quiz/capital', methods=['GET', 'POST'])
def quiz_capital():
    """
    Render the quiz page for capital.
    """
    country_connection = sqlite3.connect("database/countries.db")

    first_option_country, second_option_country, third_answer_country, correct_country = get_random_quiz_data(country_connection, 'capital')
    if request.method == 'GET':
        session['first_option_country'] = first_option_country.capital
        session['second_option_country'] = second_option_country.capital
        session['third_answer_country'] = third_answer_country.capital
        session['correct_country'] = correct_country.capital


    if request.method == 'POST':
        user_input = request.form['option']
        correct_country_from_session = session['correct_country']
        if user_input in correct_country_from_session:
            return redirect('/quiz/continent')
        else:
            return redirect('/quiz/score')
    return render_template('webpages/quiz_capital.html', first_option=first_option_country, second_option=second_option_country, third_option=third_answer_country, correct_country=correct_country)


@app.route('/quiz/continent', methods=['GET', 'POST'])
def quiz_continent():
    """
    Render the quiz page for continents.
    """
    country_connection = sqlite3.connect("database/countries.db")

    first_option_country, second_option_country, third_answer_country, correct_country = get_random_quiz_data(country_connection, 'continent')
    if request.method == 'GET':
        session['first_option_country'] = first_option_country.continent
        session['second_option_country'] = second_option_country.continent
        session['third_answer_country'] = third_answer_country.continent
        session['correct_country'] = correct_country.continent


    if request.method == 'POST':
        user_input = request.form['option']
        correct_country_from_session = session['correct_country']
        if user_input in correct_country_from_session:
            return redirect('/quiz/population')
        else:
            return redirect('/quiz/score')
    return render_template('webpages/quiz_continent.html', first_option=first_option_country, second_option=second_option_country, third_option=third_answer_country, correct_country=correct_country)

@app.route('/quiz/area', methods=['GET', 'POST'])
def quiz_area():
    """
    Render the quiz page for area.
    """
    country_connection = sqlite3.connect("database/countries.db")

    first_option_country, second_option_country, third_answer_country, correct_country = get_random_quiz_data(country_connection, 'area')
    if request.method == 'GET':
        session['first_option_country'] = first_option_country.area
        session['second_option_country'] = second_option_country.area
        session['third_answer_country'] = third_answer_country.area
        session['correct_country'] = correct_country.area


    if request.method == 'POST':
        user_input = request.form['option']
        correct_country_from_session = session['correct_country']
        if user_input in correct_country_from_session:
            return redirect('/quiz/population')
        else:
            return redirect('/quiz/score')
    return render_template('webpages/quiz_continent.html', first_option=first_option_country, second_option=second_option_country, third_option=third_answer_country, correct_country=correct_country)


@app.route('/quiz/score', methods=['GET', 'POST'])
def quiz_score():
    """
    Render the score page.
    """
    return render_template('webpages/score.html')


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
            return render_template('webpages/index.html', message="Invalid username! Username must be 4-8 characters long and can only contain letters, numbers, and underscores.")
        if check_username_exists(user_connection, username):
            return render_template('webpages/index.html', message="User already exists!")
        else:
            insert_user(user_connection, username)
            session['username'] = username
            return redirect('/quiz/capital')
    return render_template('webpages/index.html')


if __name__ == '__main__':
    app.run(debug=True)
