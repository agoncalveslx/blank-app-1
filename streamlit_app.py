import streamlit as st

st.title("Sistema de Validação de Decisão")

i1 = st.selectbox("Inconsistência de identidade", ["Low", "Medium", "High"])
i6 = st.selectbox("Conflito entre fontes", ["Low", "Medium", "High"])

if st.button("Gerar decisão"):
    if i1 == "High" and i6 == "High":
        st.error("Escalate (Red)")
    elif i1 == "Medium" or i6 == "Medium":
        st.warning("Monitor (Amber)")
    else:
        st.success("Dismiss (Green)")

st.write("Validação pelo utilizador: confirmar ou alterar a decisão.")
