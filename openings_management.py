import json
import os

class Openings:

    def __init__(self):
        self.file = "openings_data.json"

    def create(self):
        if not os.path.exists(self.file):
            with open(self.file, 'w') as f:
                json.dump({}, f, indent=4)
        return True
    
    def get_all(self):
        with open(self.file, 'r') as f:
            data = json.load(f)
        return data

    def get_all_opening(self, company):
        with open(self.file, 'r') as f:
            data = json.load(f)
        if company not in data:
            data[company] = {}
        return data[company]

    def get_opening(self, company, opening_id):
        with open(self.file, 'r') as f:
            data = json.load(f)
        return data[company][opening_id]
    
    def create_opening(self, company, d):
        with open(self.file, 'r') as f:
            data = json.load(f)
        with open(self.file, 'w') as f:
            if company not in data:
                data[company] = {}
            data[company][len(data[company])+1] = d
            json.dump(data, f, indent=4)
        return True
        
    def close(self, company, opening_id):
        with open(self.file, 'r') as f:
            data = json.load(f)[company]
            data[opening_id] = "Closed"
        with open(self.file, 'w') as f:
            json.dump(data, f, indent=4)

    def pause(self, company, opening_id):
        with open(self.file, 'r') as f:
            data = json.load(f)[company]
            data[opening_id] = "Pause"
        with open(self.file, 'w') as f:
            json.dump(data, f, indent=4)