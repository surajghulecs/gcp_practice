import pandas as pd
from google.cloud import bigquery

client = bigquery.Client(project="project-f2f5392b-abfa-4181-b85")
query = "SELECT column_name, data_type FROM `client_analytics.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = 'customer_status_optimized'"

# Convert directly to a DataFrame
df = client.query(query).to_dataframe()

# Print the entire table structure cleanly
print(df)