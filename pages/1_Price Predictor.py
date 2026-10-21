import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(page_title="Viz Demo")

with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

st.header('Enter your inputs')

# property_type
property_type = st.selectbox('Property Type',['flat','house'])

# sector
sector = st.selectbox('Sector',sorted(list(df['sector'].unique())))

# bedroom
bedroom = int(st.selectbox('Number of Bedroom',sorted(list(df['bedRoom'].unique()))))

# bathroom
bathroom = int(st.selectbox('Number of Bathroom',sorted(list(df['bathroom'].unique()))))

# balcony
balcony = st.selectbox('Number of Balcony',sorted(list(df['balcony'].unique())))

# agepossesion
property_age = st.selectbox('Property Age',sorted(list(df['agePossession'].unique())))

# built_up_area
def estimate_built_up_area(bedroom, bathroom, balcony, property_type):
    
    balcony_n = 3 if str(balcony) == '3+' else int(balcony)

    if property_type == 'Flat':
        area = 290 * bedroom + 260 * bathroom + 35 * balcony_n
    else:  # House
        area = 300 * bedroom + 150 * bathroom + 100 * balcony_n

    return int(max(area, 300))

default_area = estimate_built_up_area(bedroom, bathroom, balcony, property_type)

built_up_area = float(st.number_input('Built Up Area (sqft)',min_value=100,value=default_area,
                                      step=10,key=f'built_up_{default_area}'))

def change(x):
    if x=='Yes':
        return 1
    else:
        return 0

# servant room
servant_room = change(st.selectbox('Servant Room',['No','Yes']))

# store room
store_room = change(st.selectbox('Store Room',['No','Yes']))

# furnishing type
furnishing_type = st.selectbox('Furnishing Type',sorted(list(df['furnishing_type'].unique())))

# luxury category
luxury_category = st.selectbox('Luxury Category',sorted(list(df['luxury_category'].unique())))

# floor category
floor_category = st.selectbox('Floor Category',sorted(list(df['floor_category'].unique())))

if st.button('Predict'):

    # Form a DataFrame

    data = [[property_type, sector, bedroom, bathroom, balcony, property_age, built_up_area,
             servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    # Predict
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.24
    high = base_price + 0.24

    # Display
    st.text("The price of the {} is between {} Cr and {} Cr".format(one_df.iloc[0,:]['property_type'],round(low,2), round(high,2)))
