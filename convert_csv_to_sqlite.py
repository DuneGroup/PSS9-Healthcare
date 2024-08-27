# use this script if you want to download HHS/OCR fresh csv and load into
# sqlite db
import pandas as pd
import sqlite3


# Load the CSV data into a pandas DataFrame
df = pd.read_csv("HHS - breach_report.csv")

# Create a connection to an SQLite database
conn = sqlite3.connect('breach_report.db')
cursor = conn.cursor()

# Write the DataFrame to the SQLite database
df.to_sql('breaches', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
