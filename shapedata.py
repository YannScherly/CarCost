import pandas as pd
import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


processed_data = process_car_data('CarPrice.csv')
def process_car_data('CarPrice.csv'):
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
