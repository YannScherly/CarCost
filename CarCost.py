
import streamlit as st
import pandas as pd
import numpy as np
import warnings
from streamlit.logger import get_logger
warnings.filterwarnings('ignore')

car_df=pd.read_csv('CarPrice.csv')
car_df.head()
car_df.duplicated().sum()
car_df.drop_duplicates(inplace= True)
car_df['Brand Name']=car_df['CarName'].str.split(' ').str.slice(0,1).str.join('')
car_df['Model']=car_df['CarName'].str.split('').str.slice(2,3).str.join('')
car_df['Model name']=car_df['CarName'].str.split(' ').str.slice(2,3).str.join('')
car_df.rename(columns={'carname':'Model name'},inplace=True)
car_df.drop('Model name',axis=1,inplace=True)
car_df=car_df.iloc[:,[26,2,25,3,5,21,24]]



 
 

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
year = float(year)
kmdrivenperyear = st.number_input('Average yearly kilometers driven', min_value=0)
kmdrivenperyear = float(kmdrivenperyear)
petrolprice = st.number_input('Enter the actual petrol price in frs', min_value=0.5, max_value=10.0, value=1.5)
petrolprice = float(petrolprice)
st.header('Personal details')
age = st.number_input('Age', min_value=16)
typeofdriver = st.selectbox('How would you describe your driving style?',['Ecological','Normal','Aggressive'])
options_mapping_driver = {
    'Ecological': 2,
    'Normal': 8,
    'Aggressive': 15,
}
typeofdriver_numeric = options_mapping_driver[typeofdriver]
typeofdriver = float(typeofdriver_numeric)
typeofinsurance = st.selectbox('Which type of insurance would you subscribe?', ['Legal Minimum', 'Partially Covered', 'Fully Insured']) 
options_mapping_insurance = {
    'Legal Minimum': 900,
    'Partially Covered': 1500,
    'Fully Insured': 2500,
}
typeofinsurance_numeric = options_mapping_driver[typeofinsurance]
typeofinsurance = float(typeofinsurance_numeric)
monthsofusage = st.selectbox('For how many months are you planning on using the selected car?', ['12', '24', '36', '48'])
monthsofusage = float(monthsofusage)

def predict_price(year, kmdrivenperyear, petrolprice, typeofdriver, typeofinsurance, price, mpg, monthsofusage):
    return (((2024 - year) * 50 + (kmdrivenperyear / 12 * monthsofusage) * 0.1 + (kmdrivenperyear / 12 * monthsofusage) * petrolprice * typeofdriver * (2.35/mpg)) / 100 + price * 0.01 + typeofdriver * 100) / 12 + typeofinsurance


# Add a button to trigger the prediction

if st.button('Predict Price'):
    price_predicted = predict_price(year, kmdrivenperyear, petrolprice, typeofdriver, typeofinsurance, price, mpg, monthsofusage)
    st.success(f'You can expect, on average, {price_predicted:,.0f} Swiss Francs for charges, per month, for your car.')




LOGGER = get_logger(__name__)
