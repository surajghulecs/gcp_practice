# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "projects/project-f2f5392b-abfa-4181-b85/datasets/client_analytics/tables/customer_metrics_summary"
resource "google_bigquery_table" "customer_metrics_summary" {
  clustering               = null
  dataset_id               = "client_analytics"
  deletion_protection      = true
  description              = null
  expiration_time          = 0
  friendly_name            = null
  labels                   = {}
  max_staleness            = null
  project                  = "project-f2f5392b-abfa-4181-b85"
  require_partition_filter = false
  resource_tags            = {}
  schema = jsonencode([{
    name = "customer_id"
    type = "INTEGER"
    }, {
    name = "customer_name"
    type = "STRING"
    }, {
    name = "status"
    type = "STRING"
    }, {
    name = "updated_at"
    type = "TIMESTAMP"
    }, {
    name = "loyalty_tier"
    type = "STRING"
  }])
  table_id = "customer_metrics_summary"
}
