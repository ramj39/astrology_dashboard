import streamlit as st
import swisseph as swe
import pytz
from datetime import datetime
# Disclaimer text
st.markdown(
    """
    <style>
    .disclaimer {
        background-color: #FFFF99; /* canary yellow */
        color: #000000;            /* black text */
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    <div class="disclaimer">
        ⚠️ Disclaimer: This application is for educational and analytical purposes only.  
        It should not be used as a substitute for professional medical advice, diagnosis, or treatment.  
        Always seek the advice of qualified health providers with any questions about medical conditions.
    </div>
    """,
    unsafe_allow_html=True
)
# -----------------------------
# Directions & Place Clues
# -----------------------------
PLANET_DIRECTIONS = {
    'Sun': ('East', 'Near light, windows, open spaces, official desk'),
    'Moon': ('Northwest', 'Moist places, upper shelves, near water or containers'),
    'Mars': ('South', 'Kitchens, tools, machinery, heat sources'),
    'Mercury': ('North', 'Study rooms, desks, books, papers, communication devices'),
    'Jupiter': ('Northeast', 'Sacred/educational spots, near books, religious items'),
    'Venus': ('Southeast', 'Decorative areas, ornaments, clothes, perfumes'),
    'Saturn': ('West', 'Dark corners, storage, old piles, behind furniture'),
    'Rahu': ('Southwest', 'Hidden piles, mixed items, confusing spots'),
    'Ketu': ('South', 'Isolated corners, obscure places, detached areas'),
}

GOOD_HOUSES = [1, 2, 4, 9, 11]
MIDL_HOUSES = [3, 5, 7, 10]
BAD_HOUSES = [6, 8, 12]

# -----------------------------
# Nakshatra & Starlord Mapping
# -----------------------------
NAKSHATRAS = [
    ('Ashwini', 'Ketu', 0), ('Bharani', 'Venus', 13.3333), ('Krittika', 'Sun', 26.6667),
    ('Rohini', 'Moon', 40), ('Mrigashira', 'Mars', 53.3333), ('Ardra', 'Rahu', 66.6667),
    ('Punarvasu', 'Jupiter', 80), ('Pushya', 'Saturn', 93.3333), ('Ashlesha', 'Mercury', 106.6667),
    ('Magha', 'Ketu', 120), ('Purva Phalguni', 'Venus', 133.3333), ('Uttara Phalguni', 'Sun', 146.6667),
    ('Hasta', 'Moon', 160), ('Chitra', 'Mars', 173.3333), ('Swati', 'Rahu', 186.6667),
    ('Vishakha', 'Jupiter', 200), ('Anuradha', 'Saturn', 213.3333), ('Jyeshtha', 'Mercury', 226.6667),
    ('Mula', 'Ketu', 240), ('Purva Ashadha', 'Venus', 253.3333), ('Uttara Ashadha', 'Sun', 266.6667),
    ('Shravana', 'Moon', 280), ('Dhanishta', 'Mars', 293.3333), ('Shatabhisha', 'Rahu', 306.6667),
    ('Purva Bhadrapada', 'Jupiter', 320), ('Uttara Bhadrapada', 'Saturn', 333.3333), ('Revati', 'Mercury', 346.6667),
]

def get_nakshatra_and_starlord(moon_lon):
    lon = moon_lon % 360
    current = NAKSHATRAS[0]
    for name, lord, start in NAKSHATRAS:
        if lon >= start:
            current = (name, lord, start)
    return current[0], current[1]

# -----------------------------
# Horary Ascendant Mapping
# -----------------------------
def get_ascendant_from_horary(horary_number):
    # Map horary number (1–249) to 0–360°
    asc_deg = (horary_number / 249.0) * 360.0
    return asc_deg

def house_of(lon, asc_deg):
    diff = (lon - asc_deg) % 360
    return int(diff / 30) + 1

# -----------------------------
# Prasna Analysis
# -----------------------------
def analyze_prasna(jd, horary_number):
    # Planet longitudes
    planets = {}
    for p, name in [(swe.SUN, 'Sun'), (swe.MOON, 'Moon'), (swe.MARS, 'Mars'),
                    (swe.MERCURY, 'Mercury'), (swe.JUPITER, 'Jupiter'),
                    (swe.VENUS, 'Venus'), (swe.SATURN, 'Saturn')]:
        pos, ret = swe.calc_ut(jd, p)
        lon, lat, dist = pos[0], pos[1], pos[2]
        planets[name] = lon

    moon_lon = planets['Moon']
    nakshatra, starlord = get_nakshatra_and_starlord(moon_lon)

    asc_deg = get_ascendant_from_horary(horary_number)
    moon_house = house_of(moon_lon, asc_deg)
    starlord_house = house_of(planets[starlord], asc_deg) if starlord in planets else None

    # Decision flow
    if moon_house in [1, 2, 11]:
        possibility = "Recovery likely"
    else:
        if starlord_house in GOOD_HOUSES:
            possibility = "Recovery assured via starlord"
        elif starlord_house in MIDL_HOUSES:
            possibility = "Recovery possible with effort/help"
        else:
            possibility = "Recovery doubtful or delayed"

    # Timing
    fast = ['Moon', 'Mercury', 'Venus']
    slow = ['Saturn', 'Rahu', 'Ketu']
    timing = "Quick" if (starlord in fast) else "Delayed" if (starlord in slow) else "Moderate"

    # Direction
    direction, place = PLANET_DIRECTIONS.get(starlord, ('Varies', 'Check house rulers and local context'))

    return {
        'moon_house': moon_house,
        'nakshatra': nakshatra,
        'starlord': starlord,
        'starlord_house': starlord_house,
        'possibility': possibility,
        'timing': timing,
        'direction': direction,
        'place': place
    }

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Lost-Item Prasna", page_icon="🔎", layout="centered")
st.title("🔎 Lost‑Item Prasna — Horary Dashboard (Swiss Ephemeris)")

col1, col2 = st.columns(2)
with col1:
    horary_number = st.number_input("Horary Number (1–249)", min_value=1, max_value=249, value=108)
    date_input = st.date_input("Horary Date (YYYY-MM-DD)")
    lat = st.number_input("Latitude (°)", format="%.6f", value=12.692000)
with col2:
    time_input = st.time_input("Horary Time (HH:MM)")
    lon = st.number_input("Longitude (°)", format="%.6f", value=79.976000)

tzname = st.text_input("Timezone (e.g., Asia/Kolkata)", value="Asia/Kolkata")

if st.button("Compute Prasna"):
    try:
        tz = pytz.timezone(tzname)
        local_dt = tz.localize(datetime.combine(date_input, time_input))
        jd = swe.julday(local_dt.year, local_dt.month, local_dt.day,
                        local_dt.hour + local_dt.minute/60.0)

        result = analyze_prasna(jd, horary_number)

        st.subheader("🪔 Chart Summary")
        st.write(f"**Moon house:** {result['moon_house']}")
        st.write(f"**Moon nakshatra:** {result['nakshatra']}")
        st.write(f"**Moon starlord:** {result['starlord']} (house {result['starlord_house']})")

        st.subheader("✅ Decision")
        st.write(f"**Possibility:** {result['possibility']}")
        st.write(f"**Timing:** {result['timing']}")
        st.write(f"**Direction:** {result['direction']}")
        st.write(f"**Place clues:** {result['place']}")

    except Exception as e:
        st.error(f"Could not compute the chart. Error: {e}")
        st.markdown("[Open southindian_chart](http://localhost:8502)")

