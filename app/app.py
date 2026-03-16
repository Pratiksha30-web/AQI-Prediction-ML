import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Air Quality Predictor",
    page_icon="🌍",
    layout="centered"
)

# Load model
model = joblib.load("models/model.pkl")

# Title
st.title("🌍 AI Air Quality Prediction System")
st.markdown("### Predict AQI and Get Health Precautions")

st.write("""
This AI system predicts the **Air Quality Index (AQI)** based on pollutant levels  
and provides **age-specific health precautions**.
""")

st.markdown("---")

# Input layout
col1, col2 = st.columns(2)

with col1:
    pm25 = st.number_input("PM2.5", min_value=0.0)
    no2 = st.number_input("NO2", min_value=0.0)
    co = st.number_input("CO", min_value=0.0)

with col2:
    pm10 = st.number_input("PM10", min_value=0.0)
    so2 = st.number_input("SO2", min_value=0.0)

st.markdown("---")

# AQI Category
def get_aqi_category(aqi):

    aqi = round(aqi)

    if aqi <= 50:
        return "Good 🌿"
    elif aqi <= 100:
        return "Satisfactory 🙂"
    elif aqi <= 200:
        return "Moderate 😐"
    elif aqi <= 300:
        return "Poor 😷"
    elif aqi <= 400:
        return "Very Poor ⚠️"
    else:
        return "Severe 🚨"


# Age-wise precautions
def get_precautions(aqi):

    aqi = round(aqi)

    if aqi <= 50:
        return {
            "Children": "Safe to play outdoors.",
            "Adults": "Normal outdoor activities are safe.",
            "Elderly": "Safe for walking and light exercise.",
            "Respiratory Patients": "Minimal health risk."
        }

    elif aqi <= 100:
        return {
            "Children": "Outdoor play is allowed but avoid long exposure.",
            "Adults": "Normal activities allowed.",
            "Elderly": "Limit long outdoor exposure.",
            "Respiratory Patients": "Avoid heavy outdoor exercise."
        }

    elif aqi <= 200:
        return {
            "Children": "Limit outdoor play.",
            "Adults": "Reduce prolonged outdoor exertion.",
            "Elderly": "Prefer staying indoors during peak pollution.",
            "Respiratory Patients": "Avoid outdoor activities."
        }

    elif aqi <= 300:
        return {
            "Children": "Avoid outdoor play.",
            "Adults": "Reduce outdoor exposure and wear masks.",
            "Elderly": "Stay indoors.",
            "Respiratory Patients": "Avoid outdoor exposure."
        }

    elif aqi <= 400:
        return {
            "Children": "No outdoor activities.",
            "Adults": "Wear N95 masks outdoors.",
            "Elderly": "Stay indoors and use air purifiers.",
            "Respiratory Patients": "High risk. Avoid exposure."
        }

    else:
        return {
            "Children": "Stay indoors completely.",
            "Adults": "Avoid going outside.",
            "Elderly": "Remain indoors.",
            "Respiratory Patients": "Very dangerous conditions."
        }


# AQI Gauge Meter
def show_aqi_gauge(aqi):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi,
        title={'text': "AQI Level"},
        gauge={
            'axis': {'range': [0, 500]},
            'steps': [
                {'range': [0, 50], 'color': "green"},
                {'range': [50, 100], 'color': "lightgreen"},
                {'range': [100, 200], 'color': "yellow"},
                {'range': [200, 300], 'color': "orange"},
                {'range': [300, 400], 'color': "red"},
                {'range': [400, 500], 'color': "darkred"}
            ]
        }
    ))

    st.plotly_chart(fig)


# Prediction
if st.button("🔍 Predict AQI"):

    data = np.array([[pm25, pm10, no2, so2, co]])

    prediction = model.predict(data)[0]

    category = get_aqi_category(prediction)

    precautions = get_precautions(prediction)

    st.success(f"Predicted AQI: {prediction:.2f}")

    st.info(f"Air Quality Category: {category}")

    # Gauge meter
    show_aqi_gauge(prediction)

    # Pollutant graph
    pollutants = {
        "PM2.5": pm25,
        "PM10": pm10,
        "NO2": no2,
        "SO2": so2,
        "CO": co
    }

    fig, ax = plt.subplots()
    ax.bar(pollutants.keys(), pollutants.values())
    ax.set_title("Pollutant Levels")
    ax.set_ylabel("Concentration")

    st.pyplot(fig)

    # Health precautions
    st.markdown("### Health Precautions")

    st.write("👶 **Children:** ", precautions["Children"])
    st.write("🧑 **Adults:** ", precautions["Adults"])
    st.write("👴 **Elderly:** ", precautions["Elderly"])
    st.write("🤧 **Respiratory Patients:** ", precautions["Respiratory Patients"])

st.markdown("---")

# Pollutant info
st.markdown("### Pollutants Used")

st.write("""
**PM2.5** – Fine particles harmful to lungs  
**PM10** – Dust particles in air  
**NO₂** – Vehicle emission gas  
**SO₂** – Industrial pollution gas  
**CO** – Carbon monoxide from fuel burning
""")

st.markdown("---")

# AQI categories
st.markdown("### AQI Categories")

st.write("""
| AQI Range | Category |
|-----------|----------|
| 0 – 50 | Good 🌿 |
| 51 – 100 | Satisfactory |
| 101 – 200 | Moderate |
| 201 – 300 | Poor |
| 301 – 400 | Very Poor |
| 401 – 500 | Severe |
""")

st.markdown("---")

st.caption("AI-based Air Quality Prediction and Health Advisory System")