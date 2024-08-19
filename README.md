# PSS9-Healthcare

Welcome to **PSS9-Healthcare**, a tool for analyzing healthcare data breaches over the past few years leveraging OCR/HHS annual breach report to congress. This project combines security analytics (maybe) with interactive data exploration to empower users in the healthcare industry.

## Overview

PSS9-Healthcare is designed to provide insights into healthcare data breaches, leveraging both **Streamlit** and **Datasette** for an enhanced user experience. Users can interact with custom dashboards, filter breach data, and conduct detailed queries, all within a unified application.

## Features

- **Interactive Dashboards**: Explore healthcare data breaches with dynamic visualizations built with Streamlit.
- **Custom Filters**: Narrow down breach data by state, type of breach, and more.
- **Datasette Integration**: Dive deeper into the data with SQL-powered queries via an embedded Datasette instance.
- **Comprehensive Analysis**: View trends, patterns, and key statistics related to breaches in the healthcare industry.

## Getting Started

### Prerequisites

- Python 3.x
- Pip (Python package installer)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jwalker/PSS9-Healthcare.git
   cd PSS9-Healthcare
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```  

3. **Prepare the SQLite database:**

   Convert the provided CSV data into an SQLite database (if not already done):

   ```bash
   python convert_csv_to_sqlite.py
   ```

4 **Run the application:**

   ```bash
   streamlit run app.py
   ```

   This will start both the Streamlit app and Datasette, accessible through your web browser.

### Usage

* Streamlit Dashboards: Access the interactive dashboards to filter and visualize healthcare breach data.
* Datasette: Use the embedded Datasette interface for advanced data querying.