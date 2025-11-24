import streamlit as st
import pandas as pd
import numpy as np
import swisseph as swe
import datetime
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

# --- UI Styling ---
st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(45deg, #ff9a9e 0%, #fad0c4 99%,#fad0c4 100%);
    min-height: 100vh;
    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)

# --- Setup ---
swe.set_ephe_path(".")
geolocator = Nominatim(user_agent="sav_app")

# --- Configs ---
sarvashtakavarga = {
    'Sun':     [5,3,2,4,6,4,4,5,4,5,3,3],
    'Moon':    [4,2,4,7,5,3,5,5,6,1,2,5],
    'Mercury': [3,7,4,3,3,5,5,7,6,3,3,5],
    'Venus':   [4,5,3,3,6,4,5,4,5,4,6,3],
    'Mars':    [3,4,2,3,2,3,5,3,5,3,2,4],
    'Jupiter': [5,1,5,5,4,5,8,3,5,5,3,7],
    'Saturn':  [3,3,0,7,4,2,5,3,4,4,2,2]
}

planet_keys = list(sarvashtakavarga.keys())
planet_map = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY, 'Venus': swe.VENUS,
    'Mars': swe.MARS, 'Jupiter': swe.JUPITER, 'Saturn': swe.SATURN
}
rashi_names = ['Mesha','Vrishabha','Mithuna','Karka','Simha','Kanya','Tula','Vrischika','Dhanu','Makara','Kumbha','Meena']

ayanamsa_map = {
    "Lahiri": swe.SIDM_LAHIRI,
    "Raman": swe.SIDM_RAMAN,
    "KP (Krishnamurti)": swe.SIDM_KRISHNAMURTI,
    "Pushya Paksha": swe.SIDM_TRUE_PUSHYA,
    "Sri Surya Siddhanta": swe.SIDM_SURYASIDDHANTA,
    "Fagan/Bradley": swe.SIDM_FAGAN_BRADLEY
}

house_systems = {
    "Placidus": "P",
    "Koch": "K",
    "Whole Sign": "W",
    "Equal": "E"
}

# --- UI ---
st.title("🔭 Sarvashtakavarga Analyzer + Cohen’s *d* Tracker")
hide_sidebar = st.checkbox("🧊 Hide Sidebar", key="hide_sidebar_toggle")

if "pob" not in st.session_state:
    st.session_state.pob = "Tiruchirappalli"

if not hide_sidebar:
    with st.sidebar:
        st.header("🧘‍♂️ Birth & Settings")
        st.text_input("Name (Optional)", value=st.session_state.get("name", "SR"), key="name")
        st.date_input("📅 Date of Birth", datetime.date(1972, 1, 20), key="dob", min_value=datetime.date(1935, 1, 1))
        st.time_input("⏰ Time of Birth", datetime.time(12, 30), key="tob")
        st.text_input("🌍 Place of Birth", value=st.session_state.pob, key="pob")

pob = st.session_state.get("pob", "Tiruchirappalli")
st.markdown("this app is developed by subramanian ramajayam")
st.markdown("---")
start_date = st.date_input("📆 Analysis Start Date", datetime.date(2024,3,1), key="start_date", min_value=datetime.date(1935, 1, 1))
duration = st.slider("📊 Number of Days", 30, 90, 45, key="duration")

st.markdown("---")
ayan_choice = st.selectbox("🧭 Ayanāmsa", list(ayanamsa_map.keys()), index=2, key="ayanamsa")
house_choice = st.selectbox("🏛️ House System", list(house_systems.keys()), index=0, key="house_system")
run = st.button("💫 Run SAV Analysis", key="run_button")

if run:
    try:
        loc = geolocator.geocode(pob)
        lat, lon = loc.latitude, loc.longitude
        swe.set_topo(lon, lat, 0)

        st.markdown(f"""
        📍 **Location found**: {loc.address}  
        🧭 **Latitude**: `{lat:.4f}`  
        🧭 **Longitude**: `{lon:.4f}`
        """)
    except:
        st.error("❌ Could not geolocate the place. Please check spelling or try a nearby town.")
        st.stop()

    swe.set_sid_mode(ayanamsa_map[ayan_choice])

    # Compute natal SAV
    dob = st.session_state.dob
    tob = st.session_state.tob
    jd_birth = swe.julday(dob.year, dob.month, dob.day, tob.hour + tob.minute / 60.0)
    natal_sav = 0
    natal_positions = {}

    for pname in planet_keys:
        pl = planet_map[pname]
        lon_deg = swe.calc(jd_birth, pl)[0][0]
        rashi = int(lon_deg // 30)
        bindu = sarvashtakavarga[pname][rashi]
        natal_sav += bindu
        natal_positions[pname] = f"{lon_deg:.2f}° ({rashi_names[rashi]})"

    st.markdown(f"🧬 **Natal SAV Baseline**: `{natal_sav}`")

    date_index = []
    sav_values = []
    planet_log = []

    for i in range(duration):
        date = start_date + datetime.timedelta(days=i)
        jd = swe.julday(date.year, date.month, date.day)
        daily_sav = 0
        row = {"Date": date.strftime("%Y-%m-%d")}

        for pname in planet_keys:
            pl = planet_map[pname]
            lon_deg = swe.calc_ut(jd, pl)[0][0]
            rashi = int(lon_deg // 30)
            bindu = sarvashtakavarga[pname][rashi]
            daily_sav += bindu
            row[pname] = f"{lon_deg:.2f}° ({rashi_names[rashi]})"

        row["SAV"] = daily_sav
        sav_values.append(daily_sav)
        date_index.append(date)
        planet_log.append(row)

    df = pd.DataFrame({
        "Date": date_index,
        "SAV": sav_values
    })

    st.subheader("📈 Daily SAV Timeline")
    st.line_chart(df.set_index("Date"))

    st.subheader("🧠 Cohen’s *d* Effect Size")
    window = 5
    compare_mode = st.radio("📊 Compare SAV against:", ["Previous Window", "Natal Baseline"], key="compare_mode")

    d_vals, d_labels = [], []

    for i in range(1, len(df) - window):
        g1 = df["SAV"].iloc[i-1:i-1+window]
        g2 = df["SAV"].iloc[i:i+window]
        pooled_std = np.sqrt((g1.std()**2 + g2.std()**2)/2) if compare_mode == "Previous Window" else g2.std()
        if compare_mode == "Previous Window":
            d = (g2.mean() - g1.mean()) / pooled_std if pooled_std else 0
        else:
            d = (g2.mean() - natal_sav) / pooled_std if pooled_std else 0
        d_vals.append(d)
        d_labels.append(df["Date"].iloc[i+window-1])

    fig, ax = plt.subplots(figsize=(10,4))
    ax.axhline(0, color='gray', linestyle='--')
    ax.plot(d_labels, d_vals, marker='o', color='teal')
    ax.set_title("Cohen’s *d* - Effect Size Over Time")
    ax.set_ylabel("Effect Size (d)")
    ax.grid(True)
    st.pyplot(fig)

    # --- Export CSV ---
    effect_df = pd.DataFrame({
        "Date": [pd.to_datetime(d).strftime("%Y-%m-%d") for d in d_labels],
        "Cohen_d": d_vals
    })

    st.subheader("📄 Downloadable Effect Size Table")
    #st.dataframe(effect_df, use_container_width)
    st.dataframe(effect_df, use_container_width=True)
