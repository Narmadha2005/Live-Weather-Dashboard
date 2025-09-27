import requests
from datetime import datetime
import streamlit as st

st.markdown("""
    <style>
    .weather-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: url('https://i.pinimg.com/originals/42/5b/81/425b811084dd2421c1df0fbe7576d883.gif') no-repeat center center fixed;
        background-size: cover;
        opacity: 0.3;
    }

    .weather-box {
        background: rgba(255, 255, 255, 0.75);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        color: #333;
        text-align: center;
        font-size: 18px;
        font-family: 'Segoe UI', sans-serif;
        height: 170px;
    }

    .weather-box img {
        width: 40px;
        height: 40px;
        margin-bottom: 10px;
    }

    .stApp {
        background: transparent;
    }

    .title {
        text-align: center;
        color: #ffffff;
        font-size: 36px;
        font-weight: bold;
    }    

    .subtitle {
        text-align: center;
        color: Black;
        font-size: 22px;
        margin-bottom: 10px;
    }

    .datetime {
        text-align: center;
        color: Black;
        font-size: 18px;
        margin-bottom: 20px;
    }
    </style>
    <div class="weather-background"></div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color:Black;'>🌦 Live Weather Dashboard</h1>", unsafe_allow_html=True)

user_api = "e48d2be8498da46d4532330c079b5ccb"
location = st.text_input("🔍 Enter City Name 🌎", "")

if location:
    try:
        complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={user_api}"
        api_response = requests.get(complete_api_link)
        api_data = api_response.json()

        if api_data.get('cod') != 200:
            st.error(f"❌ Error: {api_data.get('message', 'Invalid response')}")
            st.stop()

        temp_city = round(api_data['main']['temp'] - 273.15, 2)
        weather_desc = api_data['weather'][0]['description'].title()
        hmdt = api_data['main']['humidity']
        wind_spd = api_data['wind']['speed']
        date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

        safe_conditions = ['Clear', 'Few Clouds', 'Scattered Clouds']
        alert_message = ""
        alert_color = ""

        if any(condition.lower() in weather_desc.lower() for condition in safe_conditions):
            alert_message = "✅ Weather looks good! You can go out today 😊"
            alert_color = "green"
        else:
            alert_message = "⚠️ Weather isn't great. Better to stay indoors today! 🌧️"
            alert_color = "Red"

        st.markdown(f"""
            <div style='background-color:{alert_color}; padding: 15px;
                        border-radius: 10px; text-align: center;
                        font-size: 20px; font-weight: bold; color: white;
                        box-shadow: Light red; margin-bottom: 20px;'>
                {alert_message}
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<div class='subtitle'>📍 Weather for {location.upper()}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='datetime'>🕒 {date_time}</div>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="large")

        with col1:
            st.markdown(f"""
                <div class="weather-box">
                    <img src="https://cdn-icons-png.flaticon.com/512/1684/1684375.png">
                    <div><b>Temperature</b></div>
                    <div>{temp_city} °C</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="weather-box">
                    <img src="https://cdn-icons-png.flaticon.com/512/728/728093.png">
                    <div><b>Humidity</b></div>
                    <div>{hmdt}%</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="weather-box">
                    <img src="https://cdn-icons-png.flaticon.com/512/414/414974.png">
                    <div><b>Wind Speed</b></div>
                    <div>{wind_spd} km/h</div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div class="weather-box">
                    <img src="https://cdn-icons-png.flaticon.com/512/1163/1163661.png">
                    <div><b>Condition</b></div>
                    <div>{weather_desc}</div>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")
