import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap
import numpy as np
import pandas as pd

# --- App Setup ---
st.set_page_config(page_title="Sylhet Fugitive Movement Predictor", layout="centered")
st.title("🔍 Sylhet Fugitive Movement Prediction Framework")
st.markdown("""
This prototype visualizes **likely fugitive positions and movements** around Sylhet.  
Click any point on the map to simulate prediction probabilities.  
""")

# --- Initialize session state ---
if "selected_point" not in st.session_state:
    st.session_state.selected_point = None
if "probabilities" not in st.session_state:
    st.session_state.probabilities = None
if "heatmap_points" not in st.session_state:
    st.session_state.heatmap_points = None

# --- Create base map centered on Sylhet ---
m = folium.Map(location=[24.8949, 91.8687], zoom_start=13, tiles="CartoDB positron")

# --- Map click event ---
st.markdown("### 🗺️ Select a Location")
map_data = st_folium(m, width=750, height=500)

# --- Process click ---
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    # Only recalculate if user selected a new location
    if st.session_state.selected_point != (lat, lon):
        st.session_state.selected_point = (lat, lon)

        # Generate fixed probabilities and heatmap data for this point
        directions = ["North", "South", "East", "West"]
        probs = np.random.dirichlet(np.ones(4), size=1)[0]
        st.session_state.probabilities = pd.DataFrame({
            "Direction": directions,
            "Probability": probs
        })

        # Generate simulated nearby points for heatmap
        st.session_state.heatmap_points = [
            [
                lat + np.random.uniform(-0.01, 0.01),
                lon + np.random.uniform(-0.01, 0.01),
                np.random.uniform(0.3, 1.0),
            ]
            for _ in range(80)
        ]

# --- Display Results ---
if st.session_state.selected_point:
    lat, lon = st.session_state.selected_point
    st.success(f"📍 Selected location: {lat:.5f}, {lon:.5f}")

    st.markdown("### 📊 Predicted Movement Probabilities")
    st.bar_chart(st.session_state.probabilities.set_index("Direction"))

    # Create map with marker and saved heatmap
    m = folium.Map(location=[lat, lon], zoom_start=14, tiles="CartoDB positron")
    folium.Marker([lat, lon], popup="Selected Point", icon=folium.Icon(color="red")).add_to(m)
    HeatMap(st.session_state.heatmap_points, radius=18, blur=25, max_zoom=13).add_to(m)

    st.markdown("### 🔥 Probability Heatmap (Stable until new click)")
    st_folium(m, width=750, height=500)
else:
    st.info("Click on the map above to generate probability predictions.")
