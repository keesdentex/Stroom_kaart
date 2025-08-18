import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Mijn Bereken App")

# Inputvelden
stroom_links = st.number_input("Stroomsnelheid links", value=0.0)
stroom_rechts = st.number_input("Stroomsnelheid rechts", value=0.0)
stroom_hoek = st.number_input("Hoek van stroom ten opzichte van de wind (rechts positief, links negatief)", value=0.0)
wind_snelheid= st.number_input("Windsnelheid in knopen", value=0.0)

# Plaatje maken
width, height = 10, 10
center_x = width/2
center_y = height/2
theta= np.deg2rad(stroom_hoek)
m = np.tan(theta)
x_vals = np.array([0, width])
y_vals = center_y + m * (x_vals - center_x)

# Plot maken
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.axhline(center_y, color="gray", linestyle="--", alpha=0.3)
ax.axvline(center_x, color="gray", linestyle="--", alpha=0.3)

# Lijn tekenen
ax.plot(x_vals, y_vals, color="blue", linewidth=2)
ax.set_title(f"Lijn door het midden met {stroom_hoek}° rotatie")

# Centerpunt markeren
ax.plot(center_x, center_y, 'ro')




# Actieknop
if st.button("Bereken"):
    resultaat = stroom_links + stroom_rechts  # Hier komt jouw berekening
    st.success(f"Het resultaat is: {resultaat}")
    st.pyplot(fig)




