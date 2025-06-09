output "challenge_bucket_name" {
  description = "Challenge bucket name"
  value       = module.challenge_bucket.bucket_name
}

output "challenge_bucket_url" {
  description = "Challenge bucket URL"
  value       = module.challenge_bucket.bucket_url
}

output "challenge_data_dataset_id" {
  description = "BigQuery dataset ID for processed data"
  value       = module.challenge_data_dataset.dataset_id
}

output "challenge_data_dataset_self_link" {
  description = "BigQuery dataset self link"
  value       = module.challenge_data_dataset.dataset_self_link
}

output "deployment_service_account_email" {
  description = "CI/CD Service Account email"
  value       = module.deployment_service_account.email
}

output "deployment_service_account_key" {
  description = "CI/CD Service Account private key (sensitive)"
  value       = module.deployment_service_account.private_key
  sensitive   = true
}

output "q1_table_id" {
  description = "Fully qualified BigQuery table ID for Q1"
  value       = module.q1_results_table.table_id
}

output "q1_table_name" {
  description = "BigQuery table name for Q1"
  value       = module.q1_results_table.table_name
}

output "q2_table_id" {
  description = "Fully qualified BigQuery table ID for Q2"
  value       = module.q2_results_table.table_id
}

output "q2_table_name" {
  description = "BigQuery table name for Q2"
  value       = module.q2_results_table.table_name
}

output "q3_table_id" {
  description = "Fully qualified BigQuery table ID for Q3"
  value       = module.q3_results_table.table_id
}

output "q3_table_name" {
  description = "BigQuery table name for Q3"
  value       = module.q3_results_table.table_name
}
