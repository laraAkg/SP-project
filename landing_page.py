"""
This script contains a Flask application that serves as a landing 
page for a quiz game about countries. The application allows users to answer questions
about various aspects of countries, such as their capitals, continents, population, area,
and currency. Users can earn points for correct answers and their scores are stored in a
SQLite database. The application also provides a highscore page to display the top ten scores
and the user's rank. Additionally, the application generates diagrams showing the top five
largest countries and the top five countries by population. The data for the quiz questions
and the country information is stored in a SQLite database.
"""

import os
import re
import sqlite3
import time
import matplotlib
from flask import Flask, redirect, render_template, request, session
from database_operations.countries_database_setup import (
    create_tables_for_country_db, fetch_and_insert_data)
from database_operations.user_database_operations import (
    check_username_exists, create_tables_for_user_db, get_rank_for_username,
    get_top_ten_score, set_user_score)
from help_services import get_random_quiz_data, return_options_for_continents
from visual_helper import (
    plot_top_five_largest_countries, plot_top_five_population_countries, hypothesis_test, get_correlation_coefficient)

matplotlib.use('Agg')

app = Flask(__name__, static_folder='static')
app.secret_key = 'BAD_SECRET_KEY'


@app.route('/quiz/capital', methods=['GET'])
def render_capital_quiz_page():
    """
    Renders the capital quiz page.

    Returns:
        The rendered template for the capital quiz page.
    """
    if session['status'] != 'level_up':
        session['score'] = 0
        session['status'] = 'beginner'
    connection = sqlite3.connect("database/countries.db")
    first_option, second_option, third_option, correct_option = get_random_quiz_data(
        connection, 'capital')
    session['first_option_country'] = first_option.capital
    session['second_option_country'] = second_option.capital
    session['third_option_country'] = third_option.capital
    session['correct_country'] = correct_option.capital
    return render_template('quiz_capital.html',
                           first_option=first_option,
                           second_option=second_option,
                           third_option=third_option,
                           correct_country=correct_option)


@app.route('/quiz/capital', methods=['POST'])
def process_capital_quiz_submission():
    """
    Process the user's submission for the capital quiz.

    Returns:
        A redirect response to either the next question or the score page.
    """
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    if user_input in correct_country_from_session:
        session['score'] += 50
        return redirect('/quiz/continent')
    return redirect('/quiz/score')


@app.route('/quiz/continent', methods=['GET'])
def render_continent_quiz_page():
    """
    Renders the continent quiz page.

    Returns:
        The rendered template for the continent quiz page.
    """
    connection = sqlite3.connect("database/countries.db")
    list_continents = return_options_for_continents(connection)
    session['first_option_country'] = list_continents[0].continent
    session['second_option_country'] = list_continents[1].continent
    session['third_option_country'] = list_continents[2].continent
    session['correct_country'] = list_continents[3].continent
    return render_template('quiz_continent.html',
                           first_option=list_continents[0],
                           second_option=list_continents[1],
                           third_option=list_continents[2],
                           correct_country=list_continents[3])


@app.route('/quiz/continent', methods=['POST'])
def process_continent_quiz_submission():
    """
    Process the user's submission for the continent quiz.

    Returns:
        A redirect response to the appropriate quiz page.
    """
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    if user_input in correct_country_from_session:
        session['score'] += 50
        return redirect('/quiz/population')
    return redirect('/quiz/score')


@app.route('/quiz/population', methods=['GET'])
def render_population_quiz_page():
    """
    Renders the population quiz page.

    Returns:
        The rendered population quiz page.
    """
    connection = sqlite3.connect("database/countries.db")
    first_country, second_country, third_country, correct_country = get_random_quiz_data(
        connection, 'population')
    session['first_option_country'] = first_country.population
    session['second_option_country'] = second_country.population
    session['third_option_country'] = third_country.population
    session['correct_country'] = correct_country.population
    return render_template('quiz_population.html',
                           first_option=first_country,
                           second_option=second_country,
                           third_option=third_country,
                           correct_country=correct_country)


@app.route('/quiz/population', methods=['POST'])
def process_population_quiz_submission():
    """
    Process the user's submission for the population quiz.

    Returns:
        A redirect response to the appropriate quiz page.
    """
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    if int(user_input) == correct_country_from_session:
        session['score'] += 50
        return redirect('/quiz/area')
    return redirect('/quiz/score')


@app.route('/quiz/area', methods=['GET'])
def render_area_quiz_page():
    """
    Renders the area quiz page.

    Returns:
        The rendered HTML template for the area quiz page.
    """
    connection = sqlite3.connect("database/countries.db")
    first_country, second_country, third_country, correct_country = get_random_quiz_data(
        connection, 'area')
    session['first_option_country'] = first_country.area
    session['second_option_country'] = second_country.area
    session['third_option_country'] = third_country.area
    session['correct_country'] = correct_country.area
    return render_template('quiz_area.html',
                           first_option=first_country,
                           second_option=second_country,
                           third_option=third_country,
                           correct_country=correct_country)


