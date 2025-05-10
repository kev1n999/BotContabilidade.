from sqlite3 import * 

class Database:
    def __init__(self, name):
        self.name = name 
        self.db = connect(f"../src/database/db/{self.name}.db")
        self.cursor = self.db.cursor()