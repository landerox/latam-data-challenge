provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = var.credentials_file != "" ? file(var.credentials_file) : null
}

module "challenge_bucket" {
  source        = "./modules/bucket"
  name          = "${var.project_id}-data"
  region        = var.region
  force_destroy = true
  versioning    = true
  labels = {
    env   = var.environment
    owner = "latam-challenge"
  }
}

module "challenge_data_dataset" {
  source                    = "./modules/bigquery/dataset"
  dataset_id                = "challenge_data"
  friendly_name             = "Challenge Data"
  dataset_location          = var.region
  description               = "Dataset for processed data and final results"
  delete_contents_on_destroy = true
}

module "deployment_service_account" {
  source      = "./modules/serviceAccount"
  project_id  = var.project_id
  name        = "sa-deployment"
  description = "Service account for CI/CD deployment"
  roles = [
    "roles/artifactregistry.admin",
    "roles/bigquery.admin",
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/iam.serviceAccountUser",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/run.admin",
    "roles/storage.admin",
    "roles/storage.objectAdmin"
  ]
  create_key  = true
}

module "q1_results_table" {
  source                  = "./modules/bigquery/tables"
  project_id              = var.project_id
  dataset_id              = module.challenge_data_dataset.dataset_id
  name_table              = "q1_results"
  schema                  = file("${path.module}/modules/bigquery/tables/tables_schemas/q1_results.json")
  description             = "Top tweet dates and most active user per date"
  partition_type          = "DAY"
  partition_field         = "ingested_at"
  require_partition_filter = true
  deletion_protection     = false
}

module "q2_results_table" {
  source                  = "./modules/bigquery/tables"
  project_id              = var.project_id
  dataset_id              = module.challenge_data_dataset.dataset_id
  name_table              = "q2_results"
  schema                  = file("${path.module}/modules/bigquery/tables/tables_schemas/q2_results.json")
  description             = "Most used emojis in tweets"
  partition_type          = "DAY"
  partition_field         = "ingested_at"
  require_partition_filter = true
  deletion_protection     = false
}

module "q3_results_table" {
  source                  = "./modules/bigquery/tables"
  project_id              = var.project_id
  dataset_id              = module.challenge_data_dataset.dataset_id
  name_table              = "q3_results"
  schema                  = file("${path.module}/modules/bigquery/tables/tables_schemas/q3_results.json")
  description             = "Most mentioned users in tweets"
  partition_type          = "DAY"
  partition_field         = "ingested_at"
  require_partition_filter = true
  deletion_protection     = false
}