@app.route('/quiz/area', methods=['POST'])
def process_area_quiz_submission():
    """
    Process the user's submission for the area quiz.

    Returns:
        A redirect response to either the currency quiz or the quiz score page.
    """
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    if user_input in str(correct_country_from_session):
        session['score'] += 50
        return redirect('/quiz/currency')
    return redirect('/quiz/score')


@app.route('/quiz/currency', methods=['GET'])
def render_currency_quiz_page():
    """
    Renders the currency quiz page.

    Returns:
        The rendered template for the currency quiz page.
    """
    connection = sqlite3.connect("database/countries.db")
    first_country, second_country, third_country, correct_country = get_random_quiz_data(
        connection, 'currency')
    session['first_option_country'] = first_country.currency
    session['second_option_country'] = second_country.currency
    session['third_option_country'] = third_country.currency
    session['correct_country'] = correct_country.currency
    if correct_country.currency == "":
        session['status'] = 'level_up'
        return redirect('/quiz/capital')
    return render_template('quiz_currency.html',
                           first_option=first_country,
                           second_option=second_country,
                           third_option=third_country,
                           correct_country=correct_country)


@app.route('/quiz/currency', methods=['POST'])
def process_currency_quiz_submission():
    """
    Process the user's currency quiz submission.

    Returns:
        A redirect response to either the quiz capital page or the quiz score page.
    """
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    if user_input in correct_country_from_session:
        session['score'] += 50
        session['status'] = 'level_up'
        return redirect('/quiz/capital')
    return redirect('/quiz/score')


@app.route('/quiz/score', methods=['GET', 'POST'])
def quiz_score():
    """
    Renders the score page and resets the user's status to 'beginner'.

    Returns:
        The rendered 'score.html' template.
    """
    session['status'] = 'beginner'
    return render_template('score.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Renders the landing page of the application and handles user registration.

    Returns:
        The rendered template for the landing page.
    """
    user_connection = sqlite3.connect("database/user.db")
    create_tables_for_user_db(user_connection)
    session.clear()
    if request.method == 'POST':
        username = request.form['name']
        if not re.match(r'^[a-zA-Z0-9]{4,12}$', username):
            return render_template(
                'index.html',
                message=(
                    "Invalid username! Username must be 4-12 characters long and "
                    "can only contain letters and numbers."
                )
            )
        if check_username_exists(user_connection, username):
            return render_template(
                'index.html', message="User already exists!")
        session['username'] = username
        session['score'] = 0
        session['status'] = 'beginner'
        return redirect('/quiz/capital')
    return render_template('index.html')


@app.route('/quiz/highscore', methods=['GET', 'POST'])
def highscore():
    """
    Retrieves the highscore data from the database and renders the highscore.html template.

    Returns:
        The rendered highscore.html template.
    """
    user_connection = sqlite3.connect("database/user.db")
    set_user_score(user_connection, session['username'], session['score'])
    top_ten = get_top_ten_score(user_connection)
    user_rank = get_rank_for_username(user_connection, session['username'])
    user_rank_text = 0
    if user_rank > 10:
        user_rank_text = user_rank
    return render_template(
        'highscore.html',
        top_ten=top_ten,
        user_rank_text=user_rank_text,
        enumerate=enumerate)


@app.route('/quiz/diagrams', methods=['GET'])
def diagrams():
    """
    This function connects to the 'countries.db' database, plots the top five largest
    countries and the top five population countries, and returns the 'diagrams.html' template.
    """
    connection = sqlite3.connect("database/countries.db")
    plot_top_five_largest_countries(connection)
    plot_top_five_population_countries(connection)
    return render_template('diagrams.html')


@app.route('/quiz/stats', methods=['GET'])
def stats():
    """
    Retrieves continent area and population data from the database and renders the 'stats.html' template.

    Returns:
        The rendered template with the retrieved data passed to the context.
    """
    connection = sqlite3.connect("database/countries.db")
    corr_coeff = get_correlation_coefficient(connection)
    hypothesis = hypothesis_test(connection)
    return render_template('stats.html', corr_coeff=corr_coeff.correlation, hypothesis_test=hypothesis, p_value=corr_coeff.pvalue)


if __name__ == '__main__':
    COUNTRY_DB_PATH = "database/countries.db"
    THIRTY_DAYS = 30 * 24 * 60 * 60

    if not os.path.exists(COUNTRY_DB_PATH) or \
            (time.time() - os.path.getmtime(COUNTRY_DB_PATH)) > THIRTY_DAYS:
        country_connection = sqlite3.connect(COUNTRY_DB_PATH)
        create_tables_for_country_db(country_connection)
        fetch_and_insert_data(country_connection)
        print("Data fetched and inserted into the database.")
    app.run(debug=True,host='0.0.0.0', port=80,)
    