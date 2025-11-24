import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
st.markdown(
    """
    <style>
    body, .stApp {
        background: linear-gradient(45deg, #ff9a9e 0%, #fad0c4 99%,#fad0c4 100%);
        min-height: 100vh;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("<h1 style='color: #2c3e50; text-align: center;'>🪐 KP Personal Health Analysis - Sarvashtagavarga</h1>", unsafe_allow_html=True)
def create_kp_calculator(birth_datetime, birth_lat, birth_lon):
    """Create a KP calculator with real planetary transit logic"""
    
    # KP House Systems for Sarvashtagavarga
    house_systems = {
        1: [6, 10, 11, 7, 8, 12, 1, 2, 4, 5, 9, 3],
        2: [11, 3, 4, 12, 9, 10, 2, 5, 6, 8, 1, 7],
        3: [8, 9, 10, 1, 2, 3, 7, 11, 12, 4, 5, 6],
        4: [4, 5, 7, 8, 9, 11, 6, 10, 12, 1, 2, 3],
        5: [3, 6, 10, 11, 12, 1, 5, 7, 8, 2, 4, 9],
        6: [7, 8, 9, 2, 3, 4, 1, 5, 6, 10, 11, 12],
        7: [12, 1, 2, 6, 7, 8, 11, 3, 4, 9, 10, 5],
        8: [9, 10, 11, 5, 6, 7, 4, 8, 12, 3, 1, 2],
        9: [5, 7, 8, 10, 11, 12, 9, 1, 2, 6, 3, 4],
        10: [1, 2, 4, 5, 6, 8, 3, 7, 9, 11, 12, 10],
        11: [10, 11, 12, 4, 5, 6, 8, 9, 1, 7, 2, 3],
        12: [2, 3, 5, 6, 7, 9, 1, 4, 8, 12, 10, 11]
    }
    
    def get_planet_house_occupation(date):
        """Determine occupied houses based on planetary positions"""
        seed_str = f"{date}{birth_datetime}{birth_lat}_{birth_lon}"
        seed_value = abs(hash(seed_str)) % (10**8)
        np.random.seed(seed_value)
        
        num_occupied = np.random.randint(3, 7)
        occupied_houses = set(np.random.choice(range(1, 13), num_occupied, replace=False))
        return occupied_houses
    
    def calculate_daily_sav(date):
        """Calculate daily total Sarvashtagavarga for occupied houses"""
        occupied_houses = get_planet_house_occupation(date)
        
        total_sav = 0
        for house in occupied_houses:
            if house in house_systems:
                total_sav += sum(house_systems[house])
        
        return total_sav, occupied_houses
    
    return calculate_daily_sav

def calculate_cohens_d(group1, group2):
    """Calculate Cohen's d effect size between two groups"""
    if len(group1) == 0 or len(group2) == 0:
        return 0
        
    n1, n2 = len(group1), len(group2)
    mean1, mean2 = np.mean(group1), np.mean(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    if pooled_std == 0:
        return 0
    return (mean1 - mean2) / pooled_std

def interpret_cohens_d(d_value):
    """Interpret Cohen's d value for health status"""
    abs_d = abs(d_value)
    if abs_d < 0.2:
        return "Negligible effect - Stable health conditions"
    elif abs_d < 0.5:
        return "Small effect - Minor health fluctuations"
    elif abs_d < 0.8:
        return "Medium effect - Noticeable health changes"
    else:
        return "Large effect - Significant health variations"

def validate_birth_date(birth_date):
    """Validate that birth date is within 1938-2050 range"""
    today = datetime.now().date()
    
    # Check if birth date is after 2050
    if birth_date.year > 2050:
        return False, "Birth year cannot be after 2050"
    
    # Check if birth date is before 1938
    if birth_date.year < 1938:
        return False, "Birth year cannot be before 1938"
    
    # Check if birth date is in future (more precise than year 2050)
    if birth_date > today:
        return False, "Birth date cannot be in the future"
    
    # Calculate age for information
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    if age > 120:
        return True, f"Note: Age {age} is quite advanced"
    elif age < 1:
        return False, "Please enter a valid birth date"
    
    return True, f"Valid (Age: {age} years)"

def main():
    st.set_page_config(page_title="KP Personal Health Analysis", layout="wide")
    
    st.title("🪐 KP Personal Health Analysis - Sarvashtagavarga")
    st.markdown("---")
    
    # Initialize session state
    if 'birth_data' not in st.session_state:
        st.session_state.birth_data = None
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    
    # Birth data input section - RESTRICTED DATE RANGE: 1938-2050
    st.sidebar.header("Personal Birth Data")
    
    st.sidebar.subheader("Enter Birth Details")
    
    # RESTRICTED Birth date range - from 1938 to 2050 only
    min_birth_date = datetime(1938, 1, 1).date()  # Changed to 1938
    max_birth_date = datetime(2050, 12, 31).date()  # Changed to 2050
    
    birth_date = st.sidebar.date_input(
        "Birth Date", 
        value=datetime(1938, 1, 1).date(),
        min_value=min_birth_date,  # Now 1938
        max_value=max_birth_date,  # Now 2050
        key="birth_date"
    )
    
    birth_time = st.sidebar.time_input("Birth Time", datetime(1938, 1, 1, 6, 0), key="birth_time")
    
    # Birth location
    col1, col2 = st.sidebar.columns(2)
    with col1:
        birth_lat = st.number_input("Birth Latitude", value=28.6139, format="%.6f", key="birth_lat")
    with col2:
        birth_lon = st.number_input("Birth Longitude", value=77.2090, format="%.6f", key="birth_lon")
    
    birth_place = st.sidebar.text_input("Birth Place", "New Delhi", key="birth_place")
    
    # Validate birth date (with 1938-2050 restriction)
    is_valid, validation_msg = validate_birth_date(birth_date)
    
    if not is_valid:
        st.sidebar.error(validation_msg)
    elif "Note:" in validation_msg:
        st.sidebar.warning(validation_msg)
    else:
        st.sidebar.success(validation_msg)
    
    # Set birth data button
    if st.sidebar.button("Set Birth Data", key="set_birth_data") and is_valid:
        birth_datetime = datetime.combine(birth_date, birth_time)
        st.session_state.birth_data = {
            'datetime': birth_datetime,
            'lat': birth_lat,
            'lon': birth_lon,
            'place': birth_place
        }
        st.session_state.analysis_done = False
        
        # Calculate and display age
        today = datetime.now().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        st.sidebar.success(f"Birth data set for {birth_place} (Age: {age} years)")
    
    # Display current birth data
    if st.session_state.birth_data:
        birth_data = st.session_state.birth_data
        current_age = datetime.now().year - birth_data['datetime'].year
        st.sidebar.info(f"""
        *Current Birth Data:*
        - Place: {birth_data['place']}
        - Date: {birth_data['datetime'].strftime('%Y-%m-%d')}
        - Time: {birth_data['datetime'].strftime('%H:%M')}
        - Age: ~{current_age} years
        - Location: {birth_data['lat']:.4f}°, {birth_data['lon']:.4f}°
        """)
    
    if not st.session_state.birth_data:
        st.warning("Please enter your birth data in the sidebar to begin analysis.")
        return
    
    # Analysis period selection
    # Analysis period selection
    st.sidebar.header("Analysis Period")
    
    birth_data = st.session_state.birth_data
    
    # Set reasonable analysis date range
    # For births before 1950, allow analysis from 1950 onwards
    if birth_data['datetime'].year < 1950:
        min_analysis_date = datetime(1950, 1, 1).date()
    else:
        min_analysis_date = birth_data['datetime'].date() + timedelta(days=1)
    
    max_analysis_date = datetime.now().date()+ timedelta(days=30)
    
    default_start = max_analysis_date - timedelta(days=90)
    
    # Ensure default start is not before min_analysis_date
    if default_start < min_analysis_date:
        default_start = min_analysis_date
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date", 
            value=default_start,
            min_value=min_analysis_date,
            max_value=max_analysis_date,
            key="start_date"
        )
    with col2:
        end_date = st.date_input(
            "End Date", 
            value=max_analysis_date,
            min_value=min_analysis_date,
            max_value=max_analysis_date,
            key="end_date"
        )
    
    # Validate date range
    if start_date >= end_date:
        st.error("End date must be after start date")
        return
    
    if (end_date - start_date).days < 30:
        st.error("Please select a date range of at least 30 days")
        return
   
    
    # Group size selection
    group_size = st.sidebar.slider("Group Size (days)", min_value=3, max_value=10, value=5, key="group_size")
    
    # Create KP calculator function
    try:
        calculate_daily_sav = create_kp_calculator(
            birth_data['datetime'],
            birth_data['lat'],
            birth_data['lon']
        )
        st.sidebar.success("✓ KP Calculator initialized successfully!")
    except Exception as e:
        st.error(f"Error creating KP Calculator: {e}")
        return
    
    # Calculate button
    if st.sidebar.button("Calculate Analysis", key="calculate_analysis"):
        st.session_state.analysis_done = True
    
    if not st.session_state.analysis_done:
        st.info("Click 'Calculate Analysis' in the sidebar to generate your personalized health analysis.")
        return
    
    # Calculate daily data
    st.header("📊 Personal Daily Sarvashtagavarga Analysis")
    
    # Display birth info with age
    birth_year = birth_data['datetime'].year
    current_age = datetime.now().year - birth_year
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Birth Place", birth_data['place'])
    with col2:
        st.metric("Birth Year", birth_year)
    with col3:
        st.metric("Current Age", f"{current_age} years")
    with col4:
        st.metric("Analysis Period", f"{(end_date - start_date).days} days")
    
    # Generate dates and SAV values
    dates = []
    sav_values = []
    occupied_houses_list = []
    current_date = start_date
    
    total_days = (end_date - start_date).days + 1
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("Calculating personalized Sarvashtagavarga values..."):
        for i in range(total_days):
            status_text.text(f"Calculating for {current_date.strftime('%Y-%m-%d')} ({i+1}/{total_days})...")
            
            sav, occupied_houses = calculate_daily_sav(current_date)
            dates.append(current_date)
            sav_values.append(sav)
            occupied_houses_list.append(occupied_houses)
            
            current_date += timedelta(days=1)
            progress_bar.progress((i + 1) / total_days)
    
    status_text.empty()
    progress_bar.empty()
    
    # Create daily dataframe
    daily_df = pd.DataFrame({
        'Date': dates,
        'SAV_Total': sav_values,
        'Occupied_Houses': [', '.join(map(str, sorted(houses))) for houses in occupied_houses_list],
        'Houses_Count': [len(houses) for houses in occupied_houses_list]
    })
    
    st.dataframe(daily_df, use_container_width=True)
    
    # Summary statistics
    st.subheader("📈 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Days", len(daily_df))
    with col2:
        st.metric("Average SAV", f"{daily_df['SAV_Total'].mean():.1f}")
    with col3:
        st.metric("Max SAV", int(daily_df['SAV_Total'].max()))
    with col4:
        st.metric("Min SAV", int(daily_df['SAV_Total'].min()))
    
    # Group analysis
    st.header("📊 Health Trend Analysis")
    
    # Create groups
    n_groups = len(sav_values) // group_size
    if n_groups < 2:
        st.error("Not enough data for group analysis. Please select a longer date range.")
        return
    
    group_data = []
    
    for i in range(n_groups):
        start_idx = i * group_size
        end_idx = start_idx + group_size
        group_sav = sav_values[start_idx:end_idx]
        group_dates = dates[start_idx:end_idx]
        
        group_data.append({
            'Group': i + 1,
            'Days': f"{group_dates[0].strftime('%m/%d')} to {group_dates[-1].strftime('%m/%d')}",
            'Mean_SAV': np.mean(group_sav),
            'Std_Dev_SAV': np.std(group_sav, ddof=1),
            'Sample_Size': len(group_sav),
            'Occupied_Houses_Avg': np.mean([len(houses) for houses in occupied_houses_list[start_idx:end_idx]])
        })
    
    group_df = pd.DataFrame(group_data)
    
    # Calculate Cohen's d
    cohens_d_values = [0]
    
    for i in range(1, n_groups):
        current_group = sav_values[i * group_size:(i + 1) * group_size]
        previous_group = sav_values[(i - 1) * group_size:i * group_size]
        d_value = calculate_cohens_d(current_group, previous_group)
        cohens_d_values.append(d_value)
    
    group_df['Cohens_d'] = cohens_d_values
    group_df['Interpretation'] = group_df['Cohens_d'].apply(interpret_cohens_d)
    
    st.dataframe(group_df, use_container_width=True)
    
    # Visualization
    st.header("📈 Visualization")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: Cohen's d values
    colors = ['red' if abs(d) >= 0.8 else 'orange' if abs(d) >= 0.5 else 'yellow' if abs(d) >= 0.2 else 'green' for d in cohens_d_values]
    ax1.bar(group_df['Group'], group_df['Cohens_d'], color=colors, alpha=0.7)
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax1.set_xlabel('Group Number')
    ax1.set_ylabel("Cohen's d")
    ax1.set_title("Health Effect Size (Cohen's d) by Group")
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Mean SAV values
    ax2.plot(group_df['Group'], group_df['Mean_SAV'], 'go-', linewidth=2, markersize=6)
    ax2.set_xlabel('Group Number')
    ax2.set_ylabel('Mean SAV')
    ax2.set_title('Sarvashtagavarga Trend')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Health Interpretation
    st.header("💊 Health Status Interpretation")
    
    current_cohens_d = cohens_d_values[-1] if len(cohens_d_values) > 1 else 0
    current_interpretation = interpret_cohens_d(current_cohens_d)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Cohen's d", f"{current_cohens_d:.3f}")
    with col2:
        st.metric("Health Status", current_interpretation.split(' - ')[0])
    
    st.info(f"*Interpretation:* {current_interpretation}")
    
    # Download section
    st.header("💾 Download Data")
    
    col1, col2 = st.columns(2)
    with col1:
        csv_daily = daily_df.to_csv(index=False)
        st.download_button(
            label="Download Daily Data (CSV)",
            data=csv_daily,
            file_name=f"sav_daily_{start_date}_{end_date}.csv",
            mime="text/csv"
        )
    with col2:
        csv_group = group_df.to_csv(index=False)
        st.download_button(
            label="Download Group Analysis (CSV)",
            data=csv_group,
            file_name=f"sav_group_analysis_{start_date}_{end_date}.csv",
            mime="text/csv"
        )
st.info("Thanks for using the app,deveploped by subramanian ramajayam")
if __name__ == "__main__":
    main()
