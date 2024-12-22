import streamlit as st
import numpy as np
import pickle

st.title("Modelo de Análisis de Riesgo de Crédito FEMAP")
st.divider()
salario = st.number_input('Salario Mensual')
st.write("{:0,.0f}".format(float(salario)))
edad = st.text_input('Edad', value=25, type="default", label_visibility="visible")
plazo = st.slider('Plazo en Meses',0,180,12)
gasto_financiero = st.number_input('Gasto Financiero')
st.write("{:0,.0f}".format(float(gasto_financiero)))
st.markdown(''':red[Gasto Financiero:] :gray[Valor de todas las cuotas de los créditos activos inluyendo la futura cuota del nuevo crédito de ser aprobado]''')
cap_des = st.slider('Capacidad de Descuento %',0,50,25)
capital = st.number_input('Monto del Credito',label_visibility="visible")
st.write("{:0,.0f}".format(float(capital)))
empresa = st.selectbox("Empresa",('Mapfre Generales','Mapfre Vida','Andiasistencia','Cesvicolombia','FEMAP','Solunion','Otros'))
municipio = st.selectbox("Municipio",('Bogota','Medellin','Cali','Otros'))
destino = st.selectbox("Destino",('Polizas e Impuestos','Promocion','Extraordinario','Prima',
                       'Recreacion','Compra de Cartera','otros'))
if (municipio='Bogota'):
  mun_index=0
if (municipio='Medellin'):
  mun_index=1
if (municipio='Cali'):
  mun_index=2
if (municipio='Otros'):
  mun_index=30  
if (empresa='Mapfre Generales'):
  emp_index=0
if (empresa='Mapfre Vida'):
  emp_index=1
if (empresa='Andiasistencia'):
  emp_index=2
if (empresa='Cesvicolombia'):
  emp_index=3
if (empresa='FEMAP'):
  emp_index=4
if (empresa='Solunion'):
  emp_index=5
if (empresa='Otros'):
  emp_index=7  
garantia = st.radio("Tipo de Garantia",["Real", "Personal"])
if st.button("Calcular Riesgo de Crédito"):
  ind_cap = capital/salario
  st.write("{:0,.2f}".format(float(ind_cap)))
  vp=[[cap_des,salario,mun_index,plazo,gasto_financiero,emp_index,NOMBREDEST_index,EDAD,ANTIGUEDAD,IND_CAP,TIPOGARANT_index,CAPITALINI,NOMBREGARA_index]]
