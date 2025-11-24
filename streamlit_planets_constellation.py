import streamlit as st
import ephem
import pandas as pd
import datetime

# 🎨 Styling
st.set_page_config(page_title="Planet Ephemeris Viewer", layout="centered")
st.markdown("""
    <style>
        body { background-color: #f0f8ff; color: #003366; }
        .stApp { background-color: #f0f8ff; }
        h1, h2, h3 { color: #003366; }
    </style>
""", unsafe_allow_html=True)

# 🪐 Planet options
planet_names = {
    "Sun":ephem.Sun,
    "Moon":ephem.Moon,
    "Mercury": ephem.Mercury,
    "Venus": ephem.Venus,
    "Mars": ephem.Mars,
    "Jupiter": ephem.Jupiter,
    "Saturn": ephem.Saturn,
    "Uranus": ephem.Uranus,
     
}

st.title("📆 Planet Ephemeris Viewer")

# 🌍 Select planet
selected_planet = st.selectbox("Choose a planet", list(planet_names.keys()))

# 📅 Date range
#start_date = st.date_input("Start date", datetime.date(1950,1,1))
#end_date = st.date_input("End date", datetime.date(1950,1,1))
# 📅 Date picker
#selected_date = st.date_input(
start_date = st.date_input(
    "Select a date",
    value=datetime.date.today(),
    min_value=datetime.date(1950, 1, 1),
    max_value=datetime.date(2030, 12, 31)
)
end_date = st.date_input("End date", value = datetime.date.today(),min_value = datetime.date(1950,1,1))

# 📏 Step size
step_days = st.slider("Step size (days)", min_value=1, max_value=30, value=1)

# 🧮 Generate ephemeris
if start_date >= end_date:
    st.error("End date must be after start date.")
else:
    planet_class = planet_names[selected_planet]
    dates = pd.date_range(start=start_date, end=end_date, freq=f"{step_days}D")
    data = []

    for date in dates:
        date_str = date.strftime('%Y/%m/%d')
        planet = planet_class(date_str)
        ra = planet.ra
        dec = planet.dec
        dist = planet.earth_distance
        const = ephem.constellation(planet)[1]
        data.append({
            "Date": date.strftime('%Y-%m-%d'),
            "RA": str(ra),
            "Dec": str(dec),
            "Distance (AU)": round(dist, 4),
            "Constellation": const
        })

    df = pd.DataFrame(data)
    st.subheader(f"{selected_planet} Ephemeris from {start_date} to {end_date}")
    st.dataframe(df)

    # 📤 Optional CSV export
    st.download_button("Download CSV", df.to_csv(index=False), file_name=f"{selected_planet}_ephemeris.csv")
st.markdown("Crafted with resonance by SubramanianRamajayam. Powered by the stars. Guided by data. 📿🖤")
