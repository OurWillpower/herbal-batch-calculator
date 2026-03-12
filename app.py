import streamlit as st
import pandas as pd

from modules.database import create_ingredient_table, load_ingredients_from_csv
from modules.ingredient_manager import (
    add_ingredient,
    get_all_ingredients,
    search_ingredients,
    get_ingredient_names
)
st.title("Herbal Formulation System")

create_ingredient_table()
load_ingredients_from_csv()

st.header("Add New Ingredient")

sanskrit_name = st.text_input("Sanskrit Name")
botanical_name = st.text_input("Botanical Name")
plant_part = st.text_input("Plant Part")
form = st.text_input("Form (Powder / Extract / Oil etc)")
price = st.number_input("Price per kg")

if st.button("Add Ingredient"):
    add_ingredient(sanskrit_name, botanical_name, plant_part, form, price)
    st.success("Ingredient added successfully")

st.header("Search Ingredients")

keyword = st.text_input("Type Sanskrit or Botanical name")

if keyword:
    data = search_ingredients(keyword)
else:
    data = get_all_ingredients()

df = pd.DataFrame(
    data,
    columns=["ID","Sanskrit Name","Botanical Name","Plant Part","Form","Price/kg"]
)

st.dataframe(df)


st.header("Ingredient Selector")

ingredient_list = get_ingredient_names()

selected_ingredient = st.selectbox(
    "Select Ingredient from Database",
    ingredient_list
)

st.write("Selected Ingredient:", selected_ingredient)
