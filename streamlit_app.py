"""
Stock Opname Monitoring System - Streamlit Dashboard
Integrated YOLOv8 Detection + LSTM Forecasting

Author: Ivan David (B25B8M113)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import cv2
from PIL import Image
import io
import os
from pathlib import Path
import sqlite3
import pickle

# Deep learning models
from ultralytics import YOLO
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler

# Page configuration
st.set_page_config(
    page_title="Stock Monitoring System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Directories
BASE_DIR = Path('D:/files')
MODELS_DIR = BASE_DIR / 'models'
DATA_DIR = BASE_DIR / 'timeseries_data'
DATABASE = BASE_DIR / 'stock_monitoring.db'

# Create directories
MODELS_DIR.mkdir(exist_ok=True, parents=True)
DATA_DIR.mkdir(exist_ok=True, parents=True)

# Initialize session state
if 'detection_history' not in st.session_state:
    st.session_state.detection_history = []

# Database functions
def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(str(DATABASE))
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            object_count INTEGER NOT NULL,
            confidence_avg REAL
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS stock_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            stock_count INTEGER NOT NULL,
            source TEXT DEFAULT 'manual'
        )
    ''')
    
    conn.commit()
    conn.close()

def save_detection(object_count, confidence_avg):
    """Save detection to database"""
    conn = sqlite3.connect(str(DATABASE))
    c = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    c.execute('''
        INSERT INTO detections (timestamp, object_count, confidence_avg)
        VALUES (?, ?, ?)
    ''', (timestamp, object_count, confidence_avg))
    
    # Also add to stock history
    today = datetime.now().date().isoformat()
    c.execute('''
        INSERT OR REPLACE INTO stock_history (date, stock_count, source)
        VALUES (?, ?, 'detection')
    ''', (today, object_count))
    
    conn.commit()
    conn.close()

def get_stock_history(days=30):
    """Get stock history from database"""
    try:
        conn = sqlite3.connect(str(DATABASE))
        query = f'''
            SELECT date, stock_count, source 
            FROM stock_history 
            ORDER BY date DESC 
            LIMIT {days}
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.sort_values('date')
    except:
        return pd.DataFrame(columns=['date', 'stock_count', 'source'])

def add_manual_stock(date, count):
    """Add manual stock entry"""
    conn = sqlite3.connect(str(DATABASE))
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO stock_history (date, stock_count, source)
        VALUES (?, ?, 'manual')
    ''', (date, count))
    conn.commit()
    conn.close()

# Model loading
@st.cache_resource
def load_yolo_model():
    """Load YOLO model"""
    model_path = MODELS_DIR / 'best.pt'
    if model_path.exists():
        return YOLO(str(model_path))
    return None

@st.cache_resource
def load_lstm_model():
    """Load LSTM model and scaler"""
    model_path = MODELS_DIR / 'lstm_stock_forecasting.h5'
    scaler_path = MODELS_DIR / 'scaler.pkl'
    
    model = None
    scaler = None
    
    if model_path.exists():
        model = keras.models.load_model(str(model_path))
    
    if scaler_path.exists():
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
    
    return model, scaler

# Initialize database
init_db()

# Header
st.markdown('<h1 class="main-header">📊 Stock Opname Monitoring System</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.2em;">Deep Learning for Inventory Management | Ivan David (B25B8M113)</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📋 Navigation")
    page = st.radio("Go to", [
        "📊 Dashboard",
        "🔍 Object Detection",
        "📈 Forecasting",
        "📝 Manual Entry",
        "⚙️ Settings"
    ])
    
    st.markdown("---")
    
    # Model status
    st.subheader("🤖 Model Status")
    yolo_model = load_yolo_model()
    lstm_model, scaler = load_lstm_model()
    
    if yolo_model:
        st.success("✅ YOLOv8 Loaded")
    else:
        st.error("❌ YOLOv8 Not Found")
    
    if lstm_model:
        st.success("✅ LSTM Loaded")
    else:
        st.error("❌ LSTM Not Found")
    
    st.markdown("---")
    st.info("💡 **Tip:** Upload image for detection or view forecasts!")

# Main content based on page selection
if page == "📊 Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Get statistics
    conn = sqlite3.connect(str(DATABASE))
    
    # Total detections
    total_detections = pd.read_sql_query('SELECT COUNT(*) as count FROM detections', conn)['count'][0]
    
    # Latest stock
    latest_stock_df = pd.read_sql_query(
        'SELECT stock_count FROM stock_history ORDER BY date DESC LIMIT 1', 
        conn
    )
    latest_stock = latest_stock_df['stock_count'][0] if len(latest_stock_df) > 0 else 0
    
    # Average stock (30 days)
    avg_stock_df = pd.read_sql_query(
        'SELECT AVG(stock_count) as avg FROM stock_history WHERE date >= date("now", "-30 days")', 
        conn
    )
    avg_stock = avg_stock_df['avg'][0] if avg_stock_df['avg'][0] else 0
    
    # Trend
    recent_avg_df = pd.read_sql_query(
        'SELECT AVG(stock_count) as avg FROM stock_history WHERE date >= date("now", "-7 days")', 
        conn
    )
    recent_avg = recent_avg_df['avg'][0] if recent_avg_df['avg'][0] else avg_stock
    
    previous_avg_df = pd.read_sql_query(
        'SELECT AVG(stock_count) as avg FROM stock_history WHERE date >= date("now", "-14 days") AND date < date("now", "-7 days")', 
        conn
    )
    previous_avg = previous_avg_df['avg'][0] if previous_avg_df['avg'][0] else recent_avg
    
    conn.close()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Detections", f"{total_detections:,}")
    
    with col2:
        st.metric("Current Stock", f"{int(latest_stock):,}")
    
    with col3:
        st.metric("Avg Stock (30d)", f"{avg_stock:.0f}")
    
    with col4:
        trend_delta = ((recent_avg / previous_avg) - 1) * 100 if previous_avg > 0 else 0
        st.metric("Trend (7d)", f"{trend_delta:+.1f}%", delta=f"{trend_delta:.1f}%")
    
    st.markdown("---")
    
    # Stock history chart
    st.subheader("📈 Stock History (Last 30 Days)")
    
    df_history = get_stock_history(30)
    
    if len(df_history) > 0:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_history['date'],
            y=df_history['stock_count'],
            mode='lines+markers',
            name='Stock Count',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Stock Count Over Time",
            xaxis_title="Date",
            yaxis_title="Stock Count",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 No stock history available. Add entries via Detection or Manual Entry.")
    
    # Alerts
    st.subheader("🚨 Alerts")
    
    if latest_stock < avg_stock * 0.7:
        st.warning(f"⚠️ **Low Stock Alert:** Current stock ({int(latest_stock)}) is 30% below average ({avg_stock:.0f})")
    elif latest_stock < avg_stock * 0.5:
        st.error(f"🚨 **Critical Stock:** Current stock ({int(latest_stock)}) is critically low! Immediate reorder recommended.")
    elif latest_stock > avg_stock * 1.3:
        st.info(f"ℹ️ **High Stock:** Current stock ({int(latest_stock)}) is above average. Review ordering schedule.")
    else:
        st.success("✅ Stock levels are normal")

elif page == "🔍 Object Detection":
    st.header("🔍 Object Detection")
    st.write("Upload an image to detect and count objects on shelf")
    
    # Check if model loaded
    yolo_model = load_yolo_model()
    
    if not yolo_model:
        st.error("❌ YOLO model not found. Please place `best.pt` in `D:/files/models/`")
        st.stop()
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    
    col1, col2 = st.columns([1, 1])
    
    if uploaded_file is not None:
        # Display original image
        image = Image.open(uploaded_file)
        
        with col1:
            st.subheader("Original Image")
            st.image(image, use_column_width=True)
        
        # Detection button
        if st.button("🔍 Run Detection", type="primary", use_container_width=True):
            with st.spinner("🔄 Detecting objects..."):
                # Convert PIL to numpy array
                img_array = np.array(image)
                
                # Run detection
                results = yolo_model.predict(
                    source=img_array,
                    conf=0.25,
                    save=False,
                    verbose=False
                )
                
                # Get results
                boxes = results[0].boxes
                object_count = len(boxes)
                
                # Calculate confidence
                if object_count > 0:
                    confidences = boxes.conf.cpu().numpy()
                    avg_confidence = float(np.mean(confidences))
                else:
                    avg_confidence = 0.0
                
                # Annotate image
                annotated = results[0].plot()
                annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                
                # Display results
                with col2:
                    st.subheader("Detection Results")
                    st.image(annotated_rgb, use_column_width=True)
                
                # Metrics
                st.markdown("---")
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    st.metric("🎯 Objects Detected", f"{object_count}")
                
                with metric_col2:
                    st.metric("📊 Avg Confidence", f"{avg_confidence:.2%}")
                
                with metric_col3:
                    st.metric("⏰ Timestamp", datetime.now().strftime("%H:%M:%S"))
                
                # Save to database
                save_detection(object_count, avg_confidence)
                
                st.success(f"✅ Detection complete! Found {object_count} objects with {avg_confidence:.1%} average confidence.")
                
                # Detailed results
                if object_count > 0:
                    with st.expander("📋 Detailed Detection Results"):
                        results_data = []
                        for i, box in enumerate(boxes):
                            bbox = box.xyxy[0].cpu().numpy()
                            conf = float(box.conf[0])
                            results_data.append({
                                'Object': i + 1,
                                'Confidence': f"{conf:.2%}",
                                'BBox': f"({bbox[0]:.0f}, {bbox[1]:.0f}, {bbox[2]:.0f}, {bbox[3]:.0f})"
                            })
                        
                        st.dataframe(pd.DataFrame(results_data), use_container_width=True)

elif page == "📈 Forecasting":
    st.header("📈 Stock Forecasting")
    st.write("Predict future stock levels using historical data")
    
    # Check if model loaded
    lstm_model, scaler = load_lstm_model()
    
    if not lstm_model:
        st.error("❌ LSTM model not found. Please place model files in `D:/files/models/`")
        st.stop()
    
    # Parameters
    col1, col2 = st.columns(2)
    
    with col1:
        forecast_days = st.slider("Forecast Days", min_value=1, max_value=14, value=7)
    
    with col2:
        lookback_days = st.slider("Lookback Window", min_value=7, max_value=60, value=30)
    
    # Get historical data
    df_history = get_stock_history(lookback_days)
    
    if len(df_history) < lookback_days:
        st.warning(f"⚠️ Need at least {lookback_days} days of historical data. Currently have {len(df_history)} days.")
        st.info("💡 **Tip:** Add more data via Object Detection or Manual Entry")
        st.stop()
    
    # Forecast button
    if st.button("🔮 Generate Forecast", type="primary", use_container_width=True):
        with st.spinner("🔄 Generating predictions..."):
            # Prepare data
            stock_values = df_history['stock_count'].values.reshape(-1, 1)
            
            # Scale data
            if scaler is None:
                scaler = MinMaxScaler()
                stock_scaled = scaler.fit_transform(stock_values)
            else:
                stock_scaled = scaler.transform(stock_values)
            
            # Generate predictions
            predictions = []
            current_sequence = stock_scaled[-lookback_days:].reshape(1, lookback_days, 1)
            
            last_date = pd.to_datetime(df_history['date'].max())
            
            for i in range(forecast_days):
                # Predict
                next_pred = lstm_model.predict(current_sequence, verbose=0)
                pred_value = scaler.inverse_transform(next_pred)[0, 0]
                
                # Store
                forecast_date = (last_date + timedelta(days=i+1)).date()
                predictions.append({
                    'Date': forecast_date,
                    'Predicted Stock': int(pred_value)
                })
                
                # Update sequence
                current_sequence = np.append(
                    current_sequence[:, 1:, :],
                    next_pred.reshape(1, 1, 1),
                    axis=1
                )
            
            # Display predictions
            st.success(f"✅ Generated {forecast_days}-day forecast!")
            
            # Create DataFrame
            forecast_df = pd.DataFrame(predictions)
            
            # Visualization
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=df_history['date'],
                y=df_history['stock_count'],
                mode='lines+markers',
                name='Historical',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=forecast_df['Date'],
                y=forecast_df['Predicted Stock'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='#ff6b6b', width=3, dash='dash'),
                marker=dict(size=10, symbol='star')
            ))
            
            # Add vertical line at today
            fig.add_vline(
                x=last_date,
                line_dash="dot",
                line_color="gray",
                annotation_text="Today"
            )
            
            fig.update_layout(
                title=f"{forecast_days}-Day Stock Forecast",
                xaxis_title="Date",
                yaxis_title="Stock Count",
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Forecast table
            st.subheader("📋 Forecast Details")
            st.dataframe(forecast_df, use_container_width=True)
            
            # Business insights
            st.subheader("💡 Business Insights")
            
            avg_forecast = forecast_df['Predicted Stock'].mean()
            min_forecast = forecast_df['Predicted Stock'].min()
            max_forecast = forecast_df['Predicted Stock'].max()
            trend = "Increasing" if forecast_df['Predicted Stock'].iloc[-1] > forecast_df['Predicted Stock'].iloc[0] else "Decreasing"
            
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            
            with insight_col1:
                st.metric("Average Forecast", f"{avg_forecast:.0f}")
            
            with insight_col2:
                st.metric("Range", f"{min_forecast:.0f} - {max_forecast:.0f}")
            
            with insight_col3:
                st.metric("Trend", trend)
            
            # Recommendations
            st.markdown("### 📌 Recommendations")
            st.info(f"""
            - **Reorder Point:** {min_forecast * 0.8:.0f} items
            - **Safety Stock:** {(avg_forecast * 0.2):.0f} items
            - **Weekly Order:** {avg_forecast * forecast_days / 7:.0f} items
            """)

elif page == "📝 Manual Entry":
    st.header("📝 Manual Stock Entry")
    st.write("Manually add or update stock counts")
    
    with st.form("manual_entry"):
        col1, col2 = st.columns(2)
        
        with col1:
            entry_date = st.date_input("Date", value=datetime.now())
        
        with col2:
            stock_count = st.number_input("Stock Count", min_value=0, value=100, step=1)
        
        submitted = st.form_submit_button("💾 Save Entry", type="primary", use_container_width=True)
        
        if submitted:
            add_manual_stock(entry_date.isoformat(), stock_count)
            st.success(f"✅ Added entry: {entry_date} - {stock_count} items")
            st.balloons()
    
    st.markdown("---")
    
    # Show recent entries
    st.subheader("📊 Recent Entries")
    df_history = get_stock_history(10)
    
    if len(df_history) > 0:
        # Add color based on source
        df_display = df_history.copy()
        df_display['Source'] = df_display['source'].apply(
            lambda x: '🤖 Detection' if x == 'detection' else '✍️ Manual'
        )
        df_display = df_display[['date', 'stock_count', 'Source']]
        df_display.columns = ['Date', 'Stock Count', 'Source']
        
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("No entries yet. Add your first entry above!")

elif page == "⚙️ Settings":
    st.header("⚙️ Settings")
    
    st.subheader("📁 Directory Paths")
    st.code(f"""
