import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap
import numpy as np
import pandas as pd

# --- App Title and Description ---
st.set_page_config(page_title="Sylhet Fugitive Movement Predictor", layout="centered")
st.title("🔍 Sylhet Fugitive Movement Prediction Framework")
st.markdown("""
This prototype helps visualize **likely fugitive positions and movements** around Sylhet.
Click any point on the map to simulate prediction probabilities.
""")

# --- Create Folium Map Centered on Sylhet ---
m = folium.Map(location=[24.8949, 91.8687], zoom_start=13, tiles="CartoDB positron")

# --- Show the Map and Capture Clicks ---
st.markdown("### 🗺️ Select a Location")
map_data = st_folium(m, width=750, height=500)

# --- If user clicked on map ---
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    st.success(f"📍 Selected location: {lat:.5f}, {lon:.5f}")

    # --- Simulate directional probability prediction ---
    directions = ["North", "South", "East", "West"]
    probs = np.random.dirichlet(np.ones(4), size=1)[0]
    df = pd.DataFrame({"Direction": directions, "Probability": probs})

    st.markdown("### 📊 Predicted Movement Probabilities")
    st.bar_chart(df.set_index("Direction"))

    # --- Generate random nearby points to simulate probability zones ---
    points = [
        [
            lat + np.random.uniform(-0.01, 0.01),
            lon + np.random.uniform(-0.01, 0.01),
            np.random.uniform(0.3, 1.0),
        ]
        for _ in range(80)
    ]

    # --- Add marker for the clicked location ---
    m = folium.Map(location=[lat, lon], zoom_start=14, tiles="CartoDB positron")
    folium.Marker([lat, lon], popup="Selected Point", icon=folium.Icon(color="red")).add_to(m)

    # --- Add simulated heatmap layer ---
    HeatMap(points, radius=18, blur=25, max_zoom=13).add_to(m)

    st.markdown("### 🔥 Probability Heatmap (Simulated)")
    st_folium(m, width=750, height=500)

else:
    st.info("Click on the map above to generate probability predictions.")
