import sqlite3
import csv


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
        )
    """)

    conn.commit()
    conn.close()


def load_ingredients_from_csv():

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    # check if database already has data
    cursor.execute("SELECT COUNT(*) FROM ingredients")
    count = cursor.fetchone()[0]

    if count == 0:

        with open("ingredients_master.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                cursor.execute("""
                    INSERT INTO ingredients
                    (sanskrit_name, botanical_name, plant_part, form, price_per_kg)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    row["sanskrit_name"],
                    row["botanical_name"],
                    row["plant_part"],
                    row["form"],
                    row["price_per_kg"]
                ))

        conn.commit()

    conn.close()
