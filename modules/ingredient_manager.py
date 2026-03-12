def get_all_ingredients():

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ingredients")
    rows = cursor.fetchall()

    conn.close()

    return rows
