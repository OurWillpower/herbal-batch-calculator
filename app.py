import streamlit as st
from modules.database import create_ingredient_table
from modules.ingredient_manager import add_ingredient

st.title("Herbal Formulation System")

create_ingredient_table()

st.header("Add New Ingredient")

sanskrit_name = st.text_input("Sanskrit Name")
botanical_name = st.text_input("Botanical Name")
plant_part = st.text_input("Plant Part")
form = st.text_input("Form (Powder / Extract / Oil etc)")
price = st.number_input("Price per kg")

if st.button("Add Ingredient"):
    add_ingredient(sanskrit_name, botanical_name, plant_part, form, price)
    st.success("Ingredient added successfully")
