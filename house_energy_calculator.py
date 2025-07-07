import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for center alignment and efficiency
st.markdown("""
<style>
    .main > div {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border: 1px solid #e0e0e0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }
    
    .efficiency-badge {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
        box-shadow: 0 4px 20px rgba(0, 184, 148, 0.3);
    }
    
    .tip-card {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #e17055;
        box-shadow: 0 2px 10px rgba(253, 203, 110, 0.3);
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    .stNumberInput > div > div {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    .stTextInput > div > div {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    .section-header {
        text-align: center;
        color: #2d3436;
        font-size: 1.5rem;
        margin: 2rem 0 1rem 0;
        font-weight: 600;
    }
    
    .center-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for efficiency
if 'cal_energy' not in st.session_state:
    st.session_state.cal_energy = 0
if 'appliances_used' not in st.session_state:
    st.session_state.appliances_used = []

# Header
st.markdown("""
<div class="main-header">
    <h1>⚡ Smart Energy Calculator</h1>
    <p>Calculate your household energy consumption efficiently</p>
</div>
""", unsafe_allow_html=True)

# Centered input form
st.markdown('<div class="input-section">', unsafe_allow_html=True)

# Personal Information Section
st.markdown('<h3 class="section-header">📋 Personal Information</h3>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name", placeholder="Enter your name")
    city = st.text_input("City", placeholder="Enter your city")

with col2:
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    area = st.text_input("Area", placeholder="Enter your area")

# Housing Details Section
st.markdown('<h3 class="section-header">🏠 Housing Details</h3>', unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    flat_tenement = st.selectbox("Property Type", ["Flat", "Tenement"])

with col4:
    facility = st.selectbox("Accommodation", ["1BHK", "2BHK", "3BHK"])

# Appliances Section
st.markdown('<h3 class="section-header">🔌 Appliances</h3>', unsafe_allow_html=True)
col5, col6, col7 = st.columns(3)

with col5:
    ac = st.selectbox("Air Conditioner", ["No", "Yes"])
    tv = st.selectbox("Television", ["No", "Yes"])

with col6:
    fridge = st.selectbox("Refrigerator", ["No", "Yes"])
    microwave = st.selectbox("Microwave", ["No", "Yes"])

with col7:
    washing_machine = st.selectbox("Washing Machine", ["No", "Yes"])
    water_heater = st.selectbox("Water Heater", ["No", "Yes"])

st.markdown('</div>', unsafe_allow_html=True)

# Calculate button for efficiency
if st.button("🔍 Calculate Energy Consumption", type="primary", use_container_width=True):
    # Efficient calculation function
    def calculate_energy():
        cal_energy = 0
        appliances_used = []
        
        # Base consumption lookup (more efficient than if-elif)
        base_consumption = {
            "1BHK": 2.4,
            "2BHK": 3.6,
            "3BHK": 4.8
        }
        
        cal_energy += base_consumption.get(facility, 2.4)
        
        # Appliance consumption lookup
        appliance_data = {
            "AC": (ac == "Yes", 3.0),
            "Fridge": (fridge == "Yes", 3.0),
            "Washing Machine": (washing_machine == "Yes", 2.5),
            "Television": (tv == "Yes", 0.5),
            "Microwave": (microwave == "Yes", 1.2),
            "Water Heater": (water_heater == "Yes", 2.0)
        }
        
        for appliance, (is_used, consumption) in appliance_data.items():
            if is_used:
                cal_energy += consumption
                appliances_used.append((appliance, consumption))
        
        return cal_energy, appliances_used, base_consumption[facility]
    
    # Calculate and store in session state
    st.session_state.cal_energy, st.session_state.appliances_used, base_consumption = calculate_energy()
    
    # Display results
    if st.session_state.cal_energy > 0:
        st.markdown('<div class="center-container">', unsafe_allow_html=True)
        
        # Welcome message
        if name:
            st.markdown(f"<h2 style='text-align: center; color: #2d3436;'>Hello {name}! 👋</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: #636e72;'><strong>Location:</strong> {area}, {city} | <strong>Property:</strong> {facility} {flat_tenement}</p>", unsafe_allow_html=True)
        
        # Energy consumption metrics in cards
        st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
        
        daily_cost = st.session_state.cal_energy * 5
        monthly_cost = daily_cost * 30
        annual_cost = daily_cost * 365
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Daily Usage</h3>
            <h2>{st.session_state.cal_energy:.1f} kWh</h2>
            <p>₹{daily_cost:.0f} per day</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Monthly Usage</h3>
            <h2>{st.session_state.cal_energy * 30:.1f} kWh</h2>
            <p>₹{monthly_cost:.0f} per month</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Annual Usage</h3>
            <h2>{st.session_state.cal_energy * 365:.1f} kWh</h2>
            <p>₹{annual_cost:.0f} per year</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Efficiency rating
        def get_efficiency_rating(consumption):
            if consumption < 5:
                return "Excellent 🌟", "#00b894"
            elif consumption < 10:
                return "Good 👍", "#0984e3"
            elif consumption < 15:
                return "Average ⚠️", "#fdcb6e"
            else:
                return "High Usage 🔴", "#e17055"
        
        rating, color = get_efficiency_rating(st.session_state.cal_energy)
        st.markdown(f"""
        <div class="efficiency-badge" style="background: {color};">
            <h3>Energy Efficiency Rating: {rating}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualization section
        if st.session_state.appliances_used:
            st.markdown('<h3 class="section-header">📊 Energy Breakdown</h3>', unsafe_allow_html=True)
            
            # Create efficient visualization
            labels = ["Base Consumption"] + [app[0] for app in st.session_state.appliances_used]
            values = [base_consumption] + [app[1] for app in st.session_state.appliances_used]
            
            fig = px.pie(
                values=values,
                names=labels,
                title="Energy Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Smart tips section
        st.markdown('<h3 class="section-header">💡 Smart Energy Tips</h3>', unsafe_allow_html=True)
        
        # Efficient tip generation
        tips = []
        tip_map = {
            "AC": "🌡️ Set AC to 24°C for optimal efficiency",
            "Fridge": "❄️ Maintain fridge at 3-4°C, freezer at -18°C",
            "Washing Machine": "🧺 Use cold water for washing",
            "Television": "📺 Turn off TV completely, avoid standby mode",
            "Water Heater": "🚿 Use timer switches for water heaters"
        }
        
        for appliance, _ in st.session_state.appliances_used:
            if appliance in tip_map:
                tips.append(tip_map[appliance])
        
        # Add general tips
        tips.extend([
            "💡 Switch to LED bulbs for 75% energy savings",
            "🔌 Unplug electronics when not in use",
            "🌞 Use natural light during daytime"
        ])
        
        # Display tips efficiently
        for i, tip in enumerate(tips[:5]):
            st.markdown(f'<div class="tip-card">{tip}</div>', unsafe_allow_html=True)
        
        # Environmental impact
        st.markdown('<h3 class="section-header">🌍 Environmental Impact</h3>', unsafe_allow_html=True)
        
        col_env1, col_env2 = st.columns(2)
        
        with col_env1:
            co2_emission = st.session_state.cal_energy * 0.82 * 365
            st.metric("Annual CO₂ Emissions", f"{co2_emission:.0f} kg", "Carbon footprint")
        
        with col_env2:
            trees_needed = co2_emission / 22
            st.metric("Trees to offset", f"{trees_needed:.0f} trees", "Plant trees! 🌳")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-top: 2rem; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);">
    <h3>🌟 Start Saving Energy Today!</h3>
    <p>Small changes lead to big savings. Every kWh counts! 💚</p>
</div>
""", unsafe_allow_html=True)