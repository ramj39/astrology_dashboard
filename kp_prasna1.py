import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import altair as alt
from datetime import datetime

# -------------------------
# Config and helpers
# -------------------------
st.set_page_config(page_title="KP Prasna SAV Analyzer", layout="wide")

# Styles
PRIMARY_COLOR = "#2d6cdf"
GOOD_COLOR = "#2fbf71"
BAD_COLOR = "#e4572e"
NEUTRAL_COLOR = "#8898aa"

# Utility: safe float
def to_float(x, default=np.nan):
    try:
        return float(x)
    except:
        return default

# Ascendant fallback via KP horary number
def kp_horary_to_asc_degree(horary_number: int) -> float:
    """
    Fallback mapping: divide zodiac (360°) into 249 segments, assign center of segment.
    This is a placeholder when precise astro libraries are unavailable.
    """
    n = max(1, min(249, int(horary_number)))
    segment_size = 360.0 / 249.0
    asc_deg = (n - 0.5) * segment_size  # center of segment
    # Normalize to [0, 360)
    return asc_deg % 360.0

def degree_to_sign(deg: float):
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    idx = int(np.floor((deg % 360) / 30))
    return signs[idx], idx + 1  # house/sign number 1-12

def compute_cohens_d(group_vals, baseline_vals):
    g = np.array(group_vals, dtype=float)
    b = np.array(baseline_vals, dtype=float)
    g = g[~np.isnan(g)]
    b = b[~np.isnan(b)]
    if len(g) < 2 or len(b) < 2:
        return np.nan
    mg, mb = np.mean(g), np.mean(b)
    sg, sb = np.std(g, ddof=1), np.std(b, ddof=1)
    pooled = np.sqrt(((len(g)-1)*sg**2 + (len(b)-1)*sb**2) / (len(g)+len(b)-2))
    if pooled == 0:
        return np.nan
    return (mg - mb) / pooled

def classify_effect(d, good_threshold=0.5, bad_threshold=-0.5):
    if np.isnan(d):
        return "inconclusive", NEUTRAL_COLOR
    if d >= good_threshold:
        return "good", GOOD_COLOR
    if d <= bad_threshold:
        return "adversity", BAD_COLOR
    return "neutral", NEUTRAL_COLOR

def bytes_from_df(df: pd.DataFrame) -> BytesIO:
    buf = BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return buf

# -------------------------
# Sidebar: Inputs
# -------------------------
st.sidebar.header("Inputs")

# KP horary + location/time
horary = st.sidebar.number_input("KP horary number (1–249)", min_value=1, max_value=249, value=108)
lat = st.sidebar.text_input("Latitude (e.g., 12.693)", value="12.693")
lon = st.sidebar.text_input("Longitude (e.g., 79.975)", value="79.975")
dt_str = st.sidebar.text_input("Local date & time (YYYY-MM-DD HH:MM)", value=datetime.now().strftime("%Y-%m-%d %H:%M"))

# Ascendant computation mode
asc_mode = st.sidebar.selectbox("Ascendant mode", ["Fallback (KP segment)", "Manual entry"])
manual_deg = st.sidebar.text_input("Ascendant degree (0–360) if manual", value="")

# CSV upload
st.sidebar.subheader("Upload SAV CSV")
uploaded = st.sidebar.file_uploader("30-day SAV CSV", type=["csv"])

# Column mapping
st.sidebar.subheader("CSV column mapping")
col_date = st.sidebar.text_input("Date/day column name", value="date")
col_sav = st.sidebar.text_input("SAV total column name", value="sav_total")

# Analysis options
st.sidebar.subheader("Analysis options")
baseline_choice = st.sidebar.selectbox("Baseline for Cohen’s d", ["Global mean (all 30 days)", "First cohort (days 1–5)"])
good_thr = st.sidebar.slider("Good threshold (d)", 0.2, 1.0, 0.5, 0.1)
bad_thr = st.sidebar.slider("Adversity threshold (d)", -1.0, -0.2, -0.5, 0.1)
show_bands = st.sidebar.checkbox("Show z-score bands on time-series", value=True)

# -------------------------
# Ascendant section
# -------------------------
st.header("Prasna ascendant fixing from KP horary, location, time")

