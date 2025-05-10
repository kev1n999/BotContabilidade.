from database.database import Database

class StaffsDatabase(Database):
    def __init__(self):
        super().__init__("Staffs")
        
    def table_staff(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Staffs (ticket_channel_id INTEGER, staff_id INTEGER)")
    
    def table_avaliacoes(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Avaliacoes (staff_id INTEGER, client_id INTEGER, nota TEXT, recomenda TEXT)")
    
    def table_recomendacoes(self):
       self. cursor.execute('''
    CREATE TABLE IF NOT EXISTS recomendacoes (
        user_id INTEGER PRIMARY KEY,
        sim INTEGER DEFAULT 0,
        nao INTEGER DEFAULT 0
    )
    ''')