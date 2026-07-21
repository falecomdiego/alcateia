import os
import sqlite3
from typing import Optional

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
DB_PATH = os.path.join(DB_DIR, "alcateia_mvp.db")

def get_db_connection() -> sqlite3.Connection:
    """Retorna uma conexão aberta com o banco de dados local SQLite."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Inicializa o esquema relacional do banco de dados MVP, se não existir."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela: Demandas de Investigação (Discovery Service)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS demandas_investigacao (
        demanda_id TEXT PRIMARY KEY,
        contexto TEXT NOT NULL,
        pergunta TEXT NOT NULL,
        data_hora TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    # Tabela: Diário de Fontes (Evidence Service)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diario_fontes (
        fonte_id TEXT PRIMARY KEY,
        arquivo_bruto TEXT NOT NULL,
        hash_sha256 TEXT NOT NULL,
        total_linhas INTEGER NOT NULL,
        status TEXT NOT NULL
    )
    """)

    # Tabela: Cadeias de Evidência / MUE (Audit & Monitoring Services)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cadeias_evidencia (
        chain_id TEXT PRIMARY KEY,
        demanda_id TEXT NOT NULL,
        fonte_id TEXT NOT NULL,
        registro_id TEXT NOT NULL,
        texto_evidencia TEXT NOT NULL,
        categoria_taxonomica TEXT NOT NULL,
        grau_incerteza TEXT NOT NULL,
        hash_origem TEXT NOT NULL,
        aprovador_humano TEXT NOT NULL,
        data_auditoria TEXT NOT NULL,
        FOREIGN KEY (demanda_id) REFERENCES demandas_investigacao (demanda_id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Banco de dados inicializado com sucesso em:", DB_PATH)
