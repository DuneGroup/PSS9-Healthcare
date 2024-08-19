import subprocess
import streamlit as st
import pandas as pd
import plotly.express as px

# Function to start Datasette
def start_datasette():
    subprocess.Popen(["datasette", "breach_report.db"])

# Start Datasette
start_datasette()

# Streamlit app logic (this can be your existing app code)
# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("HHS - breach_report.csv")

data = load_data()

# Streamlit app
st.title("Healthcare Data Breach Analysis")

# Tabs for different features
tab1, tab2 = st.tabs(["Data Visualization", "Datasette Explorer"])

with tab1:
    # Sidebar filters
    st.sidebar.header("Filters")
    state_filter = st.sidebar.multiselect("Select State", data['State'].unique())
    breach_type_filter = st.sidebar.multiselect("Select Breach Type", data['Type of Breach'].unique())

    # Apply filters
    if state_filter:
        data = data[data['State'].isin(state_filter)]
    if breach_type_filter:
        data = data[data['Type of Breach'].isin(breach_type_filter)]

    # Convert 'Breach Submission Date' to datetime format
    data['Breach Submission Date'] = pd.to_datetime(data['Breach Submission Date'])

    # Metric 1: Breaches by State
    st.header("Breaches by State")
    state_counts = data['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']
    fig1 = px.bar(state_counts, x='State', y='Count', title='Number of Breaches by State', labels={'Count': 'Number of Breaches'})
    st.plotly_chart(fig1)

    # Metric 2: Breach Types
    st.header("Breach Types")
    breach_type_counts = data['Type of Breach'].value_counts().reset_index()
    breach_type_counts.columns = ['Type of Breach', 'Count']
    fig2 = px.pie(breach_type_counts, names='Type of Breach', values='Count', title='Distribution of Breach Types')
    st.plotly_chart(fig2)

    # Metric 3: Individuals Affected
    st.header("Number of Individuals Affected")
    affected_over_time = data.groupby('Breach Submission Date')['Individuals Affected'].sum().reset_index()
    fig3 = px.line(affected_over_time, x='Breach Submission Date', y='Individuals Affected', title='Trend of Individuals Affected Over Time', labels={'Individuals Affected': 'Number of Individuals'})
    st.plotly_chart(fig3)

    # Metric 4: Location of Breached Information
    st.header("Location of Breached Information")
    location_counts = data['Location of Breached Information'].value_counts().reset_index()
    location_counts.columns = ['Location of Breached Information', 'Count']
    fig4 = px.bar(location_counts, x='Location of Breached Information', y='Count', title='Location of Breached Information', labels={'Count': 'Number of Breaches'})
    st.plotly_chart(fig4)

    # Metric 5: Breach Submission Trends
    st.header("Breach Submission Trends")
    submission_trends = data.groupby(data['Breach Submission Date'].dt.to_period('M')).size().reset_index(name='Count')
    submission_trends['Breach Submission Date'] = submission_trends['Breach Submission Date'].dt.to_timestamp()
    fig5 = px.line(submission_trends, x='Breach Submission Date', y='Count', title='Trend of Breach Submissions Over Time', labels={'Count': 'Number of Breaches'})
    st.plotly_chart(fig5)

    # Metric 6: Percentage of Reports Received by Entity Type
    st.header("Percentage of Reports Received by Entity Type")
    entity_type_counts = data['Covered Entity Type'].value_counts().reset_index()
    entity_type_counts.columns = ['Covered Entity Type', 'Count']
    fig6 = px.pie(entity_type_counts, names='Covered Entity Type', values='Count', title='Percentage of Reports by Entity Type')
    st.plotly_chart(fig6)

    # Show filtered data
    st.header("Filtered Data")
    st.dataframe(data)

    # Add download option for the filtered data
    st.download_button(
        label="Download Filtered Data as CSV",
        data=data.to_csv(index=False),
        file_name='filtered_breach_data.csv',
        mime='text/csv',
    )

with tab2:
    st.header("Datasette Explorer")
    st.markdown("""
    Explore the dataset in a more interactive and queryable way using Datasette. Below is an embedded view of the Datasette interface.
    """)
    st.markdown("""
    <iframe src="http://localhost:8001" width="1000" height="800"></iframe>
    """, unsafe_allow_html=True)