Base Directory: {BASE_DIR}
Models Directory: {MODELS_DIR}
Database: {DATABASE}
    """)
    
    st.subheader("🤖 Model Information")
    
    yolo_model = load_yolo_model()
    lstm_model, scaler = load_lstm_model()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**YOLOv8 Detection Model**")
        if yolo_model:
            st.success("✅ Model loaded successfully")
            model_path = MODELS_DIR / 'best.pt'
            st.info(f"📄 File: {model_path.name}")
            st.info(f"💾 Size: {model_path.stat().st_size / 1e6:.2f} MB")
        else:
            st.error("❌ Model not found")
            st.warning(f"Please place `best.pt` in: `{MODELS_DIR}`")
    
    with col2:
        st.markdown("**LSTM Forecasting Model**")
        if lstm_model:
            st.success("✅ Model loaded successfully")
            model_path = MODELS_DIR / 'lstm_stock_forecasting.h5'
            st.info(f"📄 File: {model_path.name}")
            st.info(f"💾 Size: {model_path.stat().st_size / 1e6:.2f} MB")
        else:
            st.error("❌ Model not found")
            st.warning(f"Please place model files in: `{MODELS_DIR}`")
    
    st.markdown("---")
    
    st.subheader("💾 Database Statistics")
    
    conn = sqlite3.connect(str(DATABASE))
    
    total_detections = pd.read_sql_query('SELECT COUNT(*) as count FROM detections', conn)['count'][0]
    total_history = pd.read_sql_query('SELECT COUNT(*) as count FROM stock_history', conn)['count'][0]
    
    conn.close()
    
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        st.metric("Total Detections", f"{total_detections:,}")
    
    with stat_col2:
        st.metric("Stock History Records", f"{total_history:,}")
    
    st.markdown("---")
    
    st.subheader("🗑️ Data Management")
    
    if st.button("🔄 Reset Database", type="secondary"):
        if st.checkbox("⚠️ Confirm reset (this will delete all data)"):
            os.remove(DATABASE)
            init_db()
            st.success("✅ Database reset successfully")
            st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Stock Opname Monitoring System</strong></p>
    <p>Ivan David (B25B8M113) | Deep Learning for Inventory Management</p>
    <p>Built with Streamlit + YOLOv8 + LSTM</p>
</div>
""", unsafe_allow_html=True)
