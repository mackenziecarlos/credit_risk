import streamlit as st

st.title("Modelo de Análisis de Riesgo de Crédito FEMAP")
st.divider()
salario = st.number_input('Salario Mensual')
st.write("{:0,.0f}".format(float(salario)))
edad = st.text_input('Edad', value=25, type="default", label_visibility="visible")
plazo = st.slider('Plazo en Meses',0,180,12)
gasto_financiero = st.number_input('Gasto Financiero')
st.write("{:0,.0f}".format(float(gasto_financiero)))
st.markdown('''
    :red[Gasto Financiero:] :black[Valor de todas las cuotas de los créditos activos inluyendo la futura cuota del nuevo crédito de ser aprobado]''')
cap_des = st.slider('Capacidad de Descuento %',0,50,25)
capital = st.number_input('Monto del Credito',label_visibility="visible")
st.write("{:0,.0f}".format(float(capital)))
ind_cap = capital/salario
empresa = st.selectbox('Mapfre Generales','Mapfre Vida','Andiasistencia','Cesvicolombia','FEMAP','Solunion','Otros')
municipio = st.selectbox('Bogota','Medellin','Cali','Otros')
destino = st.selectbox('Polizas e Impuestos','Promocion','Extraordinario','Prima',
                       'Recreacion','Compra de Cartera','otros')
garantia = st.radio("Tipo de Garantia",
    ["Real", "***Personal***", "Documentary :movie_camera:"],
    captions=[
        "Laugh out loud.",
        "Get the popcorn.",
        "Never stop learning.",
    ],
)
