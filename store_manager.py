import json
import os

class StoreManager:
    def __init__(self, filename='stores.json'):
        self.filename = filename
        self.stores = self.load_stores()
        if not self.stores:
            self.add_default_store()

    def load_stores(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {}

    def save_stores(self):
        with open(self.filename, 'w') as f:
            json.dump(self.stores, f, indent=2)

    def add_store(self, name, details):
        self.stores[name] = details
        self.save_stores()

    def remove_store(self, name):
        if name in self.stores:
            del self.stores[name]
            self.save_stores()
            return True
        return False

    def get_store(self, name):
        return self.stores.get(name)

    def list_stores(self):
        return list(self.stores.keys())

    def add_default_store(self):
        default_store = {
            "name": "Default Store",
            "items": [
                {"name": "Item 1", "price": 10.99},
                {"name": "Item 2", "price": 15.99},
                {"name": "Item 3", "price": 5.99},
                {"name": "Item 4", "price": 20.99},
                {"name": "Item 5", "price": 8.99}
            ],
            "tax_rate": 0.08
        }
        self.add_store("default", default_store)

