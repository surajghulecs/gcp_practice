from datetime import datetime, timedelta
from airflow.decorators import dag, task
from google.cloud import bigquery

default_args = {
    'owner': 'suraj.ghule',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='client_analytics_pipeline',
    default_args=default_args,
    description='Orchestrated BigQuery ingestion with data quality checks',
    start_date=datetime(2026, 1, 1),
    schedule='@daily',
    catchup=False,
)
def analytics_pipeline():

    @task()
    def setup_dataset_and_table():
        client = bigquery.Client(project="project-f2f5392b-abfa-4181-b85")
        dataset_id = "client_analytics"
        table_id = "customer_status_optimized"
        
        client.create_dataset(bigquery.Dataset(f"project-f2f5392b-abfa-4181-b85.{dataset_id}"), exists_ok=True)
        
        ddl = f"""
            CREATE TABLE IF NOT EXISTS `{dataset_id}.{table_id}` (
                customer_id INT64,
                customer_name STRING,
                status STRING,
                updated_at TIMESTAMP
            )
            PARTITION BY DATE(updated_at)
            CLUSTER BY status, customer_id;
        """
        client.query(ddl).result()
        return "Dataset and Table verified/created."

    @task()
    def run_incremental_merge(setup_status: str):
        client = bigquery.Client(project="project-f2f5392b-abfa-4181-b85")
        dataset_id = "client_analytics"
        table_id = "customer_status_optimized"

        merge_query = f"""
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
        client.query(merge_query).result()
        return "MERGE completed successfully."

    @task()
    def run_data_quality_check(merge_status: str):
        client = bigquery.Client(project="project-f2f5392b-abfa-4181-b85")
        dataset_id = "client_analytics"
        table_id = "customer_status_optimized"

        # Check for duplicate customer_ids (a classic data quality failure)
        dq_query = f"""
            SELECT customer_id, COUNT(*) as cnt
            FROM `{dataset_id}.{table_id}`
            GROUP BY customer_id
            HAVING cnt > 1
        """
        results = list(client.query(dq_query))
        
        if len(results) > 0:
            raise ValueError(f"❌ Data Quality Failed: Found duplicate customer IDs! {results}")
        
        print("✅ Data Quality Passed: No duplicate primary keys found.")
        return "Validation Passed."

    # Define task dependencies
    status = setup_dataset_and_table()
    merge_res = run_incremental_merge(status)
    run_data_quality_check(merge_res)

dag_instance = analytics_pipeline()