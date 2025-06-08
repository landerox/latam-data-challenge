output "dataset_id" {
  description = "The dataset ID."
  value       = google_bigquery_dataset.dataset.dataset_id
}

output "dataset_self_link" {
  description = "The self link of the dataset."
  value       = google_bigquery_dataset.dataset.self_link
}
