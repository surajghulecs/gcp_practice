from google.cloud import bigquery

# Initialize the BigQuery client
client = bigquery.Client(project="project-f2f5392b-abfa-4181-b85")

dataset_id = "client_analytics"
table_id = "customer_status"

# 1. Explicitly create the dataset first so BigQuery doesn't throw a 404
dataset_ref = client.dataset(dataset_id)
dataset = bigquery.Dataset(dataset_ref)
dataset.location = "US"
client.create_dataset(dataset, exists_ok=True)
print(f"Dataset '{dataset_id}' verified/created successfully.")

# 2. Execute DDL + MERGE (Upsert) query
merge_query = f"""
    CREATE TABLE IF NOT EXISTS `{dataset_id}.{table_id}` (
        customer_id INT64,
        customer_name STRING,
        status STRING,
        updated_at TIMESTAMP
    );

    MERGE `{dataset_id}.{table_id}` T
    USING (
        SELECT 101 AS customer_id, 'Alice Smith' AS customer_name, 'Active' AS status, CURRENT_TIMESTAMP() AS updated_at UNION ALL
        SELECT 102, 'Bob Jones', 'Inactive', CURRENT_TIMESTAMP() UNION ALL
        SELECT 103, 'Charlie Brown', 'Active', CURRENT_TIMESTAMP()
    ) S
    ON T.customer_id = S.customer_id
    
    WHEN MATCHED THEN
      UPDATE SET T.status = S.status, T.updated_at = S.updated_at
      
    WHEN NOT MATCHED THEN
      INSERT (customer_id, customer_name, status, updated_at)
      VALUES (S.customer_id, S.customer_name, S.status, S.updated_at);
"""

print("Executing BigQuery MERGE (Upsert) operation...")
query_job = client.query(merge_query)
query_job.result()  # Wait for BigQuery to finish the job
print("✅ MERGE statement executed successfully!")