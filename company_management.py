import json

class Company:
    def __init__(self):
        self.db = "companies.json"
        self.data = self.load_data()

    # Load data from the JSON file
    def load_data(self):
        try:
            with open(self.db, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}  # Return an empty dictionary if the file doesn't exist

    # Save data to the JSON file
    def save_data(self):
        with open(self.db, 'w') as file:
            json.dump(self.data, file, indent=4)

    # Add a new company to the JSON file
    def add(self, name, type, website, description, size, city, state):
        self.data[name] = {
            "type": type,
            "website": website,
            "company_description": description,
            "company_size": size,
            "city": city,
            "state": state
        }
        self.save_data()
        print(f"Company '{name}' added successfully.")

    # Retrieve company information by a hint (e.g., name or partial name)
    def get_company(self, hint):
        results = {name: info for name, info in self.data.items() if hint.lower() in name.lower()}
        if results:
            return results
        else:
            print("No matching company found.")
            return None

# Example usage
if __name__ == "__main__":
    company_manager = Company()

    # Add a new company
    company_manager.add(
        name="new test company",
        type="Technology",
        website="https://www.techcorp.com",
        description="Innovative tech solutions provider",
        size="20",
        city="nashik",
        state="mh"
    )

    # Search for a company by a partial name
    result = company_manager.get_company("Tech")
    if result:
        print("Company found:", result)