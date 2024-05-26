"""
Represents a country with its attributes such as official name, capital, continent, borders,
population, area, languages, and currency.
"""

class Country:

    def __init__(self, official_name, capital, continent, borders, population, area,
                 languages, currency):
        self.official_name = official_name
        self.capital = capital
        self.continent = continent
        self.borders = borders
        self.population = population
        self.area = area
        self.languages = languages
        self.currency = currency
