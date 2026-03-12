import streamlit as st
from modules.database import create_ingredient_table

st.title("Herbal Formulation System")

# create ingredient table when app starts
create_ingredient_table()

st.write("System initialized successfully.")
