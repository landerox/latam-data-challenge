# Service Account module

resource "google_service_account" "account" {
  account_id   = var.name
  display_name = var.display_name != "" ? var.display_name : var.name
  description  = var.description != "" ? var.description : var.name
}

resource "google_project_iam_member" "roles" {
  for_each = toset(var.roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.account.email}"
}

resource "google_service_account_key" "key" {
  count              = var.create_key ? 1 : 0
  service_account_id = google_service_account.account.name
}
