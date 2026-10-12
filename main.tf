terraform {
  required_version = ">= 1.0.0"
    
  backend "gcs" {
    bucket = "project-f2f5392b-abfa-4181-b85-tfstate"
    prefix = "client-analytics/state"
}
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "project-f2f5392b-abfa-4181-b85"
  region  = "us-central1"
}

resource "google_bigquery_dataset" "client_analytics" {
  dataset_id                 = "client_analytics"
  location                   = "US"
  delete_contents_on_destroy = false
}

resource "google_bigquery_table" "customer_status_tf" {
  dataset_id          = google_bigquery_dataset.client_analytics.dataset_id
  table_id            = "customer_status_tf"
  deletion_protection = false
  description = "Remote state test table"
  time_partitioning {
    type  = "DAY"
    field = "updated_at"
  }

  clustering = ["status", "customer_id"]

  schema = jsonencode([
    { name = "customer_id", type = "INTEGER", mode = "REQUIRED", description = "Unique customer identifier" },
    { name = "customer_name", type = "STRING", mode = "NULLABLE", description = "Customer full name" },
    { name = "status", type = "STRING", mode = "NULLABLE", description = "Account status" },
    { name = "updated_at", type = "TIMESTAMP", mode = "REQUIRED", description = "Timestamp of last status update" },
    { name = "loyalty_tier", type = "STRING", mode = "NULLABLE", description = "Customer loyalty tier" }
  ])
}

resource "google_bigquery_dataset" "enterprise_analytics" {
  dataset_id                  = "enterprise_analytics_ds"
  friendly_name               = "Enterprise Analytics Dataset"
  description                 = "Dataset for client analytics reporting"
  location                    = "US"
  delete_contents_on_destroy  = false
}

