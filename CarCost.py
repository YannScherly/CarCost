
import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import numpy as np
import warnings
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
kmdrivenpermonth = st.number_input('Average monthly kilometers driven', min_value=0)
petrolprice = st.number_input('Enter the actual petrol price', min_value=0.5, max_value=10, value=1.5)
st.header('Personal details')
age = st.number_input('Age', min_value=16)
typeofdriver = st.selectbox('How would you describe your driving style?',['Ecological','Normal','Aggressive'])
options_mapping = {
    'Ecological': 2,
    'Normal': 8,
    'Aggressive': 15,
}
typeofinsurance = st.selectbox('Which type of insurance would you subscribe?', ['Legal Minimum', 'Partially Covered', 'Fully Insured']) 
options_mapping = {
    'Legal minimum': 900,
    'Partially Covered': 1500,
    'Fully Covered': 2500,
}
monthsofusage = st.selectbox('For how many months are you planning on using the selected car?', ['12', '24', '36', '48'])


def predict_price(year, kmdrivenpermonth, petrolprice, typeofdriver, typeofinsurance, price):
    return (2024 - year) * 50 + kmdrivenpermonth * 0.1 + kmdrivenpermonth * petrolprice * typeofdriver / 100 + price * 0.01 + typeofinsurance + typeofdriver * 100




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
