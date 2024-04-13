import sqlite3

def execute_query(database_file, query):
    """
    Executes a single SQL query on the specified database file.

    Args:
        database_file (str): Path to the SQLite database file.
        query (str): SQL query to execute.

    Returns:
        None
    """
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    try:
        # Execute the SQL query
        c.execute(query)

        # Commit changes to the database
        conn.commit()
        print("Query executed successfully!")

    except sqlite3.Error as e:
        print("Error executing query:", e)

    finally:
        # Close connection
        conn.close()

# Example usage
database_file = "database/countries.db"

# SQL queries for creating other tables
queries = [
    """
    CREATE TABLE IF NOT EXISTS Countries (
        id_country INTEGER PRIMARY KEY,
        official_name TEXT UNIQUE,
        code TEXT,
        area REAL,
        population INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Capitals (
        id_capital INTEGER PRIMARY KEY,
        capital TEXT UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Continents (
        id_continent INTEGER PRIMARY KEY AUTOINCREMENT,
        continent TEXT UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Borders (
        id_boarder INTEGER PRIMARY KEY AUTOINCREMENT,
        country_code_short TEXT UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Currencies (
        id_currency INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        symbol TEXT UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Languages (
        id_language INTEGER PRIMARY KEY AUTOINCREMENT,
        language TEXT UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Countries_Capitals (
        id_capital INTEGER,
        id_country INTEGER,
        UNIQUE(id_capital, id_country) ON CONFLICT REPLACE,
        FOREIGN KEY (id_capital) REFERENCES Capitals(id_capital),
        FOREIGN KEY (id_country) REFERENCES Countries(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Countries_Currencies (
        id_currency INTEGER,
        id_country INTEGER,
        FOREIGN KEY (id_currency) REFERENCES Currencies(id_currency),
        FOREIGN KEY (id_country) REFERENCES Countries(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Countries_Languages (
        id_language INTEGER,
        id_country INTEGER,
        UNIQUE(id_language, id_country) ON CONFLICT REPLACE,
        FOREIGN KEY (id_language) REFERENCES Languages(id_language),
        FOREIGN KEY (id_country) REFERENCES Countries(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Countries_Continents (
        id_continent INTEGER,
        id_country INTEGER,
        FOREIGN KEY (id_continent) REFERENCES Continents(id_continent),
        FOREIGN KEY (id_country) REFERENCES Countries(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Countries_Borders (
        id_boarder INTEGER,
        id_country INTEGER,
        FOREIGN KEY (id_boarder) REFERENCES Borders(id_boarder),
        FOREIGN KEY (id_country) REFERENCES Countries(id)
    )
    """
]

# Execute each SQL query
for query in queries:
    execute_query(database_file, query)
