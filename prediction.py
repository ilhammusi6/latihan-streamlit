import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

def prediction_app():
    st.subheader("Aplikasi Prediksi Harga Taxi Trip")
    st.write(
        "Aplikasi ini memungkinkan pengguna untuk memprediksi harga perjalanan taksi "\
        "berdasarkan fitur-fitur perjalanan yang dimasukkan. Pengguna dapat memasukkan "\
        "informasi seperti jarak perjalanan, durasi perjalanan, jumlah penumpang, "\
        "kondisi lalu lintas, dan struktur tarif untuk mendapatkan prediksi harga."
    )
    # Load the trained model, scaler, and feature columns
    model = joblib.load('taxi_price_model.pkl')
    scaler = joblib.load('scaler.pkl')
    model_features = joblib.load('model_features.pkl')
    
    # User inputs
    st.write("Masukkan detail perjalanan taksi:")
    distance = st.number_input("Jarak Perjalanan (km)", min_value=0.0, step=0.1)
    duration = st.number_input("Durasi Perjalanan (menit)", min_value=0)
    passenger_count = st.number_input("Jumlah Penumpang", min_value=1, step=1)
    traffic_conditions = st.selectbox("Kondisi Lalu Lintas",  
                                        ['Light Traffic', 'Moderate Traffic', 'Heavy Traffic', 'Very Heavy Traffic'])
    fare_structure = st.selectbox("Struktur Tarif",
                                    ['Standard', 'Premium', 'Shared', 'Flat Rate'])
    
    # Prepare input data for prediction
    input_data = pd.DataFrame({
        'Trip_Distance_km': [distance], 
        'Trip_Duration_Minutes': [duration],
        'Passenger_Count': [passenger_count],
        'Traffic_Conditions': [traffic_conditions],
        'Fare_Structure': [fare_structure]
    })
    # One-hot encode categorical variables
    input_data = pd.get_dummies(input_data)

    # Ensure all model features are present
    for col in model_features:
        if col not in input_data.columns:
            input_data[col] = 0
    input_data = input_data[model_features]

    # Scale input data
    input_data_scaled = scaler.transform(input_data)
    
    # Predict button
    if st.button("Prediksi Harga"):
        prediction = model.predict(input_data_scaled)
        st.success(f"Prediksi Harga Taxi Trip: ${prediction[0]:.2f}")   
    st.write(
        "Aplikasi prediksi ini memanfaatkan model machine learning yang telah dilatih "\
        "untuk memberikan estimasi harga perjalanan taksi berdasarkan fitur-fitur yang "\
        "dimasukkan oleh pengguna."
    )

