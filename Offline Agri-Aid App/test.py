import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import os

# Database configuration
db_config = {
    'user': 'root',
    'password': 'ES410_Project',
    'host': '34.34.136.92',
    'database': 'mydb'
}

# Connect to the database
def db_connection():
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        st.sidebar.success("Successfully connected to the database")
    except mysql.connector.Error as error:
        st.sidebar.error(f"Error connecting to MySQL: {error}")
    return conn

# Retrieve data from the database and convert it to a pandas DataFrame
def retrieve_data():
    conn = db_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM soil_measurements"
            cursor.execute(query)
            rows = cursor.fetchall()
            data = pd.DataFrame(rows, columns=['id', 'temperature', 'moisture', 'timestamp'])
            return data
        except mysql.connector.Error as error:
            st.error(f"Failed to retrieve data from MySQL table: {error}")
            return pd.DataFrame()
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
    else:
        st.error("Failed to connect to the database")
        return pd.DataFrame()

# Layout and styling
st.set_page_config(page_title='AgriAid Dashboard', layout='wide')

# Title of the dashboard
st.title('AgriAid Dashboard')
st.markdown("### Monitoring Soil Conditions")

# Retrieve data from the database
data = retrieve_data()

# Drop the rows with NULL values to avoid errors in the chart
data = data.dropna()

# Convert the 'timestamp' column to datetime format for better charting
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Display interactive charts using Plotly
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔥 Temperature Over Time")
    fig_temp = px.line(data, x='timestamp', y='temperature', 
                       title='Temperature Over Time',
                       labels={'temperature': 'Temperature (°C)'})
    fig_temp.update_layout(autosize=True)
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    st.markdown("### 💧 Moisture Over Time")
    fig_moist = px.line(data, x='timestamp', y='moisture', 
                        title='Moisture Over Time',
                        labels={'moisture': 'Moisture (%)'})
    fig_moist.update_layout(autosize=True)
    st.plotly_chart(fig_moist, use_container_width=True)

# Use an expander to hide raw data by default to keep the dashboard clean
with st.expander("View Raw Data", expanded=False):
    st.dataframe(data.style.highlight_null('red'))

# Display key statistics in a more engaging way
st.write("## Key Statistics")
col3, col4 = st.columns(2)

with col3:
    avg_temp = data['temperature'].mean()
    st.metric(label="Average Temperature", value=f"{avg_temp:.2f}°C")

with col4:
    avg_moisture = data['moisture'].mean()
    st.metric(label="Average Moisture", value=f"{avg_moisture:.2f}%")

# Possibly add more statistical summaries, charts, or tables here

# Footer
st.markdown("---")
st.markdown("AgriAid Dashboard | A Streamlit App")