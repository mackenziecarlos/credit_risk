import streamlit as st

st.title("Modelo de Análisis de Riesgo de Crédito FEMAP")

salario = st.number_input('Salario Mensual',value=3500000,format=",.0f")
edad = st.text_input('Edad', value=25, type="default", label_visibility="visible")
ningreso = st.slider('Nivel de Ingreso',1,6,12)
antiguedad = st.slider('Antiguedad',0,4,20)
monto = st.number_input('Monto del Crédiro', value=5000000, label_visibility="visible",format=",.0f")
cdesc = st.number_input('Monto del Crédiro', value=0.25, label_visibility="visible",format="%0.1f")
