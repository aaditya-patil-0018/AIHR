import sqlite3
import json
import os

class HR:
    def __init__(self):
        self.db = "users.db"
        self.conn = sqlite3.connect(self.db, timeout=10)
        self.conn.execute('PRAGMA journal_mode=WAL')
        self.table_name = "hr_details"
        self.create_table()
        self.openings_file = "openings_data.json"
        self.create_openings_file()

    # Create hr_details table
    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS hr_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL
                )
            ''')

    # Ensure the openings_data.json file exists
    def create_openings_file(self):
        if not os.path.exists(self.openings_file):
            with open(self.openings_file, 'w') as f:
                json.dump({}, f, indent=4)

    # Load the job openings data from the JSON file
    def load_openings_data(self):
        with open(self.openings_file, 'r') as f:
            return json.load(f)

    # Save the updated openings data back to the JSON file
    def save_openings_data(self, data):
        with open(self.openings_file, 'w') as f:
            json.dump(data, f, indent=4)

    # Create a new job opening
    def create_opening(self, company_name, job_data):
        data = self.load_openings_data()

        if company_name not in data:
            data[company_name] = []

        data[company_name].append(job_data)

        self.save_openings_data(data)
        print(f"Job opening created for {company_name}.")

    # Edit an existing job opening
    def edit_job(self, company_name, job_index, updated_data):
        data = self.load_openings_data()

        if company_name in data and 0 <= job_index < len(data[company_name]):
            data[company_name][job_index].update(updated_data)
            self.save_openings_data(data)
            print(f"Job opening at {company_name} updated.")
        else:
            print("Job opening not found.")

    # Delete a job opening
    def delete_opening(self, company_name, job_index):
        data = self.load_openings_data()

        if company_name in data and 0 <= job_index < len(data[company_name]):
            deleted_job = data[company_name].pop(job_index)
            self.save_openings_data(data)
            print(f"Job opening at {company_name} deleted: {deleted_job}")
        else:
            print("Job opening not found.")

    # Get all job openings for a company
    def get_openings(self, company_name):
        data = self.load_openings_data()
        return data.get(company_name, [])

    # Check if an HR with the given email is already registered
    def already_registered(self, email):
        cursor = self.conn.execute('''
            SELECT email FROM hr_details WHERE email = ?
        ''', (email,))
        return cursor.fetchone() is not None

    # Register new HR details if not already registered
    def register(self, data):
        if not self.already_registered(data["email"]):
            with self.conn:
                self.conn.execute('''
                    INSERT INTO hr_details (email, name, company, role, phone, city, state)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (data["email"], data["name"], data["company"], data["role"], data["phone"], data["city"], data["state"]))
            print("HR registration successful!")
            return True
        else:
            print("HR already registered.")
            return False

    # Get HR information by email
    def get(self, email):
        cursor = self.conn.execute('''
            SELECT * FROM hr_details WHERE email = ?
        ''', (email,))
        return cursor.fetchone()

    # Delete HR details by email
    def delete(self, email):
        with self.conn:
            self.conn.execute('''
                DELETE FROM hr_details WHERE email = ?
            ''', (email,))
        print(f"HR {email} deleted.")

    # Close the database connection
    def close(self):
        self.conn.close()


# Example usage
if __name__ == "__main__":
    pass
    '''
    # HR manager usage
    hr_manager = HR()
    
    # Register a new HR
    hr_data = {
        "email": "newhr@example.com",
        "name": "abcd",
        "company": "new test company",
        "role": "HR Manager",
        "phone": "0987654321",
        "city": "Nashik",
        "state": "MH"
    }

    if hr_manager.register(hr_data):
        print("HR registration successful!")

    # Get HR details
    hr_details = hr_manager.get("hr@example.com")
    if hr_details:
        print("HR Details:", hr_details)
    else:
        print("HR not found.")

    # Create a new job opening
    job_data = {
        "type": "Full-time",
        "description": "HR Manager to oversee recruitment processes.",
        "user_role": "HR Manager",
        "status": "Open",
        "users_enrolled": []
    }
    hr_manager.create_opening("TechCorp", job_data)

    # Edit an existing job opening
    updated_job_data = {
        "status": "Closed",
        "description": "Role filled. No longer accepting applicants."
    }
    hr_manager.edit_job("TechCorp", 0, updated_job_data)

    # Get and display all openings for a company
    openings = hr_manager.get_openings("TechCorp")
    print("Current Openings for TechCorp:", openings)

    # Delete a job opening
    hr_manager.delete_opening("TechCorp", 0)

    # Close the HR manager (if necessary)
    hr_manager.close()
    '''