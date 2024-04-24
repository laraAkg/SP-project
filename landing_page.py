"""
This file contains the code for the landing page of a Flask application that allows
users to take a quiz about countries and their capitals.
The landing page provides links to different quiz categories such as capital,
continent, population, area, and currency.
Each category has its own route and corresponding functions to render the quiz page
and process the user's submission.

The Flask application is created with the name 'app' and a secret key is set for session management.

The routes and functions in this file include:
- '/quiz/capital': Renders the capital quiz page and processes the user's submission.
- '/quiz/continent': Renders the continent quiz page and processes the user's submission.
- '/quiz/population': Renders the population quiz page and processes the user's submission.
- '/quiz/area': Renders the area quiz page and processes the user's submission.
- '/quiz/currency': Renders the currency quiz page.
- '/quiz/score': Renders the score page.
- '/': Renders the home page where users can input their name and start the quiz.
"""
import sqlite3
import re
import os
import time
from flask import Flask, request, render_template, redirect, session
from database_operations.user_database_operations import (insert_user, check_username_exists,
                                                          create_tables_for_user_db,
                                                          set_user_score)
from database_operations.countries_database_setup import (create_tables_for_country_db,
                                                          fetch_and_insert_data)
from help_services import get_random_quiz_data, return_options_for_continents

app = Flask(__name__, static_folder='static')
app.secret_key = 'BAD_SECRET_KEY'


@app.route('/quiz/capital', methods=['GET'])
def render_capital_quiz_page():
    """
    Renders the capital quiz page.

    This function connects to the 'countries.db' SQLite database and retrieves random quiz data
    for the capital quiz. It stores the options and correct answer in the session object and
    renders the 'quiz_capital.html' template with the retrieved data.

    Returns:
        The rendered template for the capital quiz page.
    """
    if session['status'] != 'level_up':
        session['score'] = 0
        session['status'] = 'beginner'
    country_connection = sqlite3.connect("database/countries.db")
    first_option, second_option, third_option, correct_option = get_random_quiz_data(
        country_connection, 'capital')
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
    Process the submission of a capital quiz answer.

    This function retrieves the user's input from the form, compares it with the correct
    country stored in the session, and redirects the user to the appropriate page based
    on the correctness of the answer.

    Returns:
        A redirect response to either '/quiz/continent' or
        '/quiz/score' based on the correctness of the answer.
    """
    user_connection = sqlite3.connect("database/user.db")
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    print(correct_country_from_session)
    print(user_input)
    if user_input in correct_country_from_session:
        session['score'] += 50
        return redirect('/quiz/continent')
    else:
        return redirect('/quiz/score')


@app.route('/quiz/continent', methods=['GET'])
def render_continent_quiz_page():
    """
    Renders the continent quiz page.

    This function connects to the 'countries.db' SQLite database and retrieves
    random quiz datafor the continent quiz.
    It stores the continent values of the options and the correct country in the session.
    Finally, it renders the 'quiz_continent.html' template with the quiz data.

    Returns:
        The rendered template for the continent quiz page.
    """
    country_connection = sqlite3.connect("database/countries.db")
    list_continents = return_options_for_continents(country_connection)
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
    Process the submission of the continent quiz.

    This function retrieves the user's input from the form, compares it with the correct country
    stored in the session, and redirects the user to the appropriate page based on the correctness
    of their answer.

    Returns:
        A redirect response to either '/quiz/population' or '/quiz/score' based on the correctness
        of the user's answer.
    """
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    print(correct_country_from_session)
    print(user_input)
    if user_input in correct_country_from_session:
        session['score'] += 50
        return redirect('/quiz/population')
    else:
        return redirect('/quiz/score')


@app.route('/quiz/population', methods=['GET'])
def render_population_quiz_page():
    """
    Renders the population quiz page.

    This function connects to the 'countries.db' database and retrieves 
    random quiz data for the population quiz.
    It stores the population values of the options and the correct country in the session.
    Finally, it renders the 'quiz_population.html' template with the quiz data.

    Returns:
        The rendered population quiz page as a Flask template.

    """
    country_connection = sqlite3.connect("database/countries.db")
    first_option_country, second_option_country, third_option_country, correct_country = get_random_quiz_data(
        country_connection, 'population')
    session['first_option_country'] = first_option_country.population
    session['second_option_country'] = second_option_country.population
    session['third_option_country'] = third_option_country.population
    session['correct_country'] = correct_country.population
    return render_template('quiz_population.html',
                           first_option=first_option_country,
                           second_option=second_option_country,
                           third_option=third_option_country,
                           correct_country=correct_country)


@app.route('/quiz/population', methods=['POST'])
def process_population_quiz_submission():
    """
    Process the user's population quiz submission.

    This function retrieves the user's input from the form, compares it with the correct
    country stored in the session,
    and redirects the user to the appropriate page based on their answer.

    Returns:
        A redirect response to either '/quiz/area' or '/quiz/score' based on the user's answer.
    """
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    if int(user_input) == correct_country_from_session:
        session['score'] += 50
        return redirect('/quiz/area')
    else:
        return redirect('/quiz/score')