# Parse inputs
lat_f = to_float(lat)
lon_f = to_float(lon)

if asc_mode == "Manual entry":
    asc_deg = to_float(manual_deg)
    if np.isnan(asc_deg):
        asc_deg = kp_horary_to_asc_degree(horary)
else:
    asc_deg = kp_horary_to_asc_degree(horary)

sign_name, sign_num = degree_to_sign(asc_deg)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ascendant degree", f"{asc_deg:.2f}°")
with col2:
    st.metric("Ascendant sign", f"{sign_name}")
with col3:
    st.metric("Ascendant sign number", f"{sign_num}")

st.caption("Note: This uses a robust fallback mapping from KP horary number to zodiac degree. Swap to manual mode to override degree if needed.")

# -------------------------
# Data ingestion and prep
# -------------------------
st.header("SAV data ingestion and validation")

if uploaded is not None:
    df = pd.read_csv(uploaded)
    # Flexible handling: if sav_total missing but house columns present, sum them.
    if col_sav not in df.columns:
        house_cols = [c for c in df.columns if c.lower().startswith("house_")]
        if house_cols:
            df[col_sav] = df[house_cols].sum(axis=1, skipna=True)
    # Build day index
    if col_date in df.columns:
        # Attempt to parse numeric day or date
        try:
            # If numeric-like
            day_idx = pd.to_numeric(df[col_date], errors="coerce")
            if day_idx.notna().sum() >= 20 and day_idx.max() <= 31:
                df["day"] = day_idx.astype(int)
            else:
                # Parse as dates and rank
                dates = pd.to_datetime(df[col_date], errors="coerce")
                df["day"] = dates.rank(method="first").astype(int)
                df["date_parsed"] = dates
        except:
            df["day"] = np.arange(1, len(df) + 1)
    else:
        df["day"] = np.arange(1, len(df) + 1)

    # Filter to first 30 entries if longer
    df = df.sort_values("day").head(30).reset_index(drop=True)
    df["sav"] = pd.to_numeric(df[col_sav], errors="coerce")

    # Validate coverage
    missing_days = set(range(1, 31)) - set(df["day"].tolist())
    if missing_days:
        st.warning(f"Missing day indices found: {sorted(list(missing_days))}. The analysis uses available days only.")

    # -------------------------
    # Cohort grouping (5-day windows)
    # -------------------------
    st.header("5-day cohort statistics and effect sizes")
    df["cohort"] = ((df["day"] - 1) // 5) + 1  # 1..6
    cohorts = []
    for k in range(1, 7):
        sub = df[df["cohort"] == k].copy()
        mean_val = sub["sav"].mean()
        std_val = sub["sav"].std(ddof=1)
        cohorts.append({"cohort": k, "n": len(sub), "mean": mean_val, "std": std_val})

    cohort_df = pd.DataFrame(cohorts)

    # Baseline selection
    if baseline_choice == "Global mean (all 30 days)":
        baseline_vals = df["sav"].values
        baseline_label = "Global baseline"
    else:
        baseline_vals = df[df["cohort"] == 1]["sav"].values
        baseline_label = "Cohort 1 baseline"

    # Compute Cohen's d per cohort
    d_vals, classes = [], []
    for k in range(1, 7):
        gvals = df[df["cohort"] == k]["sav"].values
        d = compute_cohens_d(gvals, baseline_vals)
        label, color = classify_effect(d, good_thr, bad_thr)
        d_vals.append(d)
        classes.append({"cohort": k, "label": label, "color": color})

    cohort_df["cohens_d"] = d_vals
    class_df = pd.DataFrame(classes)
    cohort_df = cohort_df.merge(class_df, on="cohort", how="left")

    # -------------------------
    # Visualizations
    # -------------------------
    st.subheader("Time-series of SAV with optional z-bands")
    base_chart = alt.Chart(df).encode(
        x=alt.X("day:Q", title="Day"),
        y=alt.Y("sav:Q", title="SAV total")
        #plt.ylim(130, max(y) + 10)  # y-axis starts at 130
    )
    #plt.plot(x, y)
    #plt.ylim(130, max(y) + 10)  # y-axis starts at 130
    #plt.show()

    line = base_chart.mark_line(color=PRIMARY_COLOR).encode()
    points = base_chart.mark_circle(color=PRIMARY_COLOR).encode()

    charts = line + points

    if show_bands:
        mu = df["sav"].mean()
        sigma = df["sav"].std(ddof=1)
        band_df = pd.DataFrame({
            "band": ["mean", "+1σ", "-1σ"],
            "y": [mu, mu + sigma, mu - sigma]
        })
        bands = alt.Chart(band_df).mark_rule(color=NEUTRAL_COLOR, strokeDash=[4,4]).encode(
            y="y:Q"
        )
        charts = charts + bands

    st.altair_chart(charts.properties(height=280), use_container_width=True)

    st.subheader("Cohort means and Cohen’s d classification")
    bar_chart = alt.Chart(cohort_df).mark_bar().encode(
        x=alt.X("cohort:O", title="5-day cohort"),
        y=alt.Y("mean:Q", title="Mean SAV"),
        color=alt.Color("label:N",
                        scale=alt.Scale(domain=["good", "neutral", "adversity"],
                                        range=[GOOD_COLOR, NEUTRAL_COLOR, BAD_COLOR]))
    )
    text = alt.Chart(cohort_df).mark_text(dy=-10, fontSize=12).encode(
        x="cohort:O",
        y="mean:Q",
        text=alt.Text("cohens_d:Q", format=".2f"),
        color=alt.value("#333333")
    )
    st.altair_chart((bar_chart + text).properties(height=280), use_container_width=True)

    # -------------------------
    # Predictions panel
    # -------------------------
    st.subheader("Predictions and interpretation")
    def cohort_range(k):
        start = (k-1)*5 + 1
        end = k*5
        return f"Days {start}–{end}"

    interp_rows = []
    for _, row in cohort_df.iterrows():
        label = row["label"]
        desc = {
            "good": "Effect-size suggests favorable period relative to baseline.",
            "adversity": "Effect-size suggests challenging period relative to baseline.",
            "neutral": "No strong deviation from baseline; expect mixed/steady signals.",
            "inconclusive": "Insufficient data or variance for reliable effect-size."
        }[label]
        interp_rows.append({
            "cohort": int(row["cohort"]),
            "range": cohort_range(int(row["cohort"])),
            "mean_sav": row["mean"],
            "std_sav": row["std"],
            "cohens_d": row["cohens_d"],
            "classification": label,
            "interpretation": desc
        })
    interp_df = pd.DataFrame(interp_rows)

    st.dataframe(interp_df.style.format({
        "mean_sav": "{:.2f}",
        "std_sav": "{:.2f}",
        "cohens_d": "{:.2f}"
    }), use_container_width=True)

    # -------------------------
    # Exports
    # -------------------------
    st.subheader("Download results")
    stats_csv = bytes_from_df(interp_df)
    st.download_button("Download cohort stats (CSV)", stats_csv, file_name="cohort_stats.csv", mime="text/csv")

    annotated_df = df[["day", "sav", "cohort"]].merge(interp_df[["cohort", "classification"]], on="cohort", how="left")
    ann_csv = bytes_from_df(annotated_df)
    st.download_button("Download annotated daily SAV (CSV)", ann_csv, file_name="annotated_sav.csv", mime="text/csv")

else:
    st.info("Upload your 30-day SAV CSV in the sidebar to proceed with analysis. Ensure it includes a date/day column and a SAV total column (or per-house columns to be summed).")

# -------------------------
# Diagnostics and teachable toggles
# -------------------------
st.header("Diagnostics and teachable overlays")
with st.expander("Show data preview and missing values"):
    if uploaded is not None:
        st.write(df.head(10))
        st.write({"rows": len(df), "days_covered": sorted(df['day'].unique().tolist())})
    else:
        st.write("Awaiting CSV upload...")

with st.expander("Adjust classification thresholds and rerun"):
    st.write("Use sidebar sliders to tune good/adversity thresholds and instantly update charts and predictions.")

with st.expander("Notes on ascendant calculation"):
    st.write("Astronomical ascendant can be computed precisely with ephemeris libraries. This app provides a KP-horary fallback and manual override for reproducible workflows without heavy dependencies.")
st.write("developed by Subramanian Ramajayam")
st. balloons()
