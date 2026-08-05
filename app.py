import streamlit as st
import numpy as np
import pickle
import pandas as pd
from xgboost import XGBClassifier
import plotly.graph_objects as go

st.title("Modelo de Análisis de Riesgo de Crédito")
st.divider()

salario = st.number_input('Salario Mensual', min_value=0.0, value=0.0)
st.write("{:0,.0f}".format(float(salario)))

edad = st.text_input('Edad', value="25", type="default", label_visibility="visible")
antiguedad = st.slider('Antiguedad del Asociado (Años)', 0, 20, 2)
plazo = st.slider('Plazo en Meses', 0, 180, 12)

gasto_financiero = st.number_input('Gasto Financiero', min_value=0.0, value=0.0)
st.write("{:0,.0f}".format(float(gasto_financiero)))

st.markdown(''':red[Gasto Financiero:] :gray[Valor de todas las cuotas de los créditos activos incluyendo la futura cuota del nuevo crédito de ser aprobado]''')

cap_des = st.slider('Capacidad de Descuento %', 0, 100, 25)
capital = st.number_input('Monto del Credito', min_value=0.0, value=0.0, label_visibility="visible")
st.write("{:0,.0f}".format(float(capital)))

empresa = st.selectbox("Empresa", ('Mapfre Generales', 'Mapfre Vida', 'Andiasistencia', 'Cesvicolombia', 'FEMAP', 'Solunion', 'Otros'))
municipio = st.selectbox("Municipio", ('Bogota', 'Medellin', 'Cali', 'Otros'))
destino = st.selectbox("Destino", ('Polizas e Impuestos', 'Promocion', 'Extraordinario', 'Prima', 'Recreacion', 'Compra de Cartera', 'Otros'))
garantia = st.radio("Tipo de Garantia", ["Real", "Personal"])
tgarantia = st.radio("Subtipo de Garantia", ["Pagare", "Poliza Cumplimiento", "Pignoracion", "Hipotecaria"])

# Mapeos
mun_index = {"Bogota": 0, "Medellin": 1, "Cali": 2, "Otros": 30}
emp_index = {'Mapfre Generales': 0, 'Mapfre Vida': 1, 'Andiasistencia': 2, 'Cesvicolombia': 3, 'FEMAP': 4, 'Solunion': 5, 'Otros': 7}
NOMBREDEST_index = {'Polizas e Impuestos': 1, 'Promocion': 2, 'Extraordinario': 4, 'Prima': 5, 'Recreacion': 6, 'Compra de Cartera': 7, 'Otros': 8}
TIPOGARANT_index = {"Real": 1, "Personal": 0}
NOMBREGARA_index = {"Pagare": 0, "Poliza Cumplimiento": 1, "Pignoracion": 2, "Hipotecaria": 3}

# Carga del modelo (Manejo de errores si falla el pickle)
try:
    load_xg = pickle.load(open('credit_risk_model2.pkl', 'rb'))
except Exception as e:
    st.error(f"Error al cargar el modelo PKL. Asegúrate de tener instalada la versión de XGBoost con la que se entrenó el modelo. Detalle: {e}")
    st.stop()

if st.button("Calcular Riesgo de Crédito"):
    if salario <= 0:
        st.warning("El salario mensual debe ser mayor a 0 para realizar el cálculo.")
    else:
        # Validación básica de edad
        try:
            val_edad = float(edad)
        except ValueError:
            st.error("Por favor ingresa un valor numérico válido para la Edad.")
            st.stop()

        ind_cap = capital / salario
        
        vp = [[
            float(cap_des),
            float(salario),
            float(mun_index[municipio]),
            float(plazo),
            float(gasto_financiero),
            float(emp_index[empresa]),
            float(NOMBREDEST_index[destino]),
            val_edad,
            float(antiguedad),
            float(ind_cap),
            float(TIPOGARANT_index[garantia]),
            float(capital),
            float(NOMBREGARA_index[tgarantia])
        ]]
        
        # Predicción
        pred = load_xg.predict(np.array(vp))[0]
        if pred == 1:
            st.markdown(''':red[**Solicitud Credito Rechazada**]''')
        else:
            st.markdown(''':green[**Solicitud Credito Aprobada**]''')
            
        p2 = load_xg.predict_proba(np.array(vp))[0, 1]
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            number = {'suffix': "% Probabilidad de Mora", 'font': {'size': 20}},
            value = p2 * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
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
                    {'range': [60, 80], 'color': 'orange'},
                    {'range': [80, 100], 'color': 'red'}
                ],
            }
        ))
        
        fig.update_layout(
            font={'color': "black", 'family': "Arial"},
            xaxis={'showgrid': False, 'range': [-1, 1]},
            yaxis={'showgrid': False, 'range': [0, 1]}
        )
        st.plotly_chart(fig, use_container_width=True)
