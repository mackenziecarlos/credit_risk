import streamlit as st

st.title("Modelo de Análisis de Riesgo de Crédito FEMAP")

salario = st.text_input('Salario Mensual',value=3500000,format="{:.2f}")
edad = st.text_input('Edad', value=25, type="default", label_visibility="visible")
ningreso = st.slider('Nivel de Ingreso',1,12,6)
antiguedad = st.slider('Antiguedad',0,20,4)
monto = st.number_input('Monto del Crédito', value=5000000, label_visibility="visible")
cdesc = st.number_input('Capacidad de Descuento', value=0.25, label_visibility="visible",format="%0.1f")
