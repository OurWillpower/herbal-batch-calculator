import streamlit as st
import pandas as pd
import sqlite3
import csv
import os

st.title("Herbal Formulation System")

# database file
DB_PATH = os.path.join(os.getcwd(), "ingredients.db")

def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sanskrit_name TEXT,
            botanical_name TEXT,
            common_name TEXT,
            plant_part TEXT,
            form TEXT,
            category TEXT,
            price_per_kg REAL
        )
    """)

    conn.commit()
    conn.close()


create_tables()

# -----------------------------
# LOAD INGREDIENT MASTER FILE
# -----------------------------

st.header("Load Ingredient Master Database")

if st.button("Load Ingredients from CSV"):

    conn = get_connection()
    cursor = conn.cursor()

    file_path = os.path.join(os.getcwd(), "ingredients_master.csv")

    if not os.path.exists(file_path):

        st.error("ingredients_master.csv file not found in project folder")

    else:

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

                except:
                    pass

        conn.commit()
        conn.close()

        st.success("Ingredient database imported successfully")


# -----------------------------
# SEARCH INGREDIENTS
# -----------------------------

st.header("Search Ingredients")

keyword = st.text_input("Type Sanskrit or Botanical name")

conn = get_connection()

if keyword:

    query = f"""
    SELECT * FROM ingredients
    WHERE sanskrit_name LIKE '%{keyword}%'
    OR botanical_name LIKE '%{keyword}%'
    """

else:

    query = "SELECT * FROM ingredients"

df = pd.read_sql(query, conn)

conn.close()

st.dataframe(df)
