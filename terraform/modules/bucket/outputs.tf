output "bucket_name" {
  description = "Name of the bucket"
  value       = google_storage_bucket.bucket.name
}

output "bucket_url" {
  description = "URL of the bucket"
  value       = "gs://${google_storage_bucket.bucket.name}"
}
