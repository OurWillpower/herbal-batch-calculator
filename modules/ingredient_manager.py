import sqlite3


def add_ingredient(sanskrit_name, botanical_name, plant_part, form, price_per_kg):

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ingredients
        (sanskrit_name, botanical_name, plant_part, form, price_per_kg)
        VALUES (?, ?, ?, ?, ?)
        """,
        (sanskrit_name, botanical_name, plant_part, form, price_per_kg)
    )

    conn.commit()
    conn.close()


def get_all_ingredients():

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ingredients")
    rows = cursor.fetchall()

    conn.close()

    return rows


def search_ingredients(keyword):

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM ingredients
        WHERE sanskrit_name LIKE ?
        OR botanical_name LIKE ?
        """,
        ('%' + keyword + '%', '%' + keyword + '%')
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
    def get_ingredient_names():

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sanskrit_name || ' - ' || botanical_name FROM ingredients
    """)

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]
