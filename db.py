import json

class JSONDatabase:
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)

    def insert_data(self, key, value):
        self.data[key] = value
        self.save_data()

    def get_data(self, key):
        return self.data.get(key, None)

    def update_data(self, key, new_value):
        if key in self.data:
            self.data[key] = new_value
            self.save_data()
        else:
            print(f"Key '{key}' not found in the database.")

    def delete_data(self, key):
        if key in self.data:
            del self.data[key]
            self.save_data()
        else:
            print(f"Key '{key}' not found in the database.")
