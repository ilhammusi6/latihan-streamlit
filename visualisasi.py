import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Taxi Trip Price Analysis Dashboard",    
    layout="wide",
    initial_sidebar_state="expanded"
)

def chart():
    # Inject CSS untuk KPI card dengan efek hover
    st.markdown("""
        <style>
        .kpi-card {
            background-color: #fdf6f0;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            text-align: center;
        }
        .kpi-card:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        }
        .kpi-title {
            font-size: 16px;
            color: #555;
            margin-bottom: 8px;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: bold;
            color: #d35400;
        }
        </style>
    """, unsafe_allow_html=True)

    df = pd.read_csv('Taxi Trip Price.csv')
    st.dataframe(df.head())

    # KPI Metrics
    st.subheader('KPI Metrics')
    total_trips = len(df)
    average_price = df['Trip_Price'].mean()
    average_distance = df['Trip_Distance_km'].mean()
    average_duration = df['Trip_Duration_Minutes'].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Perjalanan Taxi</div>
                <div class="kpi-value">{total_trips}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Rata-Rata Harga Taxi</div>
                <div class="kpi-value">${average_price:.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Rata-Rata Jarak (km)</div>
                <div class="kpi-value">{average_distance:.2f} km</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Rata-Rata Durasi (menit)</div>
                <div class="kpi-value">{average_duration:.2f} menit</div>
            </div>
        """, unsafe_allow_html=True)

    # Visualisasi Jumlah Penumpang
    st.subheader('Visualisasi Jumlah Penumpang Taxi')   
    fig1 = px.histogram(df, x='Passenger_Count', nbins=30, title='Distribusi Jumlah Penumpang')
    st.plotly_chart(fig1, use_container_width=True)

    # Durasi vs Harga
    st.subheader('Pengaruh Durasi Perjalanan terhadap Harga Taxi')
    fig2 = px.scatter(df, x='Trip_Duration_Minutes', y='Trip_Price', 
                      title='Durasi Perjalanan vs Harga Taxi',
                      trendline='ols')
    st.plotly_chart(fig2, use_container_width=True)

    st.write("Durasi perjalanan lebih lama → harga lebih tinggi akibat tarif berbasis waktu.")

    # Harga vs Traffic
    st.subheader('Distribusi Harga Taxi Berdasarkan Kondisi Lalu Lintas')
    fig3 = px.box(df, x='Traffic_Conditions', y='Trip_Price', 
                  title='Distribusi Harga Taxi berdasarkan Kondisi Lalu Lintas')
    st.plotly_chart(fig3, use_container_width=True)

    # Harga vs Time of Day
    st.subheader('Rata-Rata Harga Taxi Berdasarkan Waktu Perjalanan')
    fig4 = px.bar(df.groupby('Time_of_Day')['Trip_Price'].mean().reset_index(),
                  x='Time_of_Day', y='Trip_Price',
                  title='Rata-Rata Harga Taxi berdasarkan Waktu Perjalanan')    
    st.plotly_chart(fig4, use_container_width=True)

    # Harga vs Weather
    st.subheader('Perbandingan Harga Taxi Berdasarkan Kondisi Cuaca')
    fig5 = px.violin(df, x='Weather', y='Trip_Price', 
                     title='Perbandingan Harga Taxi berdasarkan Kondisi Cuaca',
                     box=True, points='all')
    st.plotly_chart(fig5, use_container_width=True)

    # Weekday vs Weekend
    st.subheader('Perbandingan Harga Taxi antara Weekday dan Weekend')
    fig6 = px.box(df, x='Time_of_Day', y='Trip_Price', 
                  title='Perbandingan Harga Taxi antara Weekday dan Weekend')   
    st.plotly_chart(fig6, use_container_width=True)

    # Statistik Deskriptif
    st.subheader('Ringkasan Statistik Deskriptif Harga Taxi')
    st.write(df['Trip_Price'].describe())

    # Korelasi
    st.subheader('Korelasi Antara Fitur Numerik')
    corr = df[['Trip_Price', 'Trip_Distance_km', 'Trip_Duration_Minutes', 'Passenger_Count']].corr()
    fig7 = px.imshow(corr, text_auto=True, title='Matriks Korelasi Antara Fitur Numerik')
    st.plotly_chart(fig7, use_container_width=True)
