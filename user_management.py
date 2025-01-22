import sqlite3
import bcrypt

class Users:

    def __init__(self):
        self.databasename = "users.db"
        # Connect to the database with a timeout and enable WAL mode for concurrency
        self.conn = sqlite3.connect(self.databasename, timeout=10)
        self.conn.execute('PRAGMA journal_mode=WAL')
        self.user_table()

    # Create user table
    def user_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    usertype TEXT NOT NULL
                )
            ''')

    # Signup: Add user to the database
    def signup(self, email, password, usertype="applicant"):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            with self.conn:
                self.conn.execute('''
                    INSERT INTO users (email, password, usertype) VALUES (?, ?, ?)
                ''', (email, hashed_password, usertype))
            print("Signup successful!")
            return True
        except sqlite3.IntegrityError:
            print("User already exists.")
            return False

    # Login: Check user's password
    def login(self, email, password, usertype="applicant"):
        user = self.get(email)
        if user:
            # Check if the given password matches the hashed password
            if bcrypt.checkpw(password.encode('utf-8'), user[1]):
                if usertype == user[2]:
                    print("Login successful!")
                    return True
                else:
                    print("Incorrect user type.")
                    return False
            else:
                print("Incorrect password.")
                return False
        else:
            print("User not found.")
            return False

    # Delete user from the database
    def delete(self, email):
        with self.conn:
            self.conn.execute('''
                DELETE FROM users WHERE email = ?
            ''', (email,))
        print(f"User {email} deleted.")

    # Get user information from the database
    def get(self, email):
        with self.conn:
            cursor = self.conn.execute('''
                SELECT email, password, usertype FROM users WHERE email = ?
            ''', (email,))
            return cursor.fetchone()

    def get_id(self, email):
        with self.conn:
            cursor = self.conn.execute('''
                SELECT * FROM users WHERE email = ?
            ''', (email,))
            return cursor.fetchone()[0]

    # Close the database connection
    def close(self):
        self.conn.close()

# Example usage
if __name__ == "__main__":
    user_manager = Users()

    # Signup a new user
    if user_manager.signup("user@example.com", "securepassword"):
        print("Signup successful!")

    # Attempt to login
    if user_manager.login("user@example.com", "securepassword"):
        print("User logged in successfully.")

    # Attempt to login with incorrect password
    if not user_manager.login("user@example.com", "wrongpassword"):
        print("Failed to log in.")

    # Delete a user
    user_manager.delete("user@example.com")

    # Close the connection
    user_manager.close()