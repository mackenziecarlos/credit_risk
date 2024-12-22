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
NOMBREGARA_index= {"Pagare":0, "Poliza Cumplimiento":1,"Pignoracion":2,"Hipotecaria":3}
NOMBREGARA_index_v=NOMBREGARA_index[tgarantia]
load_xg=pickle.load(open('credit_risk_model.pkl','rb'))
if st.button("Calcular Riesgo de Crédito"):
  ind_cap = capital/salario
  st.write("{:0,.2f}".format(float(ind_cap)))
  plazo=float(plazo)
  capital=float(capital)
  edad=int(edad)
  antiguedad=int(antiguedad)
  salario=float(salario)
  gasto_financiero=float(gasto_financiero)
  cap_des=float(cap_des)
  ind_cap=float(ind_cap)
  mun_index_v=int(mun_index_v)
  emp_index_v=int(emp_index_v)
  NOMBREDEST_index_v=int(NOMBREDEST_index_v)
  TIPOGARANT_index_v=int(TIPOGARANT_index_v)
  NOMBREGARA_index_v=int(NOMBREGARA_index_v)
  vp=[[cap_des,salario,mun_index_v,plazo,gasto_financiero,emp_index_v,NOMBREDEST_index_v,edad,antiguedad,ind_cap,TIPOGARANT_index_v,capital,NOMBREGARA_index_v]]
  st.write(load_xg.predict(np.array(vp)))
  if (load_xg.predict(np.array(vp))==1):
    p1='Solicitud Credito Rechazada'
  else:
    p1='Solicitud Credito Aprobada'
  p2=load_xg.predict_proba(np.array(vp))[0, 1]
  st.write('''# p1 ''')
  st.write('La probabilidad de incumplimiento futuro del asociado es del',"{:0,.1f}%".format(float(p2*100)))
  st.divider()
  

  if "reset" not in st.session_state:
      st.session_state.reset = False
  
  with st.container():
      default_values = {"Salario Mensual": 0, "Edad": 25, "Antiguedad del Asociado (Años)": 2, "Plazo en Meses": 12,
                       'Gasto Financiero':0,'Capacidad de Descuento %':25}
  
      inp1 = default_values["Salario Mensual"] if st.session_state.reset else st.session_state.get("Salario Mensual", default_values["Salario Mensual"])
      inp2 = default_values["Edad"] if st.session_state.reset else st.session_state.get("Edad", default_values["Edad"])
      inp3 = default_values["Antiguedad del Asociado (Años)"] if st.session_state.reset else st.session_state.get("Antiguedad del Asociado (Años)", default_values["Antiguedad del Asociado (Años)"])
      inp4 = default_values["Plazo en Meses"] if st.session_state.reset else st.session_state.get("Plazo en Meses", default_values["Plazo en Meses"])
      inp5 = default_values["Gasto Financiero"] if st.session_state.reset else st.session_state.get("Gasto Financiero", default_values["Gasto Financiero"])
      inp6 = default_values["Capacidad de Descuento %"] if st.session_state.reset else st.session_state.get("Capacidad de Descuento %", default_values["Capacidad de Descuento %"])
      
      st.session_state.inp1 = st.number_input("Salario Mensual", value=inp1)
      st.session_state.inp2 = st.text_input("Edad", value=inp2)
      st.session_state.inp3 = st.slider("Antiguedad del Asociado (Años)", value=inp3)
      st.session_state.inp4 = st.slider("Plazo en Meses", value=inp4)
      st.session_state.inp5 = st.number_input("Gasto Financiero", value=inp5)
      st.session_state.inp6 = st.slider("Capacidad de Descuento %", value=inp6)
    
  
      # Reset button
      if st.button("Reset values"):
          st.session_state.reset = True  # Mark reset as True if button is pressed
          st.experimental_rerun()  # Rerun the script
      else:
          st.session_state.reset = False  # Reset the reset flag
