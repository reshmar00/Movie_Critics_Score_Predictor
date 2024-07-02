import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)

# Query to fetch data
query = "SELECT id, movie_title, tomatometer_score, description FROM rotten_tomatoes_info"

# Fetch data into a DataFrame
df = pd.read_sql(query, conn)

# Save DataFrame to CSV locally
df.to_csv('/path/to/local/directory/rotten_tomatoes_data.csv', index=False)

# Close the connection
conn.close()