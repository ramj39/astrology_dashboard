import streamlit as st
import ephem
import datetime
st.title("🌌 Ephemeris Viewer with PyEphem")

# 📍 User Inputs
st.sidebar.header("Observer Location")
lon = st.sidebar.text_input("Longitude", "80.2707")
lat = st.sidebar.text_input("Latitude", "13.0827")

# 📅 Date Input
date_input = st.sidebar.text_input("Date (YYYY-MM-DD HH:MM:SS)", "2025-08-25 16:34:56")

try:
    # 🕒 Convert to epoch
    date = datetime.datetime.strptime(date_input, '%Y-%m-%d %H:%M:%S')
    epoch_date = int(date.timestamp())
    st.write(f"**Epoch Timestamp:** {epoch_date}")

    # 🌍 Observer Setup
    obs = ephem.Observer()
    obs.lon, obs.lat = lon, lat
    obs.date = date_input

    # 🪐 Venus Position
    venus = ephem.Venus(obs)
    st.write(f"**Venus Altitude:** {venus.alt}")
    st.write(f"**Venus Azimuth:** {venus.az}")
     # 🪐 Sun Position
    sun = ephem.Sun(obs)
    st.write(f"**Sun Altitude:** {sun.alt}")
    st.write(f"**Sun Azimuth:** {sun.az}")
     # 🪐 Moon Position
    moon = ephem.Moon(obs)
    st.write(f"**Moon Altitude:** {moon.alt}")
    st.write(f"**Moon Azimuth:** {moon.az}")
    # 🪐 Mercury Position
    mercury = ephem.Mercury(obs)
    st.write(f"**Mercury Altitude:** {mercury.alt}")
    st.write(f"**Mercury Azimuth:** {mercury.az}")
     # 🪐 Mars Position
    mars = ephem.Mars(obs)
    st.write(f"**Mars Altitude:** {mars.alt}")
    st.write(f"**Mars Azimuth:** {mars.az}")
     # 🪐 Jupiter Position
    jupiter = ephem.Jupiter(obs)
    st.write(f"**Jupiter Altitude:** {jupiter.alt}")
    st.write(f"**Jupiter Azimuth:** {jupiter.az}")
     # 🪐 Saturn Position
    saturn = ephem.Saturn(obs)
    st.write(f"**Saturn Altitude:** {saturn.alt}")
    st.write(f"**Saturn Azimuth:** {saturn.az}")

    st.subheader("Constellations on Selected Date")
    st.write(f"**Mars** is in {ephem.constellation(mars)[1]}")
    st.write(f"**Sun** is in {ephem.constellation(sun)[1]}")
    st.write(f"**Moon** is in {ephem.constellation(moon)[1]}")
    st.write(f"**Mercury** is in {ephem.constellation(mercury)[1]}")
    st.write(f"**Jupiter** is in {ephem.constellation(jupiter)[1]}")
    st.write(f"**Saturn** is in {ephem.constellation(saturn)[1]}")
    st.write(f"**Venus** is in {ephem.constellation(venus)[1]}")

    # 🌕 Moon Phases
    d1 = ephem.next_full_moon(date_input)
    d2 = ephem.next_new_moon(d1)
    d3 = ephem.previous_new_moon(date_input)
    d4 = ephem.next_new_moon(d3)

    st.subheader("🌙 Moon Phases")
    st.write(f"Next Full Moon: {d1}")
    st.write(f"Next New Moon after Full Moon: {d2}")
    st.write(f"Previous New Moon: {d3}")
    st.write(f"Next New Moon after Previous: {d4}")

except Exception as e:
    st.error(f"Error: {e}")
st.markdown("[link to kp analysis](https://astrologydashboard-rwhggza2rnprd6sgufnf9e.streamlit.app/)"))
st.text("thanks for using this app ,developed by S.Ramajayam")



