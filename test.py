import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

API_URL = "http://localhost:8000/prediction"

st.set_page_config(page_title="Uber Demand Forecasting", layout="wide")

# Header
st.markdown("""
    <h1 style='text-align:center;'>🚕 Uber Demand Forecasting Dashboard</h1>
    <p style='text-align:center; color:gray;'>Smart prediction of ride demand with spatial visualization</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,1])

location_coords = {
    "Midtown Manhattan": [40.7549, -73.9840],
    "Times Square": [40.7580, -73.9855],
    "JFK Airport": [40.6413, -73.7781],
    "LaGuardia Airport": [40.7769, -73.8740],
    "Upper East Side": [40.7736, -73.9566],
    "Chelsea": [40.7465, -74.0014],
    "Harlem": [40.8116, -73.9465],
    "Williamsburg": [40.7081, -73.9571],
    "Long Island City": [40.7447, -73.9485],
    "Financial District": [40.7075, -74.0113]
}

with col1:
    st.markdown("### User Input")

    ride_date = st.date_input("Select date")
    ride_time = st.time_input("Select time")

    locations_ = list(location_coords.keys())

    location = st.selectbox("Pickup location", locations_)

    year_ = ride_date.year
    month_ = ride_date.month
    day_ = ride_date.day
    hour_ = ride_time.hour

    if st.button("Predict Demand"):

        input_data = {
            "year": year_,
            "month": month_,
            "day": day_,
            "hour": hour_,
            "location": location
        }

        try:
            response = requests.post(API_URL, json=input_data)

            if response.status_code == 200:
                result = response.json()

                coords = location_coords.get(location)

                with col2:
                    st.markdown("### Prediction Result")
                    st.metric("Predicted Demand", result["Predicted_demand"])

                m = folium.Map(location=coords, zoom_start=12)

                folium.Marker(
                        coords,
                        popup=f"{location} | Demand: {result['Predicted_demand']}",
                        tooltip="Selected Pickup Location",
                        icon=folium.Icon(color="blue")
                ).add_to(m)

                st_folium(m, width=500, height=400)

            else:
                st.error(response.text)

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server")