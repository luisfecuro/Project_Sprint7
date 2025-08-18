# Librerias
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

df = pd.read_csv("vehicles_us.csv", sep=",")

df['is_4wd'] = df['is_4wd'].fillna(0)
df['is_4wd'] = df['is_4wd'].astype(bool)

df['paint_color'] = df['paint_color'].fillna('unknown')
df['cylinders'] = df['cylinders'].fillna('unknown')
df['brand'] = df['model'].str.split().str[0]
df['odometer'] = df['odometer'].fillna('unknown')
df['model_year'] = df['model_year'].fillna('unknown')

# Pagina web
st.title('Concesionario')

st.header('Informacion por marca', divider='gray')

brands = df['brand'].unique()
brand_selected = st.selectbox(
    'Seleccione la marca en interes:', sorted(brands), key='brands1')

cols = []

for col in df.columns:
    if col not in ['model', 'brand']:
        cols.append(col)

show_cols = st.multiselect('Seleccione la informacion a mostrar', sorted(cols))

if not show_cols:
    st.write('Seleccione la informacion deseada a ver por vehiculo')
else:

    show_table = df[df['brand'] == brand_selected][['model'] + show_cols]

    st.dataframe(show_table)

st.header('Tipos de vehiculo por marca', divider='gray')

brands_selected2 = st.multiselect(
    'Seleccione las marcas de la cual desea ver los tipos de vehiculo que tiene', sorted(
        brands), key='brands2'
)

df_hist = df[df['brand'].isin(brands_selected2)]

fig_1 = px.histogram(df_hist,
                     x='brand',
                     color='type',
                     barmode='stack')


st.plotly_chart(fig_1)

for brand in brands_selected2:

    brand_interested = df_hist[df_hist['brand'] == brand]

    moda = brand_interested['type'].mode()[0]
    cantidad = brand_interested['type'].value_counts()[moda]

    st.metric(label=f'La marca {brand} tiene en su mayoria',
              value=moda, delta=f'{cantidad} vehiculos')

st.header('Comportamiento de los vehiculos con el paso del tiempo', divider='gray')

brands_selected3 = st.selectbox(
    'Seleccione la marca de la cual quiere ver su comportamiento en el tiempo', sorted(df['brand'].unique()))

df_time = df[df['brand'] == brands_selected3]

col1, col2 = st.columns(2)

with col1:
    st.subheader('Condicion de los vehiculos')
    fig_2 = px.histogram(df_time,
                         x='model_year',
                         color='condition',
                         barmode='group',
                         category_orders={"condition": [
                             "fair", "good", "excellent", "like new", "new", "salvage"]},
                         color_discrete_map={'new': '#2ECC71',
                                             'like new': '#58D68D',
                                             'excellent': '#3498DB',
                                             'good': '#5DADE2',
                                             'fair': '#E67E22',
                                             'salvage': '#E74C3C'})
    st.plotly_chart(fig_2)

with col2:
    st.subheader('Precio de los vehiculos')
    fig_3 = px.histogram(df_time,
                         x='model_year',
                         y='price',
                         )
    st.plotly_chart(fig_3)
