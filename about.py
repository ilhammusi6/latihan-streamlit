import streamlit as st

def about_dataset():
    st.write('**Tentang Dataset**')
    col1, col2= st.columns([5,5])

    with col1:
        link = "https://i.pinimg.com/1200x/6a/d6/0d/6ad60db79e97190a53bb80e085552d1f.jpg"
        st.image(link, caption="Taxi Trip Dataset")

    with col2:
        
        st.write(
        'Dataset Taxi Trip Price merupakan kumpulan data perjalanan taksi yang '\
        'digunakan untuk menganalisis faktor-faktor yang memengaruhi harga perjalanan. '\
        'Dataset ini mencakup informasi jarak tempuh, durasi perjalanan, waktu perjalanan, '\
        'jumlah penumpang, kondisi lalu lintas, kondisi cuaca, serta struktur tarif yang diterapkan. '\
        'Data ini digunakan untuk mendukung proses analisis eksploratif (EDA), '
        'data preprocessing, feature engineering, serta pengembangan model prediksi harga. '\
        'Setiap baris data merepresentasikan satu perjalanan taksi dengan informasi '\
        'yang relevan untuk memahami pola dan determinan biaya perjalanan.'\
        )
