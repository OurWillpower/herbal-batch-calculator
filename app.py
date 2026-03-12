import streamlit as st
import pandas as pd

st.title("Herbal Batch Calculator")

batch_size = st.number_input("Enter Batch Size (Liters)", value=100)

data = {
    "Ingredient":[
        "Shunthi",
        "Thyme",
        "Tvak",
        "Madhurika",
        "Sukshmaila",
        "Tulasi",
        "Haridra"
    ],
    "Percentage":[0.50,0.20,0.20,0.20,0.20,0.50,0.50]
}

df = pd.DataFrame(data)

df["Required Kg"] = batch_size * df["Percentage"] / 100

st.write(df)
from modules.database import *
from modules.ingredient_manager import *
from modules.formulation_builder import *
from modules.batch_calculator import *
