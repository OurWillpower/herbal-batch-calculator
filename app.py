import streamlit as st
import pandas as pd
import sqlite3

from modules.database import (
    create_ingredient_table,
    create_formulation_table,
    load_ingredients_from_csv
)

from modules.ingredient_manager import (
    add_ingredient,
    get_all_ingredients,
    search_ingredients,
    get_ingredient_names
)

st.title("Herbal Formulation System")

create_ingredient_table()
create_formulation_table()
load_ingredients_from_csv()


# -----------------------------
# ADD INGREDIENT
# -----------------------------

st.header("Add New Ingredient")

sanskrit_name = st.text_input("Sanskrit Name")
botanical_name = st.text_input("Botanical Name")
common_name = st.text_input("Common Name")
plant_part = st.text_input("Plant Part")
form = st.text_input("Form (Powder / Extract / Oil etc)")
category = st.text_input("Category (Herb / Oil / Resin / Mineral)")
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
    SELECT id,sanskrit_name,botanical_name,common_name,plant_part,form,category,price_per_kg
    FROM ingredients
    WHERE sanskrit_name LIKE '%{keyword}%'
    OR botanical_name LIKE '%{keyword}%'
    """

else:

    query = """
    SELECT id,sanskrit_name,botanical_name,common_name,plant_part,form,category,price_per_kg
    FROM ingredients
    """

df = pd.read_sql(query, conn)

conn.close()

st.dataframe(df)


# -----------------------------
# FORMULATION BUILDER
# -----------------------------

st.header("Formulation Builder")

product_name = st.text_input("Product Name")

conn = sqlite3.connect("ingredients.db")

ingredients = pd.read_sql(
    "SELECT sanskrit_name, botanical_name FROM ingredients",
    conn
)

ingredient_list = [
    f"{row['sanskrit_name']} ({row['botanical_name']})"
    for _, row in ingredients.iterrows()
]

conn.close()

selected_ingredient = st.selectbox(
    "Select Ingredient",
    ingredient_list
)

percentage = st.number_input("Ingredient % in Formula")

if st.button("Add Ingredient to Formula"):

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO formulations
        (product_name, ingredient_name, percentage)
        VALUES (?, ?, ?)
    """, (
        product_name,
        selected_ingredient,
        percentage
    ))

    conn.commit()
    conn.close()

    st.success("Ingredient added to formulation")
