import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap  
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import base64
from io import BytesIO
import requests

# Set page configuration
st.set_page_config(
    page_title="Chelsea FC Performance Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-contrast, vibrant design
st.markdown("""
<style>
    /* Main background and text colors */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Header styling */
    h1 {
        color: #0066cc;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    h2 {
        color: #0066cc;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
        font-size: 1.8rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #333333;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
        font-size: 1.4rem;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }
    
    p {
        color: #333333;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Card styling */
    .card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        padding: 24px;
        margin-bottom: 24px;
        border-top: 5px solid #0066cc;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        padding: 20px;
        margin: 10px;
        text-align: center;
        border-left: 5px solid #0066cc;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Metric value styling */
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        color: #0066cc;
        margin-bottom: 5px;
    }
    
    /* Metric label styling */
    .metric-label {
        font-size: 16px;
        color: #666666;
        font-weight: 500;
    }
    
    /* Navigation styling */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 30px;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 50px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .nav-button {
        background-color: #ffffff;
        color: #0066cc;
        border-radius: 50px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        cursor: pointer;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .nav-button:hover {
        background-color: #0066cc;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,102,204,0.3);
    }
    
    .nav-button.active {
        background-color: #0066cc;
        color: white;
        box-shadow: 0 4px 12px rgba(0,102,204,0.3);
    }
    
    /* Table styling */
    .dataframe-container {
        background-color: #ffffff;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        margin-bottom: 24px;
        border: 1px solid #e6e6e6;
    }
    
    /* Chart container */
    .chart-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        border-top: 5px solid #0066cc;
    }
    
    /* Highlight number */
    .highlight-number {
        font-size: 48px;
        font-weight: 700;
        background: linear-gradient(45deg, #0066cc, #00cc99);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
        line-height: 1;
    }
    
    /* Highlight label */
    .highlight-label {
        font-size: 18px;
        color: #666666;
        text-align: center;
        font-weight: 500;
    }
    
    /* Circle counter */
    .circle-counter {
        width: 140px;
        height: 140px;
        background: linear-gradient(135deg, #0066cc, #00cc99);
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        box-shadow: 0 8px 16px rgba(0,102,204,0.3);
    }
    
    .counter-number {
        font-size: 48px;
        font-weight: 700;
        color: white;
        line-height: 1;
    }
    
    .counter-label {
        font-size: 16px;
        color: white;
        text-transform: uppercase;
        font-weight: 600;
        margin-top: 5px;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #666666;
        font-size: 14px;
        background-color: #f8f9fa;
        border-radius: 12px;
    }
    
    /* Custom tab styling */
    .custom-tabs {
        display: flex;
        overflow-x: auto;
        margin-bottom: 24px;
        background-color: #f8f9fa;
        border-radius: 50px;
        padding: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .custom-tab {
        padding: 12px 24px;
        margin-right: 5px;
        background-color: transparent;
        border-radius: 50px;
        cursor: pointer;
        font-weight: 600;
        color: #666666;
        transition: all 0.3s ease;
    }
    
    .custom-tab:hover {
        background-color: rgba(0,102,204,0.1);
        color: #0066cc;
    }
    
    .custom-tab.active {
        background-color: #0066cc;
        color: white;
        box-shadow: 0 4px 12px rgba(0,102,204,0.3);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #0066cc, #00cc99);
        border-radius: 10px;
    }
    
    /* Status badge styling */
    .status-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 14px;
        color: white;
    }
    
    .status-badge.success {
        background: linear-gradient(90deg, #00cc99, #00b386);
    }
    
    .status-badge.warning {
        background: linear-gradient(90deg, #ffcc00, #ff9900);
    }
    
    .status-badge.danger {
        background: linear-gradient(90deg, #ff6666, #ff3333);
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(45deg, #0066cc, #00cc99);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Animated elements */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease forwards;
    }
    
    /* Player image styling */
    .player-image {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin: 0 auto;
        display: block;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .metric-value {
            font-size: 28px;
        }
        
        .highlight-number {
            font-size: 36px;
        }
        
        .counter-number {
            font-size: 36px;
        }
        
        .circle-counter {
            width: 120px;
            height: 120px;
        }
        
        .player-image {
            width: 100px;
            height: 100px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Function to load data
@st.cache_data
def load_data():
    # Get the directory of the running script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Build full paths to files
    gps_path = os.path.join(script_dir, 'CFC GPS Data.csv')
    physical_path = os.path.join(script_dir, 'CFC Physical Capability Data_.csv')
    recovery_path = os.path.join(script_dir, 'CFC Recovery status Data.csv')
    priority_path = os.path.join(script_dir, 'CFC Individual Priority Areas.csv')
    
    # Check if files exist
    if not os.path.exists(gps_path):
        st.error(f"File not found: {gps_path}")
        st.stop()
    if not os.path.exists(physical_path):
        st.error(f"File not found: {physical_path}")
        st.stop()
    if not os.path.exists(recovery_path):
        st.error(f"File not found: {recovery_path}")
        st.stop()
    if not os.path.exists(priority_path):
        st.error(f"File not found: {priority_path}")
        st.stop()
    
    # Load data
    gps_data = pd.read_csv(gps_path, encoding='latin1')
    physical_data = pd.read_csv(physical_path)
    recovery_data = pd.read_csv(recovery_path)
    priority_data = pd.read_csv(priority_path)
    
    # Convert dates
    gps_data['date'] = pd.to_datetime(gps_data['date'], format='%d/%m/%Y', errors='coerce')
    physical_data['testDate'] = pd.to_datetime(physical_data['testDate'], format='%d/%m/%Y', errors='coerce')
    recovery_data['sessionDate'] = pd.to_datetime(recovery_data['sessionDate'], format='%d/%m/%Y', errors='coerce')
    
    return gps_data, physical_data, recovery_data, priority_data

# Function to create a metric card
def metric_card(label, value, delta=None, prefix="", suffix=""):
    delta_html = f"<div style='color: {'#00cc99' if delta and delta > 0 else '#ff6666' if delta and delta < 0 else '#666666'};'>{delta:+.1f}% vs prev.</div>" if delta else ""
    html = f"""
    <div class="metric-card animate-fade-in">
        <div class="metric-value">{prefix}{value}{suffix}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Function to create a highlight number
def highlight_number(value, label, prefix="", suffix=""):
    html = f"""
    <div class="animate-fade-in">
        <div class="highlight-number">{prefix}{value}{suffix}</div>
        <div class="highlight-label">{label}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Function to create a circle counter
def circle_counter(number, label):
    html = f"""
    <div class="circle-counter animate-fade-in">
        <div class="counter-number">{number}</div>
        <div class="counter-label">{label}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Function to create a card
def create_card(content, title=None):
    title_html = f"<h3>{title}</h3>" if title else ""
    html = f"""
    <div class="card animate-fade-in">
        {title_html}
        {content}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Function to create a chart container
def chart_container(chart_function, title=None):
    st.markdown(f'<div class="chart-container animate-fade-in">', unsafe_allow_html=True)
    if title:
        st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
    chart_function()
    st.markdown('</div>', unsafe_allow_html=True)

# Function to create a status badge
def status_badge(status):
    if status == "Achieved":
        badge_class = "success"
    elif status == "On Track":
        badge_class = "warning"
    else:
        badge_class = "danger"
    
    return f'<span class="status-badge {badge_class}">{status}</span>'

# Function to get player image
def get_player_image(player_name):
    # Dictionary of Chelsea players with their image URLs
    chelsea_players = {
        "Mason Mount": "https://resources.premierleague.com/premierleague/photos/players/250x250/p184341.png",
        "Reece James": "https://resources.premierleague.com/premierleague/photos/players/250x250/p225796.png",
        "Kai Havertz": "https://resources.premierleague.com/premierleague/photos/players/250x250/p219847.png",
        "N'Golo Kanté": "https://resources.premierleague.com/premierleague/photos/players/250x250/p116594.png",
        "Thiago Silva": "https://resources.premierleague.com/premierleague/photos/players/250x250/p51090.png",
        "Raheem Sterling": "https://resources.premierleague.com/premierleague/photos/players/250x250/p103955.png",
        "Ben Chilwell": "https://resources.premierleague.com/premierleague/photos/players/250x250/p172850.png",
        "Christian Pulisic": "https://resources.premierleague.com/premierleague/photos/players/250x250/p176413.png",
        "Mateo Kovačić": "https://resources.premierleague.com/premierleague/photos/players/250x250/p91651.png",
        "Kepa Arrizabalaga": "https://resources.premierleague.com/premierleague/photos/players/250x250/p109745.png"
    }
    
    # Default image if player not found
    default_image = "https://resources.premierleague.com/premierleague/photos/players/250x250/p000000.png"
    
    # Return the player image URL or default if not found
    return chelsea_players.get(player_name, default_image)

# Main application
def main():
    # Load data
    try:
        gps_data, physical_data, recovery_data, priority_data = load_data()
        
        # Sidebar for filters and controls
        with st.sidebar:
            st.image("https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/800px-Chelsea_FC.svg.png", width=100)
            st.markdown("<h2 class='gradient-text'>Chelsea FC</h2>", unsafe_allow_html=True)
            st.markdown("<h3>Performance Insights</h3>", unsafe_allow_html=True)
            
            # Add a player selector
            st.markdown("---")
            st.subheader("Player Selection")
            
            # List of Chelsea players
            chelsea_players = [
                "Mason Mount", "Reece James", "Kai Havertz", "N'Golo Kanté", 
                "Thiago Silva", "Raheem Sterling", "Ben Chilwell", 
                "Christian Pulisic", "Mateo Kovačić", "Kepa Arrizabalaga"
            ]
            
            player_name = st.selectbox("Player Name", chelsea_players)
            
            # Add a season selector
            seasons = sorted(gps_data['season'].unique())
            selected_season = st.selectbox("Season", seasons, index=len(seasons)-1)
            
            # Date filter for GPS data
            st.markdown("---")
            st.subheader("Date Range")
            min_date = gps_data['date'].min().date()
            max_date = gps_data['date'].max().date()
            date_range = st.date_input(
                "Analysis Period",
                [min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
            
            # Add export options
            st.markdown("---")
            st.subheader("Export Data")
            
            # Create CSV download buttons
            csv_gps = gps_data.to_csv(index=False).encode('utf-8')
            csv_physical = physical_data.to_csv(index=False).encode('utf-8')
            csv_recovery = recovery_data.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="Download GPS Data",
                data=csv_gps,
                file_name='chelsea_gps_data.csv',
                mime='text/csv',
            )
            
            st.download_button(
                label="Download Physical Data",
                data=csv_physical,
                file_name='chelsea_physical_data.csv',
                mime='text/csv',
            )
            
            st.download_button(
                label="Download Recovery Data",
                data=csv_recovery,
                file_name='chelsea_recovery_data.csv',
                mime='text/csv',
            )
        
        # Main content
        # Navigation buttons
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            home_button = st.button("🏠 Home", key="home_button")
        with col2:
            gps_button = st.button(" ⚽ Physical Performance", key="gps_button")
        with col3:
            recovery_button = st.button(" 💪 Capabilities & Recovery", key="recovery_button")
        with col4:
            priorities_button = st.button(" 🎯 Priorities & Goals", key="priorities_button")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Determine which page to show
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        
        if home_button:
            st.session_state.current_page = 'home'
        elif gps_button:
            st.session_state.current_page = 'gps'
        elif recovery_button:
            st.session_state.current_page = 'recovery'
        elif priorities_button:
            st.session_state.current_page = 'priorities'
        
        # Display the selected page
        if st.session_state.current_page == 'home':
            display_home_page(gps_data, physical_data, recovery_data, priority_data, player_name, selected_season)
        elif st.session_state.current_page == 'gps':
            display_gps_page(gps_data, date_range, player_name)
        elif st.session_state.current_page == 'recovery':
            display_recovery_page(physical_data, recovery_data, date_range, player_name)
        elif st.session_state.current_page == 'priorities':
            display_priorities_page(priority_data, player_name)
        
        # Add footer
        st.markdown("""
        <div class="footer">
            <p>Chelsea FC Performance Insights Dashboard | Created for Vizathon Challenge</p>
            <p>© 2025 Chelsea Football Club</p>
            <p> By Eskander Bellarbi </p>
        </div>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.write("Please check that all CSV files are present in the same directory as this script.")
        
        # Show file paths for debugging
        script_dir = os.path.dirname(os.path.abspath(__file__))
        st.write(f"Script directory: {script_dir}")
        st.write("Expected files:")
        st.write(f"- {os.path.join(script_dir, 'CFC GPS Data.csv')}")
        st.write(f"- {os.path.join(script_dir, 'CFC Physical Capability Data_.csv')}")
        st.write(f"- {os.path.join(script_dir, 'CFC Recovery status Data.csv')}")
        st.write(f"- {os.path.join(script_dir, 'CFC Individual Priority Areas.csv')}")

# Home page
def display_home_page(gps_data, physical_data, recovery_data, priority_data, player_name, selected_season):
    # Header with player info and season
    st.markdown(f"<h1 class='animate-fade-in'>{player_name} | Performance Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Season: {selected_season}</h2>", unsafe_allow_html=True)
    
    # Player profile section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Player image
        player_image_url = get_player_image(player_name)
        st.markdown(f"""
        <div style="text-align: center;">
            <img src="{player_image_url}" class="player-image animate-fade-in" alt="{player_name}">
            <div class="counter-number" style="color: #0066cc; margin-top: 10px;">Chelsea</div>
            <div class="counter-label" style="color: #666666;">PLAYER</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Player stats in a card
        st.markdown(f"""
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
            <div style="flex: 0 0 48%; margin-bottom: 10px;">
                <strong style="color: #0066cc;"> 🏃‍♂️ Position:</strong> Midfielder
            </div>
            <div style="flex: 0 0 48%; margin-bottom: 10px;">
                <strong style="color: #0066cc;"> 🎂 Age:</strong> 24
            </div>
            <div style="flex: 0 0 48%; margin-bottom: 10px;">
                <strong style="color: #0066cc;"> 📏 Height:</strong> 178 cm
            </div>
            <div style="flex: 0 0 48%; margin-bottom: 10px;">
                <strong style="color: #0066cc;"> ⚖️ Weight:</strong> 74 kg
            </div>
            <div style="flex: 0 0 48%; margin-bottom: 10px;">
                <strong style="color: #0066cc;"> 🦶 Preferred Foot:</strong> Right
            </div>
            <div style="flex: 0 0 48%; margin-bottom: 10px;">
                <strong style="color: #0066cc;"> 🌍 Nationality:</strong> England
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Performance status
        st.markdown('<div class="card animate-fade-in">', unsafe_allow_html=True)
        st.markdown("<h3>Status</h3>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<span class='status-badge success'>Available</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top: 15px;'><strong>Next Match:</strong> Apr 12, 2025</p>", unsafe_allow_html=True)
        st.markdown("<p><strong>Fitness Level:</strong> 92%</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Key metrics row
    st.markdown("<h2 style='text-align: center;'>Performance Summary</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate key metrics
    total_distance = gps_data['distance'].sum() / 1000  # Convert to km
    total_sessions = len(gps_data)
    avg_speed = gps_data['peak_speed'].mean()
    max_speed = gps_data['peak_speed'].max()
    
    with col1:
        metric_card(" 📊 Total Distance", f"{total_distance:.1f}", None, suffix=" km")
    
    with col2:
        metric_card(" 📅 Total Sessions", f"{total_sessions}", None)
    
    with col3:
        metric_card(" 🚀 Avg. Speed", f"{avg_speed:.1f}", None, suffix=" km/h")
    
    with col4:
        metric_card(" ⚡ Max Speed", f"{max_speed:.1f}", None, suffix=" km/h")
    
    # Highlight best performance
    st.markdown("<h2 style='text-align: center;'>Best Performance</h2>", unsafe_allow_html=True)
    
    # Find session with highest distance
    best_session = gps_data.loc[gps_data['distance'].idxmax()]
    best_distance = best_session['distance'] / 1000  # Convert to km
    best_date = best_session['date'].strftime('%d %b %Y')
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        highlight_number(f"{best_distance:.1f}", " 🏅 Best Distance (km)")
    
    with col2:
        st.markdown(f"""
        <div class="card animate-fade-in">
            <h3>Top Performance: {best_date}</h3>
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
                <div style="flex: 0 0 48%; margin-bottom: 10px;">
                    <strong style="color: #0066cc;">Peak Speed:</strong> {best_session['peak_speed']:.1f} km/h
                </div>
                <div style="flex: 0 0 48%; margin-bottom: 10px;">
                    <strong style="color: #0066cc;">Accelerations >3.5:</strong> {best_session['accel_decel_over_3_5']}
                </div>
                <div style="flex: 0 0 48%; margin-bottom: 10px;">
                    <strong style="color: #0066cc;">Distance >21 km/h:</strong> {best_session['distance_over_21']:.1f} m
                </div>
                <div style="flex: 0 0 48%; margin-bottom: 10px;">
                    <strong style="color: #0066cc;">Match:</strong> vs. Manchester United
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance metrics
    st.markdown("<h2 style='text-align: center;'>Performance Trends</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distance trend chart
        def distance_chart():
            recent_data = gps_data.sort_values('date').tail(10)
            fig = px.line(
                recent_data, 
                x='date', 
                y='distance',
                labels={"date": "Date", "distance": "Distance (m)"}
            )
            
            # Customize the chart appearance
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=20, b=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(211,211,211,0.3)'),
            )
            
            # Update line appearance
            fig.update_traces(
                line=dict(width=3, color='#0066cc'),
                mode='lines+markers',
                marker=dict(size=8, color='#0066cc', line=dict(width=2, color='white')),
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        chart_container(distance_chart, " 📈 Distance Trend (Last 10 Sessions)")
    
    with col2:
        # Speed distribution chart
        def speed_chart():
            fig = px.histogram(
                gps_data,
                x='peak_speed',
                nbins=15,
                labels={"peak_speed": "Peak Speed (km/h)", "count": "Number of Sessions"},
                color_discrete_sequence=['#0066cc']
            )
            
            # Customize the chart appearance
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=20, b=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(211,211,211,0.3)'),
                bargap=0.1,
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        chart_container(speed_chart, " 📊 Speed Distribution")
    
    # Recovery and Priorities Overview
    st.markdown("<h2 style='text-align: center;'>Recovery & Priorities</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Recovery status
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div class="highlight-number">92%</div>
            <div class="highlight-label">Recovery Status</div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <div style="flex: 0 0 48%;">
                <strong style="color: #0066cc;">Sleep Quality:</strong>
                <div style="height: 10px; background-color: #f0f0f0; border-radius: 5px; margin-top: 5px;">
                    <div style="height: 100%; width: 85%; background: linear-gradient(90deg, #0066cc, #00cc99); border-radius: 5px;"></div>
                </div>
            </div>
            <div style="flex: 0 0 48%;">
                <strong style="color: #0066cc;">Muscle Soreness:</strong>
                <div style="height: 10px; background-color: #f0f0f0; border-radius: 5px; margin-top: 5px;">
                    <div style="height: 100%; width: 90%; background: linear-gradient(90deg, #0066cc, #00cc99); border-radius: 5px;"></div>
                </div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <div style="flex: 0 0 48%;">
                <strong style="color: #0066cc;">Fatigue Level:</strong>
                <div style="height: 10px; background-color: #f0f0f0; border-radius: 5px; margin-top: 5px;">
                    <div style="height: 100%; width: 75%; background: linear-gradient(90deg, #0066cc, #00cc99); border-radius: 5px;"></div>
                </div>
            </div>
            <div style="flex: 0 0 48%;">
                <strong style="color: #0066cc;">Readiness:</strong>
                <div style="height: 10px; background-color: #f0f0f0; border-radius: 5px; margin-top: 5px;">
                    <div style="height: 100%; width: 95%; background: linear-gradient(90deg, #0066cc, #00cc99); border-radius: 5px;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Priorities overview
        total_priorities = len(priority_data)
        achieved = sum(1 for status in priority_data['Tracking'] if status == 'Achieved')
        on_track = sum(1 for status in priority_data['Tracking'] if status == 'On Track')
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div class="highlight-number">{achieved}/{total_priorities}</div>
            <div class="highlight-label">Priorities Achieved</div>
        </div>
        <div style="margin-bottom: 15px;">
            <strong style="color: #0066cc;">Overall Progress:</strong>
            <div style="height: 10px; background-color: #f0f0f0; border-radius: 5px; margin-top: 5px;">
                <div style="height: 100%; width: {(achieved + on_track * 0.7) / total_priorities * 100}%; background: linear-gradient(90deg, #0066cc, #00cc99); border-radius: 5px;"></div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <div style="flex: 0 0 30%; text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: #0066cc;">{achieved}</div>
                <div style="font-size: 14px; color: #666666;">Achieved</div>
            </div>
            <div style="flex: 0 0 30%; text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: #0066cc;">{on_track}</div>
                <div style="font-size: 14px; color: #666666;">On Track</div>
            </div>
            <div style="flex: 0 0 30%; text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: #0066cc;">{total_priorities - achieved - on_track}</div>
                <div style="font-size: 14px; color: #666666;">In Progress</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Data overview
    st.markdown("<h2 style='text-align: center;'>Data Overview</h2>", unsafe_allow_html=True)
    
    # Create tabs for different data types
    tab1, tab2, tab3, tab4 = st.tabs(["GPS", "Physical Capabilities", "Recovery", "Priorities"])
    
    with tab1:
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(gps_data.head())
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(physical_data.head())
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(recovery_data.head())
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(priority_data)
        st.markdown('</div>', unsafe_allow_html=True)

# GPS page
def display_gps_page(gps_data, date_range, player_name):
    st.markdown("<h1 class='animate-fade-in'> 🏃‍♂️ Physical Performance (GPS)</h1>", unsafe_allow_html=True)
    
    # Player info at top
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Player image
        player_image_url = get_player_image(player_name)
        st.markdown(f"""
        <div style="text-align: center;">
            <img src="{player_image_url}" class="player-image animate-fade-in" alt="{player_name}">
            <div style="font-size: 18px; font-weight: 600; color: #0066cc; margin-top: 10px;">{player_name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>GPS Data Analysis</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>Analysis period: {date_range[0].strftime('%d %b %Y')} to {date_range[1].strftime('%d %b %Y')}</p>", unsafe_allow_html=True)
    
    # Filter data by date
    filtered_gps = gps_data[
        (gps_data['date'].dt.date >= date_range[0]) & 
        (gps_data['date'].dt.date <= date_range[1])
    ]
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics
    total_distance = filtered_gps['distance'].sum() / 1000  # Convert to km
    max_speed = filtered_gps['peak_speed'].max()
    avg_speed = filtered_gps['peak_speed'].mean()
    total_accel = filtered_gps['accel_decel_over_3_5'].sum()
    
    with col1:
        metric_card("Total Distance", f"{total_distance:.1f}", None, suffix=" km")
    
    with col2:
        metric_card("Max Speed", f"{max_speed:.1f}", None, suffix=" km/h")
    
    with col3:
        metric_card("Avg. Speed", f"{avg_speed:.1f}", None, suffix=" km/h")
    
    with col4:
        metric_card("Accelerations >3.5", f"{total_accel:.0f}", None)
    
    # Distance analysis
    st.markdown("<h2 style='text-align: center;'> 📍 Distance Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distance trend chart
        def distance_trend_chart():
            fig = px.line(
                filtered_gps.sort_values('date'),
                x='date',
                y='distance',
                labels={"date": "Date", "distance": "Distance (m)"}
            )
            
            # Add season average reference line
            season_avg = filtered_gps['distance'].mean()
            fig.add_hline(
                y=season_avg,
                line_dash="dash",
                line_color="#ff6666",
                annotation_text=f"Avg: {season_avg:.1f} m",
                annotation_position="bottom right"
            )
            
            # Customize the chart appearance
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=20, b=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(211,211,211,0.3)'),
            )
            
            # Update line appearance
            fig.update_traces(
                line=dict(width=3, color='#0066cc'),
                mode='lines+markers',
                marker=dict(size=8, color='#0066cc', line=dict(width=2, color='white')),
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        chart_container(distance_trend_chart, "Distance Trend")
    
    with col2:
        # Distance by speed zones
        def distance_by_speed_chart():
            fig = px.bar(
                filtered_gps.sort_values('date').tail(10),
                x='date',
                y=['distance_over_21', 'distance_over_24', 'distance_over_27'],
                labels={
                    "date": "Date", 
                    "value": "Distance (m)",
                    "variable": "Speed Zone"
                },
                color_discrete_map={
                    'distance_over_21': '#66b3ff',
                    'distance_over_24': '#0066cc',
                    'distance_over_27': '#004080'
                },
                barmode='stack'
            )
            
            # Customize the chart appearance
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=20, b=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(211,211,211,0.3)'),
                legend_title_text="Speed Zone",
            )
            
            # Update legend labels
            fig.for_each_trace(lambda t: t.update(
                name={
                    'distance_over_21': '21-24 km/h',
                    'distance_over_24': '24-27 km/h',
                    'distance_over_27': '>27 km/h'
                }[t.name]
            ))
            
            st.plotly_chart(fig, use_container_width=True)
        
        chart_container(distance_by_speed_chart, "Distance by Speed Zones (Last 10 Sessions)")
    
    # Speed analysis
    st.markdown("<h2 style='text-align: center;'> 💨 Speed Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Speed trend chart
        def speed_trend_chart():
            fig = px.line(
                filtered_gps.sort_values('date'),
                x='date',
                y='peak_speed',
                labels={"date": "Date", "peak_speed": "Peak Speed (km/h)"}
            )
            
            # Add average line
            avg_speed = filtered_gps['peak_speed'].mean()
            fig.add_hline(
                y=avg_speed,
                line_dash="dash",
                line_color="#ff6666",
                annotation_text=f"Avg: {avg_speed:.1f} km/h",
                annotation_position="bottom right"
            )
            
            # Customize the chart appearance
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=20, b=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(211,211,211,0.3)'),
            )
            
            # Update line appearance
            fig.update_traces(
                line=dict(width=3, color='#0066cc'),
                mode='lines+markers',
                marker=dict(size=8, color='#0066cc', line=dict(width=2, color='white')),
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        chart_container(speed_trend_chart, "Peak Speed Trend")
    
    with col2:
        # Speed vs. distance scatter plot
        def speed_vs_distance_chart():
            fig = px.scatter(
                filtered_gps,
                x='distance',
                y='peak_speed',
                labels={"distance": "Distance (m)", "peak_speed": "Peak Speed (km/h)"},
                color_discrete_sequence=['#0066cc'],
                trendline="ols"
            )
            
            # Customize the chart appearance
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=20, b=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(211,211,211,0.3)'),
            )
            
            # Update marker appearance
            fig.update_traces(
                marker=dict(
                    size=10,
                    opacity=0.7,
                    line=dict(width=1, color='white')
                ),
                selector=dict(mode='markers')
            )
            
            # Update trendline appearance
            fig.update_traces(
                line=dict(color='#ff6666', width=2),
                selector=dict(mode='lines')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        chart_container(speed_vs_distance_chart, "Relationship: Distance vs. Peak Speed")
    
    # Acceleration analysis
    st.markdown("<h2 style='text-align: center;'> 🏎️ Acceleration Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Acceleration trend chart
        def accel_trend_chart():
            fig = px.line(
                filtered_gps.sort_values('date'),
                x='date',
                y=['accel_decel_over_2_5', 'accel_decel_over_3_5', 'accel_decel_over_4_5'],
                labels={
                    "date": "Date", 
                    "value": "Count",
                    "variable": "Intensity"
                },
                color_discrete_map={
                    'accel_decel_over_2_5': '#66b3ff',
                    'accel_decel_over_3_5': '#0066cc',
                    'accel_decel_over_4_5': '#004080'
                }
            )
            
            # Customize the chart appearance
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=20, b=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(211,211,211,0.3)'),
                legend_title_text="Intensity",
            )
            
            # Update legend labels
            fig.for_each_trace(lambda t: t.update(
                name={
                    'accel_decel_over_2_5': '>2.5 m/s²',
                    'accel_decel_over_3_5': '>3.5 m/s²',
                    'accel_decel_over_4_5': '>4.5 m/s²'
                }[t.name]
            ))
            
            st.plotly_chart(fig, use_container_width=True)
        
        chart_container(accel_trend_chart, "Acceleration/Deceleration Trend")
    
    with col2:
        # Acceleration counts bar chart
        def accel_counts_chart():
            accel_data = {
                "Intensity": [">2.5 m/s²", ">3.5 m/s²", ">4.5 m/s²"],
                "Count": [
                    filtered_gps['accel_decel_over_2_5'].sum(),
                    filtered_gps['accel_decel_over_3_5'].sum(),
                    filtered_gps['accel_decel_over_4_5'].sum()
                ]
            }
            
            accel_df = pd.DataFrame(accel_data)
            
            fig = px.bar(
                accel_df,
                x='Intensity',
                y='Count',
                color_discrete_sequence=['#0066cc']
            )
            
            # Customize the chart appearance
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=20, b=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(211,211,211,0.3)'),
            )
            
            # Add data labels
            fig.update_traces(
                texttemplate='%{y:.0f}',
                textposition='outside',
                textfont=dict(family="Helvetica Neue", size=12, color="#0066cc"),
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        chart_container(accel_counts_chart, "Acceleration/Deceleration Counts by Intensity")

# Recovery page
def display_recovery_page(physical_data, recovery_data, date_range, player_name):
    st.markdown("<h1 class='animate-fade-in'>Capabilities & Recovery</h1>", unsafe_allow_html=True)
    
    # Player info at top
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Player image
        player_image_url = get_player_image(player_name)
        st.markdown(f"""
        <div style="text-align: center;">
            <img src="{player_image_url}" class="player-image animate-fade-in" alt="{player_name}">
            <div style="font-size: 18px; font-weight: 600; color: #0066cc; margin-top: 10px;">{player_name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>Physical Capabilities & Recovery Analysis</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>Analysis period: {date_range[0].strftime('%d %b %Y')} to {date_range[1].strftime('%d %b %Y')}</p>", unsafe_allow_html=True)
    
    # Create tabs for different analyses
    tab1, tab2 = st.tabs([" 💪 Physical Capabilities", " 💤 Recovery Status"])
    
    with tab1:
        st.subheader("Physical Capabilities Analysis")
        
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            movement_types = sorted(physical_data['movement'].unique())
            selected_movement = st.multiselect(
                "Movement Type",
                options=movement_types,
                default=movement_types[:3] if len(movement_types) >= 3 else movement_types
            )
        
        with col2:
            expression_types = sorted(physical_data['expression'].unique())
            selected_expression = st.multiselect(
                "Expression Type",
                options=expression_types,
                default=expression_types
            )
        
        # Filter data
        filtered_physical = physical_data[
            (physical_data['movement'].isin(selected_movement)) &
            (physical_data['expression'].isin(selected_expression))
        ]
        
        # Benchmark analysis
        st.markdown("<h3 style='text-align: center;'>Benchmark Analysis</h3>", unsafe_allow_html=True)
        
        benchmark_data = filtered_physical.dropna(subset=['benchmarkPct'])
        
        if not benchmark_data.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Benchmark distribution by movement
                def benchmark_box_chart():
                    fig = px.box(
                        benchmark_data,
                        x='movement',
                        y='benchmarkPct',
                        color='quality',
                        labels={
                            "movement": "Movement Type",
                            "benchmarkPct": "Benchmark (%)",
                            "quality": "Quality"
                        },
                        color_discrete_sequence=['#66b3ff', '#0066cc', '#004080', '#002b55']
                    )
                    
                    # Customize the chart appearance
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=40, r=40, t=20, b=40),
                        xaxis=dict(showgrid=False),
                        yaxis=dict(
                            showgrid=True, 
                            gridcolor='rgba(211,211,211,0.3)',
                            range=[0, 1],
                            tickformat=".0%"
                        ),
                        legend_title_text="Quality",
                    )
                    
                    # Update boxplot appearance
                    fig.update_traces(
                        boxmean=True,
                        jitter=0.3,
                        pointpos=-1.8,
                        boxpoints='all',
                        marker=dict(size=4, opacity=0.7),
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                chart_container(benchmark_box_chart, "Benchmark Distribution by Movement Type")
            
            with col2:
                # Benchmark heatmap
                def benchmark_heatmap():
                    # Create pivot table for heatmap
                    pivot_data = benchmark_data.pivot_table(
                        index='movement',
                        columns='quality',
                        values='benchmarkPct',
                        aggfunc='mean'
                    ).fillna(0)
                    
                    fig = px.imshow(
                        pivot_data,
                        labels=dict(x="Quality", y="Movement Type", color="Benchmark (%)"),
                        color_continuous_scale=["#e6f2ff", "#66b3ff", "#0066cc", "#004080"],
                        text_auto='.0%',
                        aspect="auto"
                    )
                    
                    # Customize the chart appearance
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=40, r=40, t=20, b=40),
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                chart_container(benchmark_heatmap, "Average Benchmark by Movement and Quality")
        else:
            st.warning("No benchmark data available for the selected filters.")
    
    with tab2:
        st.subheader("Recovery Status Analysis")
        
        # Filter recovery data by date
        filtered_recovery = recovery_data[
            (recovery_data['sessionDate'].dt.date >= date_range[0]) & 
            (recovery_data['sessionDate'].dt.date <= date_range[1])
        ]
        
        # Recovery metrics overview
        st.markdown("<h3 style='text-align: center;'>Recovery Metrics Overview</h3>", unsafe_allow_html=True)
        
        # Get numeric recovery data
        recovery_numeric = filtered_recovery.dropna(subset=['value'])
        
        if not recovery_numeric.empty:
            # Category selector
            categories = sorted(recovery_numeric['category'].unique())
            selected_category = st.selectbox(
                "Recovery Category",
                options=categories
            )
            
            # Filter by category
            category_data = recovery_numeric[recovery_numeric['category'] == selected_category]
            
            if not category_data.empty:
                # Create metrics cards for latest values
                latest_data = category_data.sort_values('sessionDate').groupby('metric').last().reset_index()
                
                # Display metrics in columns
                cols = st.columns(min(4, len(latest_data)))
                
                for i, (_, row) in enumerate(latest_data.iterrows()):
                    col_idx = i % len(cols)
                    with cols[col_idx]:
                        metric_card(
                            row['metric'],
                            f"{row['value']:.2f}",
                            None
                        )
                
                # Trend chart for selected category
                st.markdown("<h3 style='text-align: center;'>Recovery Trends</h3>", unsafe_allow_html=True)
                
                def recovery_trend_chart():
                    fig = px.line(
                        category_data.sort_values('sessionDate'),
                        x='sessionDate',
                        y='value',
                        color='metric',
                        labels={
                            "sessionDate": "Date",
                            "value": "Value",
                            "metric": "Metric"
                        },
                        color_discrete_sequence=['#66b3ff', '#0066cc', '#004080', '#002b55', '#ff6666']
                    )
                    
                    # Customize the chart appearance
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=40, r=40, t=20, b=40),
                        xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=True, gridcolor='rgba(211,211,211,0.3)'),
                        legend_title_text="Metric",
                    )
                    
                    # Update line appearance
                    fig.update_traces(
                        mode='lines+markers',
                        marker=dict(size=6, line=dict(width=1, color='white')),
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                chart_container(recovery_trend_chart, f"Recovery Metrics Trend - {selected_category}")
            else:
                st.info(f"No data available for category: {selected_category}")
        else:
            st.warning("No recovery data available for the selected date range.")

# Priorities page
def display_priorities_page(priority_data, player_name):
    st.markdown("<h1 class='animate-fade-in'>Individual Priorities & Goals</h1>", unsafe_allow_html=True)
    
    # Player info at top
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Player image
        player_image_url = get_player_image(player_name)
        st.markdown(f"""
        <div style="text-align: center;">
            <img src="{player_image_url}" class="player-image animate-fade-in" alt="{player_name}">
            <div style="font-size: 18px; font-weight: 600; color: #0066cc; margin-top: 10px;">{player_name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>Individual Priorities & Goals Analysis</h3>", unsafe_allow_html=True)
        st.markdown("<p>Track progress towards performance goals and development priorities</p>", unsafe_allow_html=True)
    
    # Progress overview
    total_priorities = len(priority_data)
    achieved = sum(1 for status in priority_data['Tracking'] if status == 'Achieved')
    on_track = sum(1 for status in priority_data['Tracking'] if status == 'On Track')
    
    overall_progress = (achieved + on_track * 0.7) / total_priorities
    
    # Progress metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        metric_card("Total Priorities", f"{total_priorities}", None)
    
    with col2:
        metric_card("Achieved", f"{achieved}", None)
    
    with col3:
        metric_card("On Track", f"{on_track}", None)
    
    # Overall progress bar
    st.markdown(f"<h3 style='text-align: center;'>Overall Progress: {overall_progress*100:.0f}%</h3>", unsafe_allow_html=True)
    st.progress(overall_progress)
    
    # Priority cards with visual indicators
    st.markdown("<h3 style='text-align: center;'>Current Priorities</h3>", unsafe_allow_html=True)
    
    for i, row in priority_data.iterrows():
        # Determine status badge
        status_html = status_badge(row['Tracking'])
        
        # Create card with custom styling
        st.markdown(f"""
        <div class="card animate-fade-in">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0;">Priority {row['Priority']}: {row['Area']}</h3>
                {status_html}
            </div>
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
                <div style="flex: 0 0 48%; margin-bottom: 10px;">
                    <strong style="color: #0066cc;">Category:</strong> {row['Category']}
                </div>
                <div style="flex: 0 0 48%; margin-bottom: 10px;">
                    <strong style="color: #0066cc;">Performance Type:</strong> {row['Performance Type']}
                </div>
                <div style="flex: 0 0 100%; margin-bottom: 10px;">
                    <strong style="color: #0066cc;">Target:</strong> {row['Target']}
                </div>
                <div style="flex: 0 0 48%; margin-bottom: 10px;">
                    <strong style="color: #0066cc;">Target set:</strong> {row['Target set']}
                </div>
                <div style="flex: 0 0 48%; margin-bottom: 10px;">
                    <strong style="color: #0066cc;">Review Date:</strong> {row['Review Date']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress chart
    st.markdown("<h3 style='text-align: center;'>Goal Progress</h3>", unsafe_allow_html=True)
    
    # Create progress values
    progress_values = []
    for status in priority_data['Tracking']:
        if status == 'Achieved':
            progress_values.append(1.0)
        elif status == 'On Track':
            progress_values.append(0.7)
        else:
            progress_values.append(0.3)
    
    def goal_progress_chart():
        fig = go.Figure()
        
        # Add progress bars
        fig.add_trace(go.Bar(
            x=priority_data['Area'],
            y=progress_values,
            text=[f"{v*100:.0f}%" for v in progress_values],
            textposition='auto',
            marker_color=['#00cc99' if v == 1.0 else '#0066cc' if v == 0.7 else '#ffcc00' for v in progress_values],
            width=0.6
        ))
        
        # Customize the chart appearance
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=20, b=40),
            xaxis=dict(
                title="Area",
                showgrid=False
            ),
            yaxis=dict(
                title="Progress",
                tickvals=[0, 0.25, 0.5, 0.75, 1.0],
                ticktext=["0%", "25%", "50%", "75%", "100%"],
                range=[0, 1],
                showgrid=True,
                gridcolor='rgba(211,211,211,0.3)'
            ),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    chart_container(goal_progress_chart, "Progress Towards Goals")

if __name__ == "__main__":
    main()
