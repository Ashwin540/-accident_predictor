import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pydeck as pdk
from pyproj import Transformer

# ✅ Page config and background design
st.set_page_config(page_title="Accident-Prone Zone Predictor", layout="wide")

# ✅ Stylish background and UI
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #e0f7fa, #80deea);
        background-attachment: fixed;
    }
    input, textarea, select, button {
        border-radius: 10px !important;
    }
    .stButton>button {
        background-color: #00acc1;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00838f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------
# Main App - Accident Zone Predictor
# -----------------------------------------------

# Load and prepare dataset
df = pd.read_csv('data/dataset.csv')
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

transformer = Transformer.from_crs("epsg:27700", "epsg:4326")
df[['longitude', 'latitude']] = df.apply(
    lambda row: pd.Series(transformer.transform(row['grid_ref:_easting'], row['grid_ref:_northing'])),
    axis=1
)

st.title("\U0001F6A6 Real-Time Accident Risk Check Based on History")

geolocator = Nominatim(user_agent="accident_predictor")

st.subheader("\U0001F50D Search Location")
search_query = st.text_input("Enter a location (e.g., MG Road, Bangalore)")
lat, lon = 12.9716, 77.5946  # Default Bangalore coordinates

if search_query:
    location = geolocator.geocode(search_query)
    if location:
        lat = location.latitude
        lon = location.longitude
        st.success(f"Location found: {location.address}")
    else:
        st.error("\u274C Location not found.")

st.subheader("\U0001F4CD Location Coordinates")
lat = st.number_input("Latitude", value=lat)
lon = st.number_input("Longitude", value=lon)

st.subheader("\U0001F4CA Real-Time Environmental Data")
vehicle_count = st.slider("Vehicle Count", min_value=0, max_value=500, value=50)
weather = st.selectbox("Weather Condition", ["Clear", "Rainy", "Foggy", "Snowy", "Windy"])
visibility = st.slider("Visibility (meters)", min_value=0, max_value=1000, value=500)

st.subheader("\U0001F6AB Accident Zone Status Based on Historical Data")
distance_threshold_km = 0.5

def find_nearby_accident(lat, lon):
    severities = []
    for _, row in df.iterrows():
        point = (row['latitude'], row['longitude'])
        distance = geodesic((lat, lon), point).km
        if distance <= distance_threshold_km:
            severities.append(row['casualty_severity'])
    if severities:
        return max(severities)
    return None

zone_status = find_nearby_accident(lat, lon)
is_danger = zone_status or vehicle_count > 200 or weather in ["Rainy", "Foggy"] or visibility < 300

if is_danger:
    st.error(f"\U0001F6A8 Danger! Accident-Prone Zone Detected! Severity: {zone_status if zone_status else 'Predicted by real-time inputs'}")
    color = [255, 0, 0]
else:
    st.success("\u2705 This zone appears to be safe based on current and historical data.")
    color = [0, 255, 0]

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/streets-v11',
    initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=14, pitch=50),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=[{"position": [lon, lat], "color": color, "radius": 150}],
            get_position="position",
            get_color="color",
            get_radius="radius",
        ),
    ],
))
