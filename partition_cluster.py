from google.cloud import bigquery

client = bigquery.Client(project="project-f2f5392b-abfa-4181-b85")

dataset_id = "client_analytics"
table_id = "customer_status_optimized"

# Ensure dataset exists
client.create_dataset(bigquery.Dataset(f"project-f2f5392b-abfa-4181-b85.{dataset_id}"), exists_ok=True)

# Optimized DDL with Partitioning and Clustering
optimized_ddl = f"""
    CREATE TABLE IF NOT EXISTS `{dataset_id}.{table_id}` (
        customer_id INT64,
        customer_name STRING,
        status STRING,
        updated_at TIMESTAMP
    )
    PARTITION BY DATE(updated_at)
    CLUSTER BY status, customer_id;
"""

print("Creating partitioned and clustered table...")
client.query(optimized_ddl).result()
print("✅ Optimized table created successfully!")