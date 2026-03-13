import sqlite3
import csv
import os


def create_ingredient_table():

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sanskrit_name TEXT,
            botanical_name TEXT UNIQUE,
            common_name TEXT,
            plant_part TEXT,
            form TEXT,
            category TEXT,
            price_per_kg REAL
        )
    """)

    conn.commit()
    conn.close()


def create_formulation_table():

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS formulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            ingredient_name TEXT,
            percentage REAL
        )
    """)

    conn.commit()
    conn.close()


def load_ingredients_from_csv():

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM ingredients")
    count = cursor.fetchone()[0]

    if count == 0:

        file_path = os.path.join(os.getcwd(), "ingredients_master.csv")

        if not os.path.exists(file_path):
            print("CSV file not found:", file_path)
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    cursor.execute("""
                        INSERT INTO ingredients
                        (sanskrit_name, botanical_name, common_name, plant_part, form, category, price_per_kg)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row["sanskrit_name"],
                        row["botanical_name"],
                        row["common_name"],
                        row["plant_part"],
                        row["form"],
                        row["category"],
                        float(row["price_per_kg"])
                    ))
                except sqlite3.IntegrityError:
                    # Skip duplicates
                    pass

        conn.commit()

    conn.close()
