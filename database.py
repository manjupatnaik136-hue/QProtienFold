import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('quantum_research.db')
    c = conn.cursor()
    # Table structure: Seq, Fold Type, Energy, and Timestamp
    c.execute('''CREATE TABLE IF NOT EXISTS simulation_logs 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  sequence TEXT, 
                  fold_type TEXT, 
                  energy REAL, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_simulation(sequence, fold_type, energy):
    conn = sqlite3.connect('quantum_research.db')
    c = conn.cursor()
    c.execute("INSERT INTO simulation_logs (sequence, fold_type, energy) VALUES (?, ?, ?)",
              (sequence, fold_type, energy))
    conn.commit()
    conn.close()

def get_all_logs():
    conn = sqlite3.connect('quantum_research.db')
    df = pd.read_sql_query("SELECT * FROM simulation_logs ORDER BY timestamp DESC", conn)
    conn.close()
    return df