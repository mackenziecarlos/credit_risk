import streamlit as st
import numpy as np
import pickle
import pandas as pd
from xgboost import XGBClassifier
import plotly.graph_objects as go
st.title("Modelo de Análisis de Riesgo de Crédito FEMAP")
st.divider()
salario = st.number_input('Salario Mensual')
st.write("{:0,.0f}".format(float(salario)))
edad = st.text_input('Edad', value=25, type="default", label_visibility="visible")
antiguedad = st.slider('Antiguedad del Asociado (Años)',0,20,2)
plazo = st.slider('Plazo en Meses',0,180,12)
gasto_financiero = st.number_input('Gasto Financiero')
st.write("{:0,.0f}".format(float(gasto_financiero)))
st.markdown(''':red[Gasto Financiero:] :gray[Valor de todas las cuotas de los créditos activos inluyendo la futura cuota del nuevo crédito de ser aprobado]''')
cap_des = st.slider('Capacidad de Descuento %',0,100,25)
capital = st.number_input('Monto del Credito',label_visibility="visible")
st.write("{:0,.0f}".format(float(capital)))
empresa = st.selectbox("Empresa",('Mapfre Generales','Mapfre Vida','Andiasistencia','Cesvicolombia','FEMAP','Solunion','Otros'))
municipio = st.selectbox("Municipio",('Bogota','Medellin','Cali','Otros'))
destino = st.selectbox("Destino",('Polizas e Impuestos','Promocion','Extraordinario','Prima','Recreacion','Compra de Cartera','Otros'))
garantia = st.radio("Tipo de Garantia",["Real", "Personal"])
tgarantia = st.radio("Subtipo de Garantia",["Pagare", "Poliza Cumplimiento","Pignoracion","Hipotecaria"])

mun_index = {"Bogota": 0,"Medellin": 1,"Cali": 2,"Otros":30}
mun_index_v = mun_index[municipio]
emp_index = {'Mapfre Generales':0,'Mapfre Vida':1,'Andiasistencia':2,'Cesvicolombia':3,'FEMAP':4,'Solunion':5,'Otros':7}
emp_index_v = emp_index[empresa]
NOMBREDEST_index ={'Polizas e Impuestos':1,'Promocion':2,'Extraordinario':4,'Prima':5,'Recreacion':6,'Compra de Cartera':7,'Otros':8}
NOMBREDEST_index_v = NOMBREDEST_index[destino]
TIPOGARANT_index ={"Real":1, "Personal":0}
TIPOGARANT_index_v=TIPOGARANT_index[garantia]
NOMBREGARA_index= {"Pagare":0, "Poliza Cumplimiento":1,"Pignoracion":2,"Hipotecaria":3}
NOMBREGARA_index_v=NOMBREGARA_index[tgarantia]
load_xg=pickle.load(open('credit_risk_model2.pkl','rb'))
if st.button("Calcular Riesgo de Crédito"):
  ind_cap = capital/salario
  plazo=float(plazo)
  capital=float(capital)
  edad=float(edad)
  antiguedad=float(antiguedad)
  salario=float(salario)
  gasto_financiero=float(gasto_financiero)
  cap_des=float(cap_des)
  ind_cap=float(ind_cap)
  mun_index_v=float(mun_index_v)
  emp_index_v=float(emp_index_v)
  NOMBREDEST_index_v=float(NOMBREDEST_index_v)
  TIPOGARANT_index_v=float(TIPOGARANT_index_v)
  NOMBREGARA_index_v=float(NOMBREGARA_index_v)
  vp=[[cap_des,salario,mun_index_v,plazo,gasto_financiero,emp_index_v,NOMBREDEST_index_v,edad,antiguedad,ind_cap,TIPOGARANT_index_v,capital,NOMBREGARA_index_v]]
  if (load_xg.predict(np.array(vp))==1):
    st.markdown(''':red[**Solicitud Credito Rechazada**]''')
  else:
    st.markdown(''':green[**Solicitud Credito Aprobada**]''')
  p2=load_xg.predict_proba(np.array(vp))[0, 1]
  fig = go.Figure(go.Indicator(
      mode = "gauge+number",
      number = {'suffix': "% Probabilidad de Mora", 'font': {'size': 20}},
      value = p2*100,
      domain = {'x': [0,1], 'y': [0,1]},
      gauge = {
          'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
          'bar': {'color': "darkblue"},
          'bgcolor': "white",
          'borderwidth': 2,
          'bordercolor': "gray",
          'steps': [
              {'range': [0, 20], 'color': 'green'},
              {'range': [20, 40], 'color': 'lightgreen'},
              {'range': [40, 60], 'color': 'yellow'},
              {'range': [60,80], 'color': 'orange'},
              {'range': [80,100], 'color': 'red'}],
          }))
  
  fig.update_layout(
      font={'color': "black", 'family': "Arial"},
      xaxis={'showgrid': False, 'range':[-1,1]},
      yaxis={'showgrid': False, 'range':[0,1]},
      # plot_bgcolor='rgba(0,0,0,0)'
      )
  st.plotly_chart(fig, use_container_width=True)
  if st.button("Realizar Otro Analisis"):
    st.rerun()


  

 
