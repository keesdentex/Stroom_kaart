
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Welke baan is sneller bij upwind met stroom?")

# Inputvelden
stroom_links = st.number_input("Stroomsnelheid links", value=0.0, step=0.1, format="%.2f")
stroom_rechts = st.number_input("Stroomsnelheid rechts", value=0.0, step=0.1, format="%.2f")
stroom_hoek = st.number_input("Hoek van stroom t.o.v. wind (rechts positief, links negatief)", value=0.0, step=1.0, format="%.1f")
wind_snelheid = st.number_input("Windsnelheid in knopen", value=0.0, step=0.1, format="%.1f")

# Ik maak de waarden zo dat ik 1 berekening maar hoef te doen
stroom_hoek_abs= abs(stroom_hoek)
if stroom_hoek < 0:
    stroom_rechts, stroom_links = stroom_links, stroom_rechts

# Plaatje maken
width, height = 10, 10
center_x = width/2
center_y = height/2
theta= np.deg2rad(90-stroom_hoek_abs)
m = np.tan(np.deg2rad(90-stroom_hoek))
x_vals = np.array([0, width])
y_vals = center_y + m * (x_vals - center_x)

# Plot maken
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, width)
ax.set_ylim(0, height)

# Lijn tekenen
ax.plot(x_vals, y_vals, color="black", linewidth=1)
ax.set_title(f"Upwind met {stroom_hoek}° stroom ten opzichte van wind")
ax.axis("off")

start_x1, start_x2 = 3, 7      # x-coördinaten van startboeien
start_y = 2                    # y-positie van de startlijn
ax.plot([start_x1, start_x2], [start_y, start_y], 'k--', linewidth=1)  # gestippelde lijn

# Startboeien
ax.plot(start_x1, start_y, 'ro', markersize=8, label="Startboei links")  # rode boei
ax.plot(start_x2, start_y, 'ro', markersize=8, label="Startboei rechts")

# --- Bovenboei toevoegen ---
bovenboei_x = center_x
bovenboei_y = 8
ax.plot(bovenboei_x, bovenboei_y, 'go', markersize=8, label="Bovenboei")  # groene boei


lengte_baan= 100



