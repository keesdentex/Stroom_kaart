import streamlit as st

st.title("Mijn Bereken App")

# Inputvelden
stroom_links = st.number_input("Stroomsnelheid links", value=0.0)
stroom_rechts = st.number_input("Stroomsnelheid rechts", value=0.0)
stroom_hoek = st.number_input("Hoek van stroom ten opzichte van de wind (rechts positief, links negatief)", value=0.0)
wind_snelheid= st.number_input("Windsnelheid in knopen", value=0.0)

# Actieknop
if st.button("Bereken"):
    resultaat = a + b  # Hier komt jouw berekening
    st.success(f"Het resultaat is: {resultaat}")