@app.route('/quiz/area', methods=['GET'])
def render_area_quiz_page():
    """
    Renders the area quiz page.

    This function connects to the 'countries.db' SQLite database and retrieves random quiz data for
    the 'area' category.
    It stores the area values of the quiz options and the correct country in the session object.
    Finally, it renders the 'quiz_area.html' template, passing the quiz options and correct country
    as template variables.

    Returns:
        The rendered HTML template for the area quiz page.
    """
    country_connection = sqlite3.connect("database/countries.db")

    first_option_country, second_option_country, third_option_country, correct_country = get_random_quiz_data(
        country_connection, 'area')
    session['first_option_country'] = first_option_country.area
    session['second_option_country'] = second_option_country.area
    session['third_option_country'] = third_option_country.area
    session['correct_country'] = correct_country.area
    return render_template('quiz_area.html',
                           first_option=first_option_country,
                           second_option=second_option_country,
                           third_option=third_option_country,
                           correct_country=correct_country)


@app.route('/quiz/area', methods=['POST'])
def process_area_quiz_submission():
    """
    Process the submission of the area quiz.

    This function retrieves the user's input from the form, compares it with the correct country
    stored in the session, and redirects the user to the appropriate page based on the 
    correctness of their answer.

    Returns:
        A redirect response to either '/quiz/population' or '/quiz/score' based on the correctness
        of the user's answer.
    """
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    if user_input in str(correct_country_from_session):
        session['score'] += 50
        return redirect('/quiz/currency')
    else:
        return redirect('/quiz/score')


@app.route('/quiz/currency', methods=['GET'])
def render_currency_quiz_page():
    """
    Renders the currency quiz page.

    This function connects to the 'countries.db' SQLite database and retrieves random quiz data for
    the currency quiz.
    It stores the currency values of the options and the correct country in the session.
    Finally, it renders the 'quiz_currency.html' template with the quiz data.

    Returns:
        The rendered template for the currency quiz page.
    """
    country_connection = sqlite3.connect("database/countries.db")

    first_option_country, second_option_country, third_option_country, correct_country = get_random_quiz_data(
        country_connection, 'currency')
    session['first_option_country'] = first_option_country.currency
    session['second_option_country'] = second_option_country.currency
    session['third_option_country'] = third_option_country.currency
    session['correct_country'] = correct_country.currency
    # If the correct country's currency is empty, redirect to the next quiz
    if correct_country.currency == "":
        session['status'] = 'level_up'
        redirect('/quiz/capital')
    else:
        return render_template('quiz_currency.html',
                               first_option=first_option_country,
                               second_option=second_option_country,
                               third_option=third_option_country,
                               correct_country=correct_country)


@app.route('/quiz/currency', methods=['POST'])
def process_currency_quiz_submission():
    """
    Process the submission of the area quiz.

    This function retrieves the user's input from the form, compares it with the correct
    country stored in the session, and redirects the user to the appropriate page based on
    the correctness of their answer.

    Returns:
        A redirect response to either '/quiz/population' or '/quiz/score'
        based on the correctness of the user's answer.
    """
    user_input = request.form['option']
    correct_country_from_session = session['correct_country']
    if user_input in correct_country_from_session:
        session['score'] += 50
        session['status'] = 'level_up'
        return redirect('/quiz/capital')
    else:
        return redirect('/quiz/score')


@app.route('/quiz/score', methods=['GET', 'POST'])
def quiz_score():
    """
    Render the score page.
    """
    score = session['score']
    username = session['username']
    session['status'] = 'beginner'
    print(score)
    print(username)
    return render_template('score.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Render the home page where users can input their name.
    Save user's name to the database and redirect to the quiz page upon submission.
    """

    user_connection = sqlite3.connect("database/user.db")
    create_tables_for_user_db(user_connection)
    session.clear()
    if request.method == 'POST':
        username = request.form['name']
        if not re.match(r'^[a-zA-Z0-9]{4,12}$', username):
            return render_template('index.html', message="Invalid username! Username must be 4-12 characters long and can only contain letters and numbers.")
        if check_username_exists(user_connection, username):
            return render_template('index.html', message="User already exists!")
        else:
            insert_user(user_connection, username)
            session['username'] = username
            session['score'] = 0
            session['status'] = 'beginner'
            return redirect('/quiz/capital')
    return render_template('index.html')


@app.route('/quiz/highscore', methods=['GET'])
def highscore():
    """
    Render the highscore page.
    """
    # TODO: call methode to get highscore from database (first implement the method in user_database_operations.py)
    # a simple select by username -> username you can get in the session
    # maybe an idea would be to display the first 10 highscores (user order by in sql query in database)
    # and if the user score is not in top 10 then show below in which place he is (e.g. 15th)
    # maybe show the user in which percentile he is with his score -> is this using p value? idk
    return render_template('highscore.html')


# create new methode that show 2-3 diagramms regarding for example biggest 10 countries etc in pychart or other chart
# for this create new function in database with order by 
# use her please pandas and dataframe to create the diagramms! Very important
# maybe island vs countries in pie chart
# decide what makes sense to display in the diagramms
# use one of the data to calculate stuff with the p value for this you can maybe experiment with the data population and area
# for this you are free to create a function in the help_services.py file
# is gini even a thing in this context? maybe you can use it to calculate the p value? if not then ignore this point


if __name__ == '__main__':
    COUNTRY_DB_PATH = "database/countries.db"
    THIRTY_DAYS = 30 * 24 * 60 * 60

    # Check if the country database exists and is up-to-date (30 days)
    if not os.path.exists(COUNTRY_DB_PATH) or \
            (time.time() - os.path.getmtime(COUNTRY_DB_PATH)) > THIRTY_DAYS:
        country_connection = sqlite3.connect(COUNTRY_DB_PATH)
        create_tables_for_country_db(country_connection)
        fetch_and_insert_data(country_connection)
        print("Data fetched and inserted into the database.")
    app.run(debug=True)
