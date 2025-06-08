provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file(var.credentials_file)
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
