import streamlit as st
import pandas as pd
import sqlite3
import csv

st.title("Herbal Formulation System")

DB_FILE = "ingredients.db"

# -----------------------------
# DATABASE SETUP
# -----------------------------

def create_tables():
    conn = sqlite3.connect(DB_FILE)
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

create_tables()

# -----------------------------
# LOAD INGREDIENT MASTER CSV
# -----------------------------

st.header("Load Ingredient Master Database")

if st.button("Load Ingredients from CSV"):

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        with open("ingredients_master.csv", newline="", encoding="utf-8") as csvfile:

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
        st.success("Ingredient database imported")

    except:
        st.error("ingredients_master.csv not found")

    conn.close()

# -----------------------------
# ADD INGREDIENT
# -----------------------------

st.header("Add New Ingredient")

sanskrit = st.text_input("Sanskrit Name")
botanical = st.text_input("Botanical Name")
common = st.text_input("Common Name")
plant = st.text_input("Plant Part")
form = st.text_input("Form (Powder / Extract / Oil etc)")
category = st.text_input("Category")
price = st.number_input("Price per kg")

if st.button("Add Ingredient"):

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ingredients
        (sanskrit_name, botanical_name, common_name, plant_part, form, category, price_per_kg)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (sanskrit, botanical, common, plant, form, category, price))

    conn.commit()
    conn.close()

    st.success("Ingredient added")

# -----------------------------
# SEARCH INGREDIENTS
# -----------------------------

st.header("Search Ingredients")

keyword = st.text_input("Type Sanskrit or Botanical name")

conn = sqlite3.connect(DB_FILE)

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

# -----------------------------
# FORMULATION BUILDER
# -----------------------------

st.header("Formulation Builder")

product_name = st.text_input("Product Name")

conn = sqlite3.connect(DB_FILE)
ingredients = pd.read_sql("SELECT sanskrit_name FROM ingredients", conn)
conn.close()

ingredient_list = ingredients["sanskrit_name"].tolist()

ingredient = st.selectbox("Select Ingredient", ingredient_list)
percentage = st.number_input("Ingredient %")

if st.button("Add to Formulation"):

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO formulations
        (product_name, ingredient_name, percentage)
        VALUES (?, ?, ?)
    """, (product_name, ingredient, percentage))

    conn.commit()
    conn.close()

    st.success("Ingredient added to formulation")

# -----------------------------
# SHOW FORMULATION
# -----------------------------

if product_name:

    conn = sqlite3.connect(DB_FILE)
    formula = pd.read_sql(
        f"SELECT ingredient_name, percentage FROM formulations WHERE product_name='{product_name}'",
        conn
    )
    conn.close()

    st.subheader("Current Formula")
    st.dataframe(formula)

# -----------------------------
# BATCH CALCULATOR
# -----------------------------

st.header("Batch Quantity Calculator")

batch_size = st.number_input("Batch Size (kg or liters)")

if product_name and batch_size:

    conn = sqlite3.connect(DB_FILE)

    formula = pd.read_sql(
        f"SELECT ingredient_name, percentage FROM formulations WHERE product_name='{product_name}'",
        conn
    )

    conn.close()

    if not formula.empty:

        formula["Required Quantity"] = batch_size * formula["percentage"] / 100

        st.subheader("Raw Material Requirement")
        st.dataframe(formula)
