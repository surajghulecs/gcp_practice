from google.cloud import bigquery

client = bigquery.Client(project="project-f2f5392b-abfa-4181-b85")

# A query filtering by our partition column (updated_at)
query = """
    SELECT customer_id, customer_name, status, updated_at
    FROM `client_analytics.customer_status_optimized`
    WHERE DATE(updated_at) = '2026-10-11'
"""

# Configure the job for a Dry Run (no execution, just validation & estimation)
job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

print("Calculating query cost via dry run...")
query_job = client.query(query, job_config=job_config)

# Print out the results
bytes_to_bill = query_job.total_bytes_billed
bytes_processed = query_job.total_bytes_processed

print(f"\n--- Cost & Performance Estimation ---")
print(f"Bytes to be processed: {bytes_processed:,} bytes")
print(f"Bytes to be billed:    {bytes_to_bill:,} bytes")
print(f"Estimated Cost:        ${(bytes_to_bill / 10**12) * 5.00:.4f} (at standard $5/TB pricing)")