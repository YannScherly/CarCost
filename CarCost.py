
import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
car_df = pd.read_csv('CarPrice.csv')
from shapedata import process_car_data

def process_car_data(CarPrice):
    # Read the CSV file
    car_df = pd.read_csv('CarPrice.csv')
    
    # Drop duplicates
    car_df.drop_duplicates(inplace=True)
    
    # Extract 'Brand Name' and 'Model' from 'CarName' column
    car_df['Brand Name'] = car_df['CarName'].str.split().str[0]
    car_df['Model'] = car_df['CarName'].str.split().str[1]
    
    # Select relevant columns
    car_df = car_df[['Brand Name', 'Model', 'Price', 'Mileage', 'Engine', 'Power', 'Seats']]
    
    return car_df

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
typeofinsurance = st.selectbox('Which type of insurance would you subscribe?', ['Legal Minimum', 'Partially Covered', 'Fully Insured']) 
monthsofusage = st.selectbox('For how many months are you planning on using the selected car?', ['12', '24', '36', '48'])
 
st.header('')

# Add a button to trigger the prediction
if st.button('Predict Price'):
    price = predict_price
    st.success(f'You can expect, on average, {price:,.0f} Swiss Francs for charges, per month, for your car.')
 # Step 1: Collect User Inputs
st.sidebar.title("Graph Input Parameters")
x_min = st.sidebar.number_input("Minimum X value", value=0)
x_max = st.sidebar.number_input("Maximum X value", value=10)
step = st.sidebar.number_input("Step size", value=0.1)

# Step 2: Perform Calculations
x_values = np.arange(x_min, x_max, step)
y_values = np.sin(x_values)  # Example calculation (sin function)

# Step 3: Plot Graph
fig, ax = plt.subplots()
ax.plot(x_values, y_values)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Graph of y = sin(x)')

# Step 4: Display the Graph
st.pyplot(fig)
LOGGER = get_logger(__name__)


