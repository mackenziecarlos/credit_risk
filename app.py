import streamlit as st
import numpy as np
import pickle

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
cap_des = st.slider('Capacidad de Descuento %',0,50,25)
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
NOMBREGARA_index_v= {"Pagare":0, "Poliza Cumplimiento":1,"Pignoracion":2,"Hipotecaria":3}
load_xg=pickle.load(open('credit_risk_model.pkl','rb'))
if st.button("Calcular Riesgo de Crédito"):
  ind_cap = capital/salario
  st.write("{:0,.2f}".format(float(ind_cap)))
  vp=[[cap_des,salario,mun_index_v,plazo,gasto_financiero,emp_index_v,NOMBREDEST_index_v,edad,antiguedad,ind_cap,TIPOGARANT_index_v,capital,NOMBREGARA_index_v]]
  if (load_xg.predict(vp)==1):
    p1='Solicitud Credito Rechazada'
  else:
    p1='Solicitud Credito Aprobada'
  p2=load_xg.predict_proba(vp)[0, 1]
  st.write('''# p1 ''')
  st.write('La probabilidad de incumplimiento futuro del asociado es del',"{:0,.1f}%".format(float(p2*100)))
