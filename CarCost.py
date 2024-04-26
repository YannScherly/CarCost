
import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from shapedata.py import process_car_data
#run a simplified version of shapedata.py cause we didn't know how to refer to it
car_df = pd.read_csv('CarPrice.csv')
processed_car_df = process_car_data(car_df)


 
 

st.title("Prediction of Monthly Expenses for a Second Hand Car")
st.header('Fill in the details to predict your average monthly expenses')
        
 # Display the uploaded DataFrame
st.write("Uploaded DataFrame:", car_df)
        
 # Dropdown for selecting a car brand
brand = st.selectbox('Brand', car_df['Brand Name'].unique())
        
# Filter DataFrame based on selected brand
filtered_df = car_df[car_df['Brand Name'] == brand]
        
# Dropdown for selecting a car model based on the selected brand
model = st.selectbox('Model', filtered_df['CarName'].unique())
        
# Filter DataFrame based on selected model
price = filtered_df[filtered_df['CarName'] == model]['price'].iloc[0]
fueltype = filtered_df[filtered_df['CarName'] == model]['fueltype'].iloc[0]  
horsepower = filtered_df[filtered_df['CarName'] == model]['horsepower'].iloc[0] 
mpg = filtered_df[filtered_df['CarName'] == model]['highwaympg'].iloc[0]

# Display infos of the selected car model
st.write("Infos regarding", model, "->","price:", price, "Fueltype:", fueltype, "Horsepower:", horsepower)


# Create the user interface

year = st.number_input("Enter the year of the car", min_value=2005, max_value=2024)
kmdrivenpermonth = st.number_input('Average monthly kilometers driven', min_value=0)
 
st.header('Personal details')
age = st.number_input('Age', min_value=16)
typeofdriver = st.selectbox('How would you describe your driving style?',['Ecological','Normal','Aggressive'])
 
 
st.header('')
 
# Add a button to trigger the prediction
if st.button('Predict Price'):
    price = predict_price(brand, year, kmdriven, fuel,)
    st.success(f'You can expect, on average, {price:,.0f} Swiss Francs for charges, per month, for your second hand car.')
LOGGER = get_logger(__name__)