# Actieknop
if st.button("Bereken"):
    # tijd voor de logica
   
    snelheid_boot= 4
    schijnbare_wind_rechts=np.array([stroom_rechts*np.cos(theta), -wind_snelheid+stroom_rechts*np.sin(theta)])
    schijnbare_wind_rechts_hoek= np.arctan2(schijnbare_wind_rechts[1], schijnbare_wind_rechts[0])
    schijnbare_wind_rechts_hoek = np.rad2deg(schijnbare_wind_rechts_hoek)
    schijnbare_wind_links=np.array([stroom_links*np.cos(theta), -wind_snelheid+stroom_links*np.sin(theta)])
    schijnbare_wind_links_hoek= np.arctan2(schijnbare_wind_links[1], schijnbare_wind_links[0])
    schijnbare_wind_links_hoek = np.rad2deg(schijnbare_wind_links_hoek)

    boot_stuurboord_links_hoek = 135 + schijnbare_wind_links_hoek
    boot_stuurboord_rechts_hoek = 135+ schijnbare_wind_rechts_hoek
    boot_bakboord_links_hoek = 225 + schijnbare_wind_links_hoek
    boot_bakboord_rechts_hoek = 225 + schijnbare_wind_rechts_hoek
    boot_stuurboord_links=np.array([snelheid_boot*np.cos(np.deg2rad(boot_stuurboord_links_hoek))-stroom_links*np.cos(theta), snelheid_boot*np.sin(np.deg2rad(boot_stuurboord_links_hoek))-stroom_links*np.sin(theta)])
    boot_stuurboord_rechts=np.array([snelheid_boot*np.cos(np.deg2rad(boot_stuurboord_rechts_hoek))-stroom_rechts*np.cos(theta), snelheid_boot*np.sin(np.deg2rad(boot_stuurboord_rechts_hoek))-stroom_rechts*np.sin(theta)])
    boot_bakboord_links=np.array([snelheid_boot*np.cos(np.deg2rad(boot_bakboord_links_hoek))-stroom_links*np.cos(theta), snelheid_boot*np.sin(np.deg2rad(boot_bakboord_links_hoek))-stroom_links*np.sin(theta)])
    boot_bakboord_rechts=np.array([snelheid_boot*np.cos(np.deg2rad(boot_bakboord_rechts_hoek))-stroom_rechts*np.cos(theta), snelheid_boot*np.sin(np.deg2rad(boot_bakboord_rechts_hoek))-stroom_rechts*np.sin(theta)])
    # hoeken over de grond
    boot_stuurboord_links_hoek2 = np.rad2deg(np.arctan2(boot_stuurboord_links[1], boot_stuurboord_links[0]))
    boot_stuurboord_rechts_hoek2 = np.rad2deg(np.arctan2(boot_stuurboord_rechts[1], boot_stuurboord_rechts[0]))
    boot_bakboord_links_hoek2 = np.rad2deg(np.arctan2(boot_bakboord_links[1], boot_bakboord_links[0]))
    boot_bakboord_rechts_hoek2 = np.rad2deg(np.arctan2(boot_bakboord_rechts[1], boot_bakboord_rechts[0]))

    snelheid_boot_stuurboord_links=np.linalg.norm(boot_stuurboord_links)
    snelheid_boot_stuurboord_rechts=np.linalg.norm(boot_stuurboord_rechts)
    snelheid_boot_bakboord_links=np.linalg.norm(boot_bakboord_links)
    snelheid_boot_bakboord_rechts=np.linalg.norm(boot_bakboord_rechts)
    # driehoek berekenen links
    hoek_links= 180-boot_bakboord_rechts_hoek2+ stroom_hoek_abs
    lengte_bakboord_links= lengte_baan*np.sin(np.deg2rad(90-stroom_hoek_abs))/np.sin(np.deg2rad(hoek_links))
    tijd_links_stroomlijn= lengte_bakboord_links/snelheid_boot_bakboord_links
    intersectie_links= [tijd_links_stroomlijn* boot_bakboord_links[0], tijd_links_stroomlijn*boot_bakboord_links[1]]

    # driehoek berekenen rechts
    hoek_rechts= 180-boot_bakboord_links_hoek2+ stroom_hoek_abs
    lengte_bakboord_rechts= lengte_baan*np.sin(np.deg2rad(90-stroom_hoek_abs))/np.sin(np.deg2rad(hoek_rechts))
    tijd_rechts_stroomlijn= -lengte_bakboord_rechts/snelheid_boot_bakboord_rechts
    intersectie_rechts= [tijd_rechts_stroomlijn* boot_bakboord_rechts[0], tijd_rechts_stroomlijn*boot_bakboord_rechts[1]]

    #tweede driehoek berekenen links
    vector_links= np.array([intersectie_links[0], intersectie_links[1]-2*lengte_baan])
    hoek_vector_links= np.arctan2(vector_links[1], vector_links[0])
    
    hoek_vector_links = np.rad2deg(hoek_vector_links)
    afstand_links= np.linalg.norm(vector_links)
    hoek_boot_links1= 180-boot_bakboord_links_hoek2 + boot_stuurboord_links_hoek2
    hoek_boot_links2= 180-boot_stuurboord_links_hoek2 + hoek_vector_links
    hoek_boot_link3=180 - hoek_boot_links1 - hoek_boot_links2

    afstand_tegenover_hoek_links2= afstand_links * np.sin(np.deg2rad(hoek_boot_links2))/ np.sin(np.deg2rad(hoek_boot_links1))
    afstand_tegenover_hoek_links3= afstand_links * np.sin(np.deg2rad(hoek_boot_link3))/ np.sin(np.deg2rad(hoek_boot_links1))
    tijd_links_naar_stuurboord_layline= afstand_tegenover_hoek_links2/snelheid_boot_bakboord_links
    tijd_links_naar_boei_via_stuurboord_layline= afstand_tegenover_hoek_links3/snelheid_boot_stuurboord_links
    totale_tijd_links= tijd_links_stroomlijn + tijd_links_naar_stuurboord_layline + tijd_links_naar_boei_via_stuurboord_layline
    
    # tweede driehoek berekenen rechts
    vector_rechts= np.array([intersectie_rechts[0], intersectie_rechts[1]+2*lengte_baan])
    hoek_vector_rechts= np.arctan2(vector_rechts[1], vector_rechts[0])
    hoek_vector_rechts = np.rad2deg(hoek_vector_rechts)

    afstand_rechts= np.linalg.norm(vector_rechts)
    hoek_boot_rechts1= 180-boot_bakboord_rechts_hoek2 + boot_stuurboord_rechts_hoek2
    hoek_boot_rechts2= hoek_vector_rechts- boot_stuurboord_rechts_hoek2
    hoek_boot_rechts3=180 - hoek_boot_rechts1 - hoek_boot_rechts2
    #st.write(f'snelheden boot rechts: {snelheid_boot_bakboord_rechts}, {snelheid_boot_stuurboord_rechts}')
    #st.write(f'snelheden boot links: {snelheid_boot_bakboord_links}, {snelheid_boot_stuurboord_links}')
    afstand_tegenover_hoek_rechts3= afstand_rechts * np.sin(np.deg2rad(hoek_boot_rechts2))/ np.sin(np.deg2rad(hoek_boot_rechts1))
    afstand_tegenover_hoek_rechts2= afstand_rechts * np.sin(np.deg2rad(hoek_boot_rechts3))/ np.sin(np.deg2rad(hoek_boot_rechts1))
    tijd_rechts_naar_bakboord_layline= afstand_tegenover_hoek_rechts2/snelheid_boot_stuurboord_rechts
    tijd_rechts_naar_stroomlijn_via_stuurboord_layline= afstand_tegenover_hoek_rechts3/snelheid_boot_bakboord_rechts
    totale_tijd_rechts= -tijd_rechts_stroomlijn + tijd_rechts_naar_bakboord_layline + tijd_rechts_naar_stroomlijn_via_stuurboord_layline
    # st.write(f'afstanden links: {lengte_bakboord_links}, {afstand_tegenover_hoek_links2}, {afstand_tegenover_hoek_links3}')
    # st.write(f'afstanden rechts: {lengte_bakboord_rechts}, {afstand_tegenover_hoek_rechts2}, {afstand_tegenover_hoek_rechts3}')
    # st.write(f'Tijd links: {totale_tijd_links:.2f} uur, tijd rechts: {totale_tijd_rechts:.2f} uur')
    # st.write(f'tijden links: {tijd_links_stroomlijn:.2f}, {tijd_links_naar_stuurboord_layline:.2f}, {tijd_links_naar_boei_via_stuurboord_layline:.2f}')
    # st.write(f'tijden rechts: {tijd_rechts_stroomlijn:.2f}, {tijd_rechts_naar_bakboord_layline:.2f}, {tijd_rechts_naar_stroomlijn_via_stuurboord_layline:.2f}')
    if stroom_hoek >=0:
        teken_stroom=True
    else:
        teken_stroom=False
    
    if  totale_tijd_links < totale_tijd_rechts:
        procent_snellere_baan= (totale_tijd_rechts - totale_tijd_links)/totale_tijd_rechts * 100
        st.write(f"De linkse baan is {procent_snellere_baan:.2f}% sneller dan de rechtse baan.")
    else: 
        procent_snellere_baan= (totale_tijd_links - totale_tijd_rechts)/totale_tijd_links * 100
        st.write(f"De rechtse baan is {procent_snellere_baan:.2f}% sneller dan de linkse baan.")
    
    # Resultaat tonen
    st.pyplot(fig)





