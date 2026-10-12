from google.cloud import bigquery

client = bigquery.Client(project="project-f2f5392b-abfa-4181-b85")
query = "SELECT * FROM `client_analytics.customer_status`"

print("Running query...")
results = client.query(query)

for row in results:
    print(dict(row))