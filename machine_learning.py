from xml.parsers.expat import model
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import numpy as np

st.subheader("Machine Learning Approach")

st.write(
    "Pada tahap ini, pendekatan Machine Learning yang digunakan adalah "\
    "Supervised Learning dengan tipe Regression. Pendekatan ini dipilih "\
    "karena dataset memiliki variabel target yang jelas, yaitu Trip_Price, "\
    "yang merepresentasikan harga perjalanan taksi. "\
    "Model regresi digunakan untuk mempelajari hubungan antara variabel "\
    "input seperti jarak perjalanan, durasi perjalanan, waktu perjalanan, "\
    "kondisi lalu lintas, dan struktur tarif terhadap harga perjalanan. "\
    "Pendekatan ini memungkinkan sistem untuk melakukan prediksi harga "\
    "berdasarkan data historis yang tersedia.")

def ml_model():
    df = pd.read_csv('Taxi Trip Price.csv')
    st.write("Dataset terdiri dari 10 fitur dan 1 target variabel yaitu Trip_Price.")
    st.dataframe(df.head()) 
    st.info(
    "Jenis Machine Learning: Supervised Learning\n"\
    "Tipe Model: Regression\n"\
    "Target Variable: Trip_Price"\
    )  
        # Data Preprocessing
    df_ml = df.copy()
    df_ml.info()

    df_ml.describe()

    #cek duplikasi & missing value
    st.write("Cek Duplikasi dan Missing Value")
    st.write("Jumlah Duplikasi: ", df_ml.duplicated().sum())
    
    df_ml.isna().sum()

    df_ml = df_ml.dropna()

    round(df_ml.describe(),2)

    #numeric isi dengan median
    numbers = df_ml.select_dtypes(include=['int64', 'float64']).columns
    for col in numbers:
        median = df_ml[col].median()
        df_ml[col].fillna(median, inplace=True)
    #categoric isi dengan modus
    categoric = df_ml.select_dtypes(include=['object']).columns
    for col in categoric:
        mode = df_ml[col].mode()[0]
        df_ml[col].fillna(mode, inplace=True)
    #cek ulang missing value
    df_ml.isna().sum()
    
    # memisahkan variabel X dan Y
    X = df_ml.drop('Trip_Price', axis=1)
    y = df_ml['Trip_Price']

    # IQR
    Q1 = df_ml [numbers].quantile(0.25)
    Q3 = df_ml [numbers].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df_ml = df_ml[~((df_ml[numbers] < lower_bound) | (df_ml[numbers] > upper_bound)).any(axis=1)]

    # cek kolinearitas heatmap
    corr = df_ml[numbers].corr()
    fig = px.imshow(corr, text_auto=True, title='Heatmap Korelasi Fitur Numerik')
    st.plotly_chart(fig)
    
    #vif 
    from statsmodels.stats.outliers_influence import variance_inflation_factor  
    vif_data = pd.DataFrame()
    vif_data["feature"] = X.select_dtypes(include=['int64', 'float64']).columns
    vif_data["VIF"] = [variance_inflation_factor(X.select_dtypes(include=['int64', 'float64']).values, i)
                       for i in range(len(X.select_dtypes(include=['int64', 'float64']).columns))]
    
    #train test split
    X = pd.get_dummies(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    st.write("Data telah dibagi menjadi data latih dan data uji dengan rasio 80:20.")

    #normalisasi
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    st.write("Fitur numerik telah dinormalisasi menggunakan StandardScaler.")

    #modelling dengan regresi linear

    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    #melihat koefisien masing-masing fitur
    coefficients = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': model.coef_
    }).sort_values(by='Coefficient', ascending=False)

    #melihat nilai intercept
    intercept = model.intercept_

    #modeling dengan ridge dan lasso
    from sklearn.linear_model import Ridge, Lasso
    ridge = Ridge(alpha=0.001)
    ridge.fit(X_train_scaled, y_train)
    lasso = Lasso(alpha=0.162)
    lasso.fit(X_train_scaled, y_train)

    #melihat koefisien masing-masing fitur
    coef_df_ml_ridge = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': ridge.coef_
    }).sort_values(by='Coefficient', ascending=False)

    coef_df_ml_lasso = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': lasso.coef_
    }).sort_values(by='Coefficient', ascending=False)   

    #evaluasi model
    def evaluate_model(model, X_test, y_test):
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        return mae, mse, rmse, r2
    
    # prediksi untuk masing-masing model
    mae_lr, mse_lr, rmse_lr, r2_lr = evaluate_model(model,
                                                    X_test_scaled, y_test)
    mae_ridge, mse_ridge, rmse_ridge, r2_ridge = evaluate_model(ridge,
                                                    X_test_scaled, y_test)  
    mae_lasso, mse_lasso, rmse_lasso, r2_lasso = evaluate_model(lasso,
                                                    X_test_scaled, y_test)  
    #menampilkan hasil evaluasi model
    eval_df = pd.DataFrame({
        'Model': ['Linear Regression', 'Ridge Regression', 'Lasso Regression'],
        'MAE': [mae_lr, mae_ridge, mae_lasso],
        'MSE': [mse_lr, mse_ridge, mse_lasso],
        'RMSE': [rmse_lr, rmse_ridge, rmse_lasso],
        'R2 Score': [r2_lr, r2_ridge, r2_lasso]
    })
    st.write("Hasil Evaluasi Model:")
    st.dataframe(eval_df)

    # Simpan model dan fitur kolom agar prediction.py bisa pakai
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(model, 'taxi_price_model.pkl')
    joblib.dump(X.columns.tolist(), 'model_features.pkl')

    return model

    






    