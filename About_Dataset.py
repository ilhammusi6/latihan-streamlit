import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.markdown("""
    <style>
    /* Efek hover untuk tab */
    .stTabs [role="tab"] {
        transition: all 0.3s ease;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 500;
    }

    .stTabs [role="tab"]:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        background-color: #f0f0f0;
        cursor: pointer;
    }

    /* Tab aktif */
    .stTabs [aria-selected="true"] {
        background-color: #ffe6e6;
        color: #d00000;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border-bottom: 2px solid #d00000;
    }
    </style>
""", unsafe_allow_html=True)

st.header('Analisa Dan Prediksi Tarif Taxi')
st.write('**Pelatihan Data Science 1.0** - dibimbing')
st.write('Jakarta , 4 Januari 2026')

tab1, tab2, tab3, tab4, tab5 = st.tabs(['About Dataset', 
                            'Dashboards', 
                            'Machine Learning',
                            'Prediction App',
                            'Contact Me'])

with tab1:
    import about
    about.about_dataset()

with tab2:
    import visualisasi
    visualisasi.chart()

with tab3:
    import machine_learning
    machine_learning.ml_model()

with tab4:
    import prediction
    prediction.prediction_app()

with tab5:
    import kontak
    kontak.contact_me()
