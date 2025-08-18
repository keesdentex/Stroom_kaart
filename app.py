import streamlit as st

st.title("Mijn Bereken App")

# Inputvelden
a = st.number_input("Voer het eerste getal in", value=0.0)
b = st.number_input("Voer het tweede getal in", value=0.0)

# Actieknop
if st.button("Bereken"):
    resultaat = a + b  # Hier komt jouw berekening
    st.success(f"Het resultaat is: {resultaat}")
