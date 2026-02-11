import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def get_connection():
    """
    Crea e restituisce una connessione a MySQL usando i parametri in config.py.
    """
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print("❌ Errore connessione MySQL:", e)
        return None


def add_categoria(nome):
    """
    Inserisce una nuova categoria in tabella 'categorie'.
    Ritorna True se inserita, False se errore (es. duplicato UNIQUE).
    """
    conn = get_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categorie (nome) VALUES (%s)", (nome,))
        conn.commit()
        return True
    except Error as e:
        #print("❌ Errore add_categoria:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def get_categoria_id(nome_categoria):
    """Ritorna l'id della categoria se esiste, altrimenti None."""
    conn = get_connection()
    if not conn:
        return None

    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute(
            "SELECT id FROM categorie WHERE nome = %s",
            (nome_categoria,)
        )
        row = cursor.fetchone()
        return row[0] if row else None
    except Error as e:
        print("❌ Errore get_categoria_id:", e)
        return None
    finally:
        cursor.close()
        conn.close()


def add_spesa(data_spesa, importo, nome_categoria, descrizione=None):
    categoria_id = get_categoria_id(nome_categoria)
    if categoria_id is None:
        return False

    conn = get_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO spese (data, importo, categoria_id, descrizione)
            VALUES (%s, %s, %s, %s)
            """,
            (data_spesa, importo, categoria_id, descrizione)
        )
        conn.commit()
        return True
    except Error as e:
        print("❌ Errore add_spesa:", e)
        return False
    finally:
        cursor.close()
        conn.close()
from mysql.connector import Error
import mysql.connector


def get_categoria_id(nome_categoria: str):
    """Ritorna l'id della categoria se esiste, altrimenti None."""
    conn = get_connection()
    if not conn:
        return None

    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("SELECT id FROM categorie WHERE nome = %s", (nome_categoria,))
        row = cursor.fetchone()
        return row[0] if row else None
    except Error as e:
        print("❌ Errore get_categoria_id:", e)
        return None
    finally:
        cursor.close()
        conn.close()


def add_spesa(data_spesa: str, importo: float, nome_categoria: str, descrizione: str | None = None) -> bool:
    """
    Inserisce una spesa in tabella 'spese'.
    - controlla che la categoria esista (via nome)
    - inserisce la spesa con FK categoria_id
    """
    categoria_id = get_categoria_id(nome_categoria)
    if categoria_id is None:
        return False

    conn = get_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES (%s, %s, %s, %s)",
            (data_spesa, importo, categoria_id, descrizione)
        )
        conn.commit()
        return True
    except Error as e:
        print("❌ Errore add_spesa:", e)
        return False
    finally:
        cursor.close()
        conn.close()

import re
from mysql.connector import Error


def set_budget(mese: str, nome_categoria: str, importo: float) -> bool:
    """
    Inserisce o aggiorna il budget per (mese, categoria).
    Ritorna True se ok, False se categoria non esiste o errore DB.
    """
    # Validazione mese YYYY-MM
    if not re.match(r"^\d{4}-\d{2}$", mese):
        print("❌ Formato mese non valido. Usa YYYY-MM.")
        return False

    categoria_id = get_categoria_id(nome_categoria)
    if categoria_id is None:
        print("❌ Errore: la categoria non esiste.")
        return False

    if importo <= 0:
        print("❌ Errore: il budget deve essere maggiore di zero.")
        return False

    conn = get_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO budget (mese, categoria_id, importo)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE importo = VALUES(importo)
            """,
            (mese, categoria_id, importo)
        )
        conn.commit()
        return True
    except Error as e:
        print("❌ Errore set_budget:", e)
        return False
    finally:
        cursor.close()
        conn.close()