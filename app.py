import streamlit as st

st.title("Modelo de Análisis de Riesgo de Crédito FEMAP")

salario = st.slider('Salario Mensual',1000000,3500000,20000000)
edad = st.text_input('Edad', value=25, type="default", label_visibility="visible")
ningreso = st.slider('Nivel de Ingreso',1,6,12)
antiguedad = st.slider('Nivel de Ingreso',0,4,20)
monto = st.text_input('Monto del Crédiro', value=5000000, type="default", label_visibility="visible")
cdesc = st.slider('cap_des',0,0.25,0.50)
