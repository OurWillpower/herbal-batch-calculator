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

# Initialize database tables
create_ingredient_table()
create_formulation_table()
load_ingredients_from_csv()


# -------------------------------------------------
# ADD NEW INGREDIENT
# -------------------------------------------------

st.header("Add New Ingredient")

sanskrit_name = st.text_input("Sanskrit Name")
botanical_name = st.text_input("Botanical Name")
plant_part = st.text_input("Plant Part")
form = st.text_input("Form (Powder / Extract / Oil etc)")
price = st.number_input("Price per kg")

if st.button("Add Ingredient"):
    add_ingredient(sanskrit_name, botanical_name, plant_part, form, price)
    st.success("Ingredient added successfully")


# -------------------------------------------------
# SEARCH INGREDIENT DATABASE
# -------------------------------------------------

st.header("Search Ingredients")

keyword = st.text_input("Type Sanskrit or Botanical name")

if keyword:
    data = search_ingredients(keyword)
else:
    data = get_all_ingredients()

df = pd.DataFrame(
    data,
    columns=["ID", "Sanskrit Name", "Botanical Name", "Plant Part", "Form", "Price/kg"]
)

st.dataframe(df)


# -------------------------------------------------
# FORMULATION BUILDER
# -------------------------------------------------

st.header("Formulation Builder")

product_name = st.text_input("Product Name")

ingredient_list = get_ingredient_names()

selected_ingredient = st.selectbox(
    "Select Ingredient",
    ingredient_list
)

percentage = st.number_input("Ingredient % in Formula")

if st.button("Add Ingredient to Formula"):

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO formulations (product_name, ingredient_name, percentage)
        VALUES (?, ?, ?)
    """, (product_name, selected_ingredient, percentage))

    conn.commit()
    conn.close()

    st.success("Ingredient added to formulation")


# -------------------------------------------------
# VIEW FORMULATION
# -------------------------------------------------

if product_name:

    conn = sqlite3.connect("ingredients.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ingredient_name, percentage
        FROM formulations
        WHERE product_name = ?
    """, (product_name,))

    rows = cursor.fetchall()

    conn.close()

    if rows:
        st.subheader("Current Formulation")

        formula_df = pd.DataFrame(
            rows,
            columns=["Ingredient", "Percentage"]
        )

        st.dataframe(formula_df)
