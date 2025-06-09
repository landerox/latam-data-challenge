output "email" {
  description = "Email address of the created service account"
  value       = google_service_account.account.email
}

output "private_key" {
  description = "Private key of the service account (if created)"
  value       = var.create_key && length(google_service_account_key.key) > 0 ? google_service_account_key.key[0].private_key : null
  sensitive   = true
}
