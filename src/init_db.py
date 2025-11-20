import sqlite3
import os

# Caminho para a pasta src (onde este ficheiro está)
BASE_DIR = os.path.dirname(__file__)

# Caminho para o arquivo SQL
sql_path = os.path.join(BASE_DIR, "..", "database", "database.sql")

# Caminho onde o SQLite irá criar o ficheiro database.db
db_path = os.path.join(BASE_DIR, "..", "database", "database.db")

print("A importar SQL de:", sql_path)
print("A criar base de dados em:", db_path)

# Lê o conteúdo do ficheiro database.sql
with open(sql_path, "r", encoding="utf-8") as f:
    sql_script = f.read()

# Cria a base de dados e executa o script
conn = sqlite3.connect(db_path)
conn.executescript(sql_script)
conn.commit()
conn.close()

print("Base de dados criada com sucesso!")
