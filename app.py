import streamlit as st
import pandas as pd
import sqlite3
import csv

from modules.database import (
    create_ingredient_table,
    create_formulation_table
)

st.title("Herbal Formulation System")

create_ingredient_table()
create_formulation_table()

# -----------------------------
# LOAD MASTER INGREDIENT FILE
# -----------------------------

st.header("Load Ingredient Master Database")

if st.button("Load Ingredients from CSV"):

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    with open("ingredients_master.csv", newline='', encoding='utf-8') as csvfile:

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

    st.success("Ingredients imported successfully")


# -----------------------------
# ADD INGREDIENT
# -----------------------------

st.header("Add New Ingredient")

sanskrit_name = st.text_input("Sanskrit Name")
botanical_name = st.text_input("Botanical Name")
common_name = st.text_input("Common Name")
plant_part = st.text_input("Plant Part")
form = st.text_input("Form (Powder / Extract / Oil etc)")
category = st.text_input("Category")
price = st.number_input("Price per kg")

if st.button("Add Ingredient"):

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ingredients
        (sanskrit_name, botanical_name, common_name, plant_part, form, category, price_per_kg)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        sanskrit_name,
        botanical_name,
        common_name,
        plant_part,
        form,
        category,
        price
    ))

    conn.commit()
    conn.close()

    st.success("Ingredient added successfully")


# -----------------------------
# SEARCH INGREDIENTS
# -----------------------------

st.header("Search Ingredients")

keyword = st.text_input("Type Sanskrit or Botanical name")

conn = sqlite3.connect("ingredients.db")

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
