from database_operations.countries_database_operations import (get_top_five_largest_countries, get_top_five_population_countries, get_countries_count_per_continent)
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
 
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
    plt.savefig('static/diagrams/topfiveareacountry.png')  # Save the diagram as an image
    plt.close()

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
    plt.savefig('static/diagrams/topfivepopulationcountry.png')  # Save the diagram as an image
    plt.close()

def plot_countries_count_per_continent(country_connection):
    print(get_countries_count_per_continent(country_connection))
