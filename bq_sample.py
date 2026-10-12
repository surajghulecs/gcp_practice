from google.cloud import bigquery
client = bigquery.Client(project="project-f2f5392b-abfa-4181-b85")

query = """
    SELECT 
      state, 
      SUM(number) AS total_babies
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE year > 2000
    GROUP BY state
    ORDER BY total_babies DESC
    LIMIT 5;
"""

print("Executing query against BigQuery...")
query_job = client.query(query)  # API request

print("\nTop 5 Results:")
for row in query_job:
    print(f"State: {row['state']}, Total Babies: {row['total_babies']:,}")