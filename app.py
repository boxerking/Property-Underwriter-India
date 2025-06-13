import streamlit as st
from utils.geo_utils import get_elevation
from utils.fire_utils import get_fire_events
from utils.rainfall_utils import get_rainfall
from utils.seismic_flood_utils import is_in_flood_zone, is_in_seismic_zone
from utils.emergency_utils import estimate_response_time
from utils.pdf_utils import generate_pdf
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Property Risk Underwriter - India", layout="wide")
st.title("🏠 AI Tool for Property Underwriting - India")

lat = st.number_input("Latitude", value=19.0760)
lon = st.number_input("Longitude", value=72.8777)

if st.button("Analyze Risk"):
    elevation = get_elevation(lat, lon)
    rainfall = get_rainfall(lat, lon)
    flood_risk = is_in_flood_zone(lat, lon)
    seismic_risk = is_in_seismic_zone(lat, lon)
    fire_data = get_fire_events(lat, lon)
    response_time = estimate_response_time(lat, lon)

    results = {
        "Latitude": lat,
        "Longitude": lon,
        "Elevation (m)": elevation,
        "Annual Rainfall (mm)": rainfall,
        "Flood Zone": flood_risk,
        "Seismic Zone": seismic_risk,
        "Nearby Fire Incidents": fire_data,
        "Fire Response Time (min)": response_time
    }

    st.success("Analysis Complete ✅")
    st.json(results)

    st.subheader("Map View")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    folium.Marker([lat, lon], tooltip="Risk Location").add_to(m)
    st_folium(m, width=700, height=500)

    if st.button("Download PDF Report"):
        generate_pdf(results)
        st.success("PDF Generated Successfully")