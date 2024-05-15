# imports for coding in Python
import streamlit as st
import pandas as pd
import warnings
import matplotlib.pyplot as plt
from streamlit.logger import get_logger
warnings.filterwarnings('ignore')

# transform the dataset into a format that is project-useful.
car_df = pd.read_csv('CarPrice.csv')
car_df.head()
car_df.duplicated().sum()
car_df.drop_duplicates(inplace=True)
car_df['Brand Name'] = car_df['CarName'].str.split(' ').str.slice(0, 1).str.join('')
car_df['Model'] = car_df['CarName'].str.split('').str.slice(2, 3).str.join('')
car_df['Model name'] = car_df['CarName'].str.split(' ').str.slice(2, 3).str.join('')
car_df.rename(columns={'carname': 'Model name'}, inplace=True)
car_df.drop('Model name', axis=1, inplace=True)
car_df = car_df.iloc[:, [26, 2, 25, 3, 5, 21, 24]]
# Title
st.title("Prediction of Monthly Expenses for a Second Hand Car")
st.header('Fill in the details to predict your average monthly expenses')
        
# Display the uploaded DataFrame
st.write("Uploaded DataFrame:", car_df)
        
# Dropdown for selecting a car brand
brand = st.selectbox('Brand', car_df['Brand Name'].unique())
        
# Filter DataFrame based on selected brand
filtered_df = car_df[car_df['Brand Name'] == brand]
        
# Dropdown for selecting a car model based on the selected brand
# Splitting the model names and selecting the second word or rest of the words
model = st.selectbox('Model', filtered_df['CarName'].unique())


# Filter DataFrame based on selected model
price = filtered_df[filtered_df['CarName'] == model]['price'].iloc[0]
fueltype = filtered_df[filtered_df['CarName'] == model]['fueltype'].iloc[0]
horsepower = filtered_df[filtered_df['CarName'] == model]['horsepower'].iloc[0]
mpg = filtered_df[filtered_df['CarName'] == model]['highwaympg'].iloc[0]

        
# Display infos of the selected car model
st.write("Infos regarding", model, "->", "price:", price, "Fueltype:", fueltype, "Horsepower:", horsepower)


# Create the user interface & ensuring that the data in the calculations are in float
year = st.number_input("Enter the year of the car", min_value=2005, max_value=2024)
year = float(year)
kmdrivenperyear = st.number_input('Average yearly kilometers driven', min_value=0)
kmdrivenperyear = float(kmdrivenperyear)
petrolprice = st.number_input('Enter the actual petrol price in frs', min_value=0.5, max_value=10.0, value=1.5)
petrolprice = float(petrolprice)
st.header('Personal details')
age = st.number_input('Age', min_value=16)
typeofdriver = st.selectbox('How would you describe your driving style?', ['Ecological', 'Normal', 'Aggressive'])
# assigning a mathematical value to the different categories
options_mapping_driver = {
    'Ecological': 2,
    'Normal': 8,
    'Aggressive': 15,
}
typeofdriver_numeric = options_mapping_driver[typeofdriver]
typeofdriver = float(typeofdriver_numeric)
typeofinsurance = st.selectbox('Which type of insurance would you subscribe?',
                               ['Legal Minimum', 'Partially Covered', 'Fully Insured'])
options_mapping_insurance = {
    'Legal Minimum': 900,
    'Partially Covered': 1500,
    'Fully Insured': 2500,
}
typeofinsurance_numeric = options_mapping_insurance[typeofinsurance]
typeofinsurance = float(typeofinsurance_numeric)
monthsofusage = st.selectbox('For how many months are you planning on using the selected car?',
                             ['12', '24', '36', '48'])
monthsofusage = float(monthsofusage)

# Cost computation
def predict_price(year, kmdrivenperyear, petrolprice, typeofdriver, typeofinsurance, price, mpg, monthsofusage):
    fuel_cost = ((kmdrivenperyear / 12 * monthsofusage) * petrolprice * typeofdriver * (2.35 / mpg)) / monthsofusage
    usage_cost = (price * 0.01 + typeofdriver * 100 + (2024 - year) * 50 +
                  (kmdrivenperyear / 12 * monthsofusage) * 0.1)/ monthsofusage
    total_cost = (fuel_cost/10 + usage_cost + typeofinsurance)
    return total_cost


# Add a button to trigger the prediction

if st.button('Predict Price'):
    st.success(f'You can expect, on average, {predict_price(year, kmdrivenperyear, petrolprice, typeofdriver, typeofinsurance, price, mpg, monthsofusage):,.0f} '
               f'Swiss Francs of charges, per month, for your car.')

 # Sort the expenses into smaller groups.
fuel_cost = ((kmdrivenperyear / 12 * monthsofusage) * petrolprice * typeofdriver * (2.35 / mpg)) / monthsofusage /10
insurance_cost = typeofinsurance
usage_cost = ((price * 0.01 + typeofdriver * 100 + (2024 - year) * 50 + (kmdrivenperyear / 12 * monthsofusage) * 0.1))\
             / monthsofusage

cost_breakdown = {'Fuel Cost': fuel_cost, 'Insurance Cost': insurance_cost, 'Usage cost': usage_cost}

labels = list(cost_breakdown.keys())
values = list(cost_breakdown.values())
# Define a custom pie chart
def my_autopct(pct):
    total = sum(values)
    val = int(round(pct*total/100))
    return f'{pct:.1f}% ({val:,.0f} CHF)'
custom_colors = ['#F08080', '#87CEFA', '#98FB98']


fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct=my_autopct, colors=custom_colors)  # Fixed the string literal here
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)


LOGGER = get_logger(__name__)
