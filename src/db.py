import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "database.db")

def conectar():
    return sqlite3.connect(DB_PATH)