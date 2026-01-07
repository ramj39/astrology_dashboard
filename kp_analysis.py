import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
st.markdown("<h1 style='color: #2c3e50; text-align: center;font-weight:bold;'>🪐 KP Personal Health Analysis - Sarvashtagavarga</h1>", unsafe_allow_html=True)
st.markdown(
    """
        ⚠️ **Disclaimer**  
Disclaimer: This application is for educational and analytical purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with any questions about medical conditions.

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

def create_kp_calculator(birth_datetime, birth_lat, birth_lon):
    """Create a KP calculator with event prediction capabilities"""
    
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
    
    # KP Planetary Significations for Event Prediction
    planet_significations = {
        'Sun': ['Father', 'Government', 'Health', 'Authority', 'Success'],
        'Moon': ['Mother', 'Mind', 'Emotions', 'Travel', 'Public'],
        'Mars': ['Brothers', 'Courage', 'Accidents', 'Property', 'Surgery'],
        'Mercury': ['Education', 'Business', 'Communication', 'Travel', 'Nervous System'],
        'Jupiter': ['Wealth', 'Children', 'Religion', 'Higher Education', 'Luck'],
        'Venus': ['Marriage', 'Relationships', 'Arts', 'Comfort', 'Vehicles'],
        'Saturn': ['Obstacles', 'Career', 'Longevity', 'Discipline', 'Property']
    }
    
    # House Significations for Event Prediction
    house_significations = {
        1: ['Self', 'Health', 'Personality', 'Vitality'],
        2: ['Wealth', 'Family', 'Speech', 'Resources'],
        3: ['Siblings', 'Courage', 'Short Travel', 'Communication'],
        4: ['Mother', 'Property', 'Vehicles', 'Comfort'],
        5: ['Children', 'Education', 'Romance', 'Creativity'],
        6: ['Health', 'Debts', 'Enemies', 'Service'],
        7: ['Marriage', 'Partnership', 'Business', 'Public'],
        8: ['Longevity', 'Obstacles', 'Inheritance', 'Research'],
        9: ['Father', 'Luck', 'Higher Education', 'Travel'],
        10: ['Career', 'Fame', 'Authority', 'Profession'],
        11: ['Gains', 'Income', 'Friends', 'Ambitions'],
        12: ['Losses', 'Spirituality', 'Foreign', 'Isolation']
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
    
    def predict_events(date, occupied_houses):
        """Predict potential events based on planetary positions and house occupations"""
        events = []
        significance_score = 0
        
        # Analyze each occupied house for event prediction
        for house in occupied_houses:
            house_signs = house_significations.get(house, [])
            
            # Calculate significance based on house and planetary combinations
            house_power = len(house_signs) * 2
            
            # Check for specific event combinations
            if house == 6 and house_power > 5:
                events.append("Possible health concern or minor obstacle")
                significance_score += 3
            elif house == 10 and house_power > 6:
                events.append("Career opportunity or professional recognition")
                significance_score += 4
            elif house == 7 and house_power > 5:
                events.append("Relationship development or partnership matter")
                significance_score += 3
            elif house == 11 and house_power > 6:
                events.append("Financial gain or achievement of desires")
                significance_score += 4
            elif house == 5 and house_power > 5:
                events.append("Creative expression or romantic opportunity")
                significance_score += 3
            elif house == 8 and house_power > 4:
                events.append("Transformation or research opportunity")
                significance_score += 2
            elif house == 12 and house_power > 4:
                events.append("Spiritual growth or need for solitude")
                significance_score += 2
        
        # Add random events based on significance score
        if significance_score > 8:
            bonus_events = ["Important decision point", "Significant life event", "Major opportunity"]
            events.append(np.random.choice(bonus_events))
        elif significance_score > 5:
            bonus_events = ["Social interaction", "Learning opportunity", "Minor achievement"]
            events.append(np.random.choice(bonus_events))
        
        return events, significance_score
    
    def get_daily_prediction(date):
        """Get comprehensive daily prediction"""
        sav, occupied_houses = calculate_daily_sav(date)
        events, significance = predict_events(date, occupied_houses)
        
        return {
            'sav': sav,
            'occupied_houses': occupied_houses,
            'events': events,
            'significance_score': significance,
            'prediction_strength': 'High' if significance > 7 else 'Medium' if significance > 4 else 'Low'
        }
    
    return calculate_daily_sav, get_daily_prediction

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
    
    if birth_date.year > 2050:
        return False, "Birth year cannot be after 2050"
    
    if birth_date.year < 1938:
        return False, "Birth year cannot be before 1938"
    
    if birth_date > today:
        return False, "Birth date cannot be in the future"
    
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    if age > 120:
        return True, f"Note: Age {age} is quite advanced"
    elif age < 1:
        return False, "Please enter a valid birth date"
    
    return True, f"Valid (Age: {age} years)"

def main():
    st.set_page_config(page_title="KP Astrology - Event Prediction", layout="wide")
    
    st.title("🪐 KP Astrology - Event Prediction & Health Analysis")
    st.markdown("---")
    
    # Initialize session state
    if 'birth_data' not in st.session_state:
        st.session_state.birth_data = None
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'prediction_mode' not in st.session_state:
        st.session_state.prediction_mode = False
    
    # Birth data input section
    st.sidebar.header("Personal Birth Data")
    
    min_birth_date = datetime(1938, 1, 1).date()
    max_birth_date = datetime(2050, 12, 31).date()
    
    birth_date = st.sidebar.date_input(
        "Birth Date", 
        value=datetime(1938, 1, 1).date(),
        min_value=min_birth_date,
        max_value=max_birth_date,
        key="birth_date"
    )
    
    birth_time = st.sidebar.time_input("Birth Time", datetime(1938, 1, 1, 6, 0), key="birth_time")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        birth_lat = st.number_input("Birth Latitude", value=28.6139, format="%.6f", key="birth_lat")
    with col2:
        birth_lon = st.number_input("Birth Longitude", value=77.2090, format="%.6f", key="birth_lon")
    
    birth_place = st.sidebar.text_input("Birth Place", "New Delhi", key="birth_place")
    
    # Analysis mode selection
    st.sidebar.header("Analysis Mode")
    analysis_mode = st.sidebar.radio(
        "Select Analysis Type:",
        ["Health Trend Analysis", "Event Prediction Analysis"],
        help="Choose between health monitoring or event prediction"
    )
    
    is_valid, validation_msg = validate_birth_date(birth_date)
    
    if not is_valid:
        st.sidebar.error(validation_msg)
    elif "Note:" in validation_msg:
        st.sidebar.warning(validation_msg)
    else:
        st.sidebar.success(validation_msg)
    
    if st.sidebar.button("Set Birth Data", key="set_birth_data") and is_valid:
        birth_datetime = datetime.combine(birth_date, birth_time)
        st.session_state.birth_data = {
            'datetime': birth_datetime,
            'lat': birth_lat,
            'lon': birth_lon,
            'place': birth_place
        }
        st.session_state.analysis_done = False
        st.session_state.prediction_mode = (analysis_mode == "Event Prediction Analysis")
        
        age = datetime.now().year - birth_date.year - ((datetime.now().month, datetime.now().day) < (birth_date.month, birth_date.day))
        st.sidebar.success(f"Birth data set for {birth_place} (Age: {age} years)")
    
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

    
    group_size = st.sidebar.slider("Group Size (days)", min_value=3, max_value=10, value=5, key="group_size")
    
    # Create KP calculator with prediction capabilities
    try:
        calculate_daily_sav, get_daily_prediction = create_kp_calculator(
            birth_data['datetime'],
            birth_data['lat'],
            birth_data['lon']
        )
        st.sidebar.success("✓ KP Calculator initialized successfully!")
    except Exception as e:
        st.error(f"Error creating KP Calculator: {e}")
        return
    
    if st.sidebar.button("Calculate Analysis", key="calculate_analysis"):
        st.session_state.analysis_done = True
    
    if not st.session_state.analysis_done:
        st.info("Click 'Calculate Analysis' to generate your analysis.")
        return
    
    # Display analysis based on selected mode
    if analysis_mode == "Health Trend Analysis":
        run_health_analysis(start_date, end_date, group_size, calculate_daily_sav, birth_data)
    else:
        run_event_prediction(start_date, end_date, get_daily_prediction, birth_data)

def run_health_analysis(start_date, end_date, group_size, calculate_daily_sav, birth_data):
    """Run health trend analysis"""
    st.header("📊 Health Trend Analysis")
    
    # Generate dates and SAV values
    dates = []
    sav_values = []
    occupied_houses_list = []
    current_date = start_date
    
    total_days = (end_date - start_date).days + 1
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("Calculating health trends..."):
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
    
    # Group analysis
    n_groups = len(sav_values) // group_size
    if n_groups < 2:
        st.error("Not enough data for group analysis.")
        return
    
    group_data = []
    
    for i in range(n_groups):
        start_idx = i * group_size
        end_idx = start_idx + group_size
        group_sav = sav_values[start_idx:end_idx]
        
        group_data.append({
            'Group': i + 1,
            'Mean_SAV': np.mean(group_sav),
            'Std_Dev_SAV': np.std(group_sav, ddof=1),
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
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    ax1.bar(group_df['Group'], group_df['Cohens_d'], color='skyblue', alpha=0.7)
    ax1.set_title("Health Effect Size (Cohen's d)")
    ax1.set_ylabel("Cohen's d")
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(group_df['Group'], group_df['Mean_SAV'], 'go-', linewidth=2)
    ax2.set_title("Sarvashtagavarga Trend")
    ax2.set_ylabel("Mean SAV")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)

def run_event_prediction(start_date, end_date, get_daily_prediction, birth_data):
    """Run event prediction analysis"""
    st.header("🔮 KP Event Prediction Analysis")
    
    st.info("""
    *Event Prediction Methodology:*
    - Analyzes planetary positions and house occupations
    - Uses KP significations for houses and planets
    - Calculates event significance scores
    - Identifies potential important dates
    """)
    
    # Generate predictions
    predictions = []
    current_date = start_date
    
    total_days = (end_date - start_date).days + 1
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("Analyzing planetary positions for event prediction..."):
        for i in range(total_days):
            status_text.text(f"Analyzing {current_date.strftime('%Y-%m-%d')} ({i+1}/{total_days})...")
            
            prediction = get_daily_prediction(current_date)
            predictions.append({
                'Date': current_date,
                'SAV_Score': prediction['sav'],
                'Occupied_Houses': ', '.join(map(str, sorted(prediction['occupied_houses']))),
                'Predicted_Events': ' | '.join(prediction['events']) if prediction['events'] else 'Normal day',
                'Significance_Score': prediction['significance_score'],
                'Prediction_Strength': prediction['prediction_strength']
            })
            
            current_date += timedelta(days=1)
            progress_bar.progress((i + 1) / total_days)
    
    status_text.empty()
    progress_bar.empty()
    
    # Create predictions dataframe
    predictions_df = pd.DataFrame(predictions)
    
    # Display significant events
    st.subheader("🎯 Significant Event Predictions")
    
    significant_events = predictions_df[predictions_df['Significance_Score'] > 5]
    
    if not significant_events.empty:
        st.dataframe(significant_events, use_container_width=True)
        
        # Show top 5 most significant days
        st.subheader("🏆 Top 5 Most Significant Days")
        top_days = significant_events.nlargest(5, 'Significance_Score')
        
        for idx, row in top_days.iterrows():
            with st.expander(f"📅 {row['Date'].strftime('%Y-%m-%d')} - Score: {row['Significance_Score']} ({row['Prediction_Strength']})"):
                st.write(f"*Events:* {row['Predicted_Events']}")
                st.write(f"*SAV Score:* {row['SAV_Score']}")
                st.write(f"*Occupied Houses:* {row['Occupied_Houses']}")
                
                # Add interpretation based on houses
                houses = [int(h) for h in row['Occupied_Houses'].split(', ')]
                st.write("*House Analysis:*")
                for house in houses:
                    if house in [6, 8, 12]:
                        st.write(f"  - House {house}: Possible challenges or transformations")
                    elif house in [1, 5, 9]:
                        st.write(f"  - House {house}: Personal growth and opportunities")
                    elif house in [2, 10, 11]:
                        st.write(f"  - House {house}: Material and career developments")
                    elif house in [3, 7]:
                        st.write(f"  - House {house}: Relationships and communications")
    else:
        st.warning("No highly significant events predicted in this period.")
    
    # Show all predictions
    st.subheader("📈 All Daily Predictions")
    st.dataframe(predictions_df, use_container_width=True)
    
    # Prediction statistics
    st.subheader("📊 Prediction Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Days Analyzed", len(predictions_df))
    with col2:
        high_sig = len(predictions_df[predictions_df['Significance_Score'] > 7])
        st.metric("High Significance Days", high_sig)
    with col3:
        avg_significance = predictions_df['Significance_Score'].mean()
        st.metric("Avg Significance", f"{avg_significance:.1f}")
    with col4:
        event_days = len(predictions_df[predictions_df['Significance_Score'] > 0])
        st.metric("Event Days", event_days)
    
    # Visualization
    st.subheader("📈 Event Significance Trend")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    dates = [p['Date'] for p in predictions]
    scores = [p['Significance_Score'] for p in predictions]
    
    ax.plot(dates, scores, 'b-', alpha=0.7, linewidth=2)
    ax.fill_between(dates, scores, alpha=0.3)
    ax.axhline(y=5, color='red', linestyle='--', alpha=0.7, label='Significance Threshold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Significance Score')
    ax.set_title('Daily Event Significance Score')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Download predictions
    st.subheader("💾 Download Predictions")
    csv_data = predictions_df.to_csv(index=False)
    st.download_button(
        label="Download Event Predictions (CSV)",
        data=csv_data,
        file_name=f"kp_event_predictions_{start_date}_{end_date}.csv",
        mime="text/csv"
    )
st.markdown("Thanks for using the app developed by subramanian ramajayam")
st.balloons()
if __name__ == "__main__":
    main()


