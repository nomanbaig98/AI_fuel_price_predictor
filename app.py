import streamlit as st
import numpy as np
import joblib
from pathlib import Path
import pickle
import streamlit_authenticator as stauth

# Set up the Streamlit app
st.set_page_config(
    page_title="Fuel Price Predictor",
    page_icon=":fuelpump:",
    layout="wide"
)

# --- USER AUTHENTICATION ---
names = ["Josh Pettingill", "David Bender", "Roy Franco"]
usernames = ["jpett", "dbend", "rfranc"]


# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")


# Define the main function for the Streamlit app
if authentication_status:

    st.title('Fuel Price Predictor')

    # Load the saved models
    models = {
        'Petrol': joblib.load('random_forest_regressor_model_for_petrol.joblib'),
        'Diesel': joblib.load('random_forest_regressor_model_for_diesel.joblib'),
        'LPG': joblib.load('random_forest_regressor_model_for_lpg.joblib'),
        'Kerosene': joblib.load('random_forest_regressor_model_for_kerosene.joblib'),
        'MGO': joblib.load('random_forest_regressor_model_for_mgo.joblib')
    }

    # Create a sidebar for user input
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")

    selected_model = st.sidebar.selectbox("Select the fuel type", ['Petrol', 'Diesel', 'LPG', 'Kerosene', 'MGO'])

    st.sidebar.subheader("Input Features:")
    #mgo_local = st.sidebar.number_input("MGO LOCAL (GHp/Lt)")
    #kerosene = st.sidebar.number_input("KEROSENE (GHp/Lt)")
    #lpg = st.sidebar.number_input("LPG (GHp/Kg)")

    # Depending on the selected fuel type, choose the appropriate input features
    if selected_model == 'Petrol':
        diesel = st.sidebar.number_input("DIESEL (GHp/Lt)")
        lpg = st.sidebar.number_input("LPG (GHp/Kg)")
        kerosene = st.sidebar.number_input("KEROSENE (GHp/Lt)")
        mgo_local = st.sidebar.number_input("MGO LOCAL (GHp/Lt)")
        user_input = np.array([[mgo_local, kerosene, lpg, diesel]])
        prediction_model = models['Petrol']

    elif selected_model == 'Diesel':
        petrol = st.sidebar.number_input("PETROL (GHp/Lt)")
        user_input = np.array([[mgo_local, kerosene, lpg, petrol]])
        prediction_model = models['Diesel']

    elif selected_model == 'LPG':
        petrol = st.sidebar.number_input("PETROL (GHp/Lt)")
        diesel = st.sidebar.number_input("DIESEL (GHp/Lt)")
        user_input = np.array([[mgo_local, kerosene, diesel, petrol]])
        prediction_model = models['Diesel']

    elif selected_model == 'Kerosene':
        petrol = st.sidebar.number_input("PETROL (GHp/Lt)")
        user_input = np.array([[mgo_local, lpg, diesel, petrol]])
        prediction_model = models['Kerosene']

    elif selected_model == 'MGO':
        diesel = st.sidebar.number_input("DIESEL (GHp/Lt)")
        petrol = st.sidebar.number_input("PETROL (GHp/Lt)")
        user_input = np.array([[kerosene, lpg, diesel, petrol]])
        prediction_model = models['MGO']

    if st.sidebar.button("Predict Fuel Price"):
        # Make a prediction using the selected model
        fuel_price_prediction = prediction_model.predict(user_input)

        # Display the prediction
        st.write(f'The predicted {selected_model} price for current month is: GHp/Lt', fuel_price_prediction)
