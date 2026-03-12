import sqlite3


def create_ingredient_table():

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sanskrit_name TEXT,
            botanical_name TEXT,
            plant_part TEXT,
            form TEXT,
            price_per_kg REAL
        );
    """)

    conn.commit()
    conn.close()
