import streamlit as st
import pandas as pd
import plotly.express as px

st.title('hello, streamlit')
st.write('this is simple streamlit application')

st.write('*ini contoh huruf miring*')
st.write('**ini contoh huruf tebal**')
st.write('***ini contoh huruf tebal miring***')

penjualan_oktober = 900
penjualan_november = 850
penjualan_desember = 1000

selisih1 = penjualan_desember - penjualan_november
selisih2 = penjualan_november - penjualan_oktober

st.metric(label ="penjualan sekarang", value = penjualan_desember, delta = selisih1)
st.metric(label ="penjualan sekarang", value = penjualan_november, delta = selisih2)

df = pd.read_csv('healthcare-dataset-stroke-data.csv')
st.dataframe(df)

st.line_chart(df['age'].value_counts().sort_index())

category_df = df['gender'].value_counts(dropna=False).reset_index()
category_df.columns = ['gender','count']
fig = px.pie(category_df, names= 'gender', values = 'count')
st.plotly_chart(fig, use_container_widht=True)

st.write('**3. Visualisasi Data - Tipe Pekerjaan**')
st.bar_chart(df['work_type'].value_counts().sort_index())

#5. Interaktif komponen
st.write('**5. Button**')
st.button('Reset',type= 'primary')
if st.button('say hello'):
    st.write('why hello there')
else:
    st.write('Goodbye')

if st.button('Aloha', type='tertiary'):
    st.write('Ciao')

#6. Checkbox
st.write('**6. Checkbox**')
agree = st.checkbox('I agree')
if agree:
    st.write('Great!')

#7. Multiselect
st.write('**7. Multiselect**')
options = st.multiselect(
    'What is your favorite colors?',
    ['Green','Yellow','Red','Blue'],
    ['Yellow','Red'],

)
st.write('You selected:',options)

#8.slider

st.write('**8. Slider**')
start_tyres, end_tyres = st.select_slider(
    'pilih komponen ban untuk race pekan ini',
    options=[
        'Hyper Soft',
        'Ultra Soft',
        'Super Soft',
        'Soft',
        'Medium',
        'Hard',
        'Super Hard',

    ],
    value=('Hyper Soft','Soft'),
)
st.write('anda memilih', start_tyres,'dan',end_tyres)
#9. Toggle
st.write('**9. Toggle**')
on = st.toggle('Activate feature')
if on:
    st.write('Feature activated!')

#10. Number input 

st.write('**10. Number Input**')
number = st.number_input (
    'Insert a number', value= None, placeholder= 'Type a number...'
)
st.write('the current number is', number)

#11.Data Input
st.write('**11. data Input**')
import datetime 
d = st.date_input(' when is your birthday', datetime.date(1999,9,14))
st.write('your birthday is:', d)


