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
