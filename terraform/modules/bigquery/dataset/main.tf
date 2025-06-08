# Deploy a BigQuery dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id                 = var.dataset_id
  friendly_name              = var.friendly_name
  location                   = var.dataset_location
  description                = var.description
  delete_contents_on_destroy = var.delete_contents_on_destroy
}
