import subprocess
import streamlit as st
import pandas as pd
import plotly.express as px

# Function to start Datasette
def start_datasette():
    subprocess.Popen(["datasette", "breach_report.db"])

# Start Datasette
start_datasette()

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("HHS - breach_report.csv")

data = load_data()

# Convert 'Breach Submission Date' to datetime format
data['Breach Submission Date'] = pd.to_datetime(data['Breach Submission Date'], format='%m/%d/%Y')

# Streamlit app
st.title("Healthcare Data Breach Analysis")

# Tabs for different features
tab1, tab2 = st.tabs(["Data Visualization", "Datasette Explorer"])

with tab1:
    # Sidebar filters
    st.sidebar.header("Filters")
    year_filter = st.sidebar.selectbox("Select Year", sorted(data['Breach Submission Date'].dt.year.unique(), reverse=True))
    state_filter = st.sidebar.multiselect("Select State", data['State'].unique())
    breach_type_filter = st.sidebar.multiselect("Select Breach Type", data['Type of Breach'].unique())

    # Apply year filter
    data_filtered = data[data['Breach Submission Date'].dt.year == year_filter]

    # Apply other filters
    if state_filter:
        data_filtered = data_filtered[data_filtered['State'].isin(state_filter)]
    if breach_type_filter:
        data_filtered = data_filtered[data_filtered['Type of Breach'].isin(breach_type_filter)]

    # Calculate YoY percentage change for the selected year
    # not sure if I want to include yet
    yoy = """if year_filter > min(data['Breach Submission Date'].dt.year):
        previous_year = year_filter - 1
        data_previous_year = data[data['Breach Submission Date'].dt.year == previous_year]
        
        # Calculate the number of breaches for each year
        current_year_breaches = len(data_filtered)
        previous_year_breaches = len(data_previous_year)
        
        # Calculate the percentage change
        if previous_year_breaches > 0:
            yoy_change = ((current_year_breaches - previous_year_breaches) / previous_year_breaches) * 100
        else:
            yoy_change = None

        # Display YoY change
        if yoy_change is not None:
            st.header(f"Year-over-Year Change in Breaches ({previous_year} to {year_filter})")
            st.metric(label=f"YoY Percentage Change", value=f"{yoy_change:.2f}%")
        else:
            st.header(f"No data available for {previous_year} to calculate YoY change.")"""

    # Metric 1: Breaches by State
    st.header(f"Breaches by State ({year_filter})")
    state_counts = data_filtered['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']
    fig1 = px.bar(state_counts, x='State', y='Count', title=f'Number of Breaches by State ({year_filter})', labels={'Count': 'Number of Breaches'})
    st.plotly_chart(fig1)

    # Metric 2: Breach Types
    st.header(f"Breach Types ({year_filter})")
    breach_type_counts = data_filtered['Type of Breach'].value_counts().reset_index()
    breach_type_counts.columns = ['Type of Breach', 'Count']
    fig2 = px.pie(breach_type_counts, names='Type of Breach', values='Count', title=f'Distribution of Breach Types ({year_filter})')
    st.plotly_chart(fig2)

    # Metric 3: Individuals Affected
    st.header(f"Number of Individuals Affected ({year_filter})")
    affected_over_time = data_filtered.groupby('Breach Submission Date')['Individuals Affected'].sum().reset_index()
    fig3 = px.line(affected_over_time, x='Breach Submission Date', y='Individuals Affected', title=f'Trend of Individuals Affected Over Time ({year_filter})', labels={'Individuals Affected': 'Number of Individuals'})
    st.plotly_chart(fig3)

    # Metric 4: Location of Breached Information (Bar Chart)
    st.header(f"Location of Breached Information ({year_filter})")
    location_counts = data_filtered['Location of Breached Information'].value_counts().reset_index()
    location_counts.columns = ['Location of Breached Information', 'Count']
    fig4 = px.bar(location_counts, x='Location of Breached Information', y='Count', title=f'Location of Breached Information ({year_filter})', labels={'Count': 'Number of Breaches'})
    st.plotly_chart(fig4)

    # Metric 5: Location of Breached Information (Pie Chart)
    st.header(f"Distribution of Breached Information Locations ({year_filter})")
    fig5 = px.pie(location_counts, names='Location of Breached Information', values='Count', title=f'Distribution of Breached Information Locations ({year_filter})')
    st.plotly_chart(fig5)

    # Metric 6: Breach Submission Trends
    st.header(f"Breach Submission Trends ({year_filter})")
    submission_trends = data_filtered.groupby(data_filtered['Breach Submission Date'].dt.to_period('M')).size().reset_index(name='Count')
    submission_trends['Breach Submission Date'] = submission_trends['Breach Submission Date'].dt.to_timestamp()
    fig6 = px.line(submission_trends, x='Breach Submission Date', y='Count', title=f'Trend of Breach Submissions Over Time ({year_filter})', labels={'Count': 'Number of Breaches'})
    st.plotly_chart(fig6)

    # Metric 7: Percentage of Reports Received by Entity Type
    st.header(f"Percentage of Reports Received by Entity Type ({year_filter})")
    entity_type_counts = data_filtered['Covered Entity Type'].value_counts().reset_index()
    entity_type_counts.columns = ['Covered Entity Type', 'Count']
    fig7 = px.pie(entity_type_counts, names='Covered Entity Type', values='Count', title=f'Percentage of Reports by Entity Type ({year_filter})')
    st.plotly_chart(fig7)

    # Show filtered data
    st.header(f"Filtered Data ({year_filter})")
    st.dataframe(data_filtered)

    # Add download option for the filtered data
    st.download_button(
        label="Download Filtered Data as CSV",
        data=data_filtered.to_csv(index=False),
        file_name=f'filtered_breach_data_{year_filter}.csv',
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
