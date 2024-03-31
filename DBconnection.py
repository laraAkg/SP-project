import sqlite3

DATABASE_NAME = 'example.db'


def create_database():
    """
    Creates a new SQLite database if it doesn't exist and creates a 'user' table in it.
    """
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS user
                         (name TEXT, email TEXT)''')
    except sqlite3.Error as e:
        print("SQLite Error:", e)

def insert_user(name, email):
    """
    Inserts a new user into the 'user' table of the SQLite database.

    Args:
        name (str): The name of the user.
        email (str): The email address of the user.
    """
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM user WHERE email=?", (email,))
            existing_user = c.fetchone()
            if existing_user:
                print(f"Email address '{email}' already exists.")
            else:
                c.execute("INSERT INTO user (name, email) VALUES (?, ?)", (name, email))
                print(f"User '{name}' with email address '{email}' has been added.")
    except sqlite3.Error as e:
        print("SQLite Error:", e)

def print_users():
    """
    Prints all the users in the 'user' table of the SQLite database.
    """
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM user")
            users = c.fetchall()

            for user in users:
                print("Name:", user[0])
                print("Email:", user[1])
                print()
    except sqlite3.Error as e:
        print("SQLite Error:", e)

if __name__ == "__main__":
    create_database()
    insert_user("John Doe", "john@example.com")
    insert_user("Jane Smith", "jane@example.com")
    print_users()
