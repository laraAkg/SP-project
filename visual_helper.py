from database_operations.countries_database_operations import (
    get_top_five_largest_countries, get_top_five_population_countries, get_continent_area_and_population_by_id)
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Connect to the database


def plot_top_five_largest_countries(country_connection):
    # Get top 5 largest countries from the database
    top_area = get_top_five_largest_countries(country_connection)

    # Extract country names and areas
    countries, areas = zip(*top_area)

    # Create a DataFrame
    df = pd.DataFrame({'Country': countries, 'Area': areas})

    # Create a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(df['Area'], labels=df['Country'], autopct='%1.1f%%')
    plt.title('Top 5 Largest Countries by Area')
    # Save the diagram as an image
    plt.savefig('static/diagrams/topfiveareacountry.png')
    plt.show()


def plot_top_five_population_countries(country_connection):
    # Get top 5 largest countries from the database
    top_population = get_top_five_population_countries(country_connection)

    # Extract country names and areas
    countries, populations = zip(*top_population)

    # Create a DataFrame
    df = pd.DataFrame({'Country': countries, 'Population': populations})

    # Create a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(df['Population'], labels=df['Country'], autopct='%1.1f%%')
    plt.title('Top 5 Largest Countries by Population')
    # Save the diagram as an image
    plt.savefig('static/diagrams/topfivepopulationcountry.png')
    plt.show()


def hypothesis_test():
    connection = sqlite3.connect("database/countries.db")
    data = get_continent_area_and_population_by_id(connection)

    # Define the null hypothesis
    H0 = "The average densitiy(population vs area) is 150."

    # Define the alternative hypothesis
    H1 = "The average densitiy(population vs area) is more than 150"

    # Calculate the test statistic
    t_stat, p_value = stats.ttest_1samp(data, 150)

    # Print the results
    print("Test statistic:", t_stat)
    print("p-value:", p_value)

    # Conclusion
    if p_value < 0.05:
        print("Reject the null hypothesis.")
    else:
        print("Fail to reject the null hypothesis.")
