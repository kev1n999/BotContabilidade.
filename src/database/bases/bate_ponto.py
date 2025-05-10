from database.database import Database

class BatePontoDatabase(Database):
    def __init__(self):
        super().__init__("BatePonto")
        
    def table_ponto(self):
        self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS ponto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        inicio TEXT NOT NULL,
        termino TEXT,
        tempo_trabalhado TEXT
    )
    """)
    
    def table_pausas(self):
        self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS pausas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        ponto_id INTEGER NOT NULL,
        pausa TEXT NOT NULL,
        retorno TEXT,
        FOREIGN KEY (ponto_id) REFERENCES ponto (id)
    )
    """)
        
    def table_recommendations(self):
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS recomendacoes (
        user_id INTEGER PRIMARY KEY,
        sim INTEGER DEFAULT 0,
        nao INTEGER DEFAULT 0
    )
    ''')