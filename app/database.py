import sqlite3

def get_connection():
    return sqlite3.connect('db/TaskManagerDB')

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TASK (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DS_TASK TEXT NOT NULL,
        DT_INCL TIMESTAMP NOT NULL,
        DT_VENCIMENTO DATE,
        STATUS TEXT NOT NULL DEFAULT 'IN',
        CATEGORIA TEXT,
        DT_EXCLUSAO TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()
