# Service Account module variables

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "name" {
  description = "Service account name (without domain or project)"
  type        = string
}

variable "description" {
  description = "Service account description"
  type        = string
  default     = ""
}

variable "display_name" {
  description = "Display name for the service account"
  type        = string
  default     = ""
}

variable "roles" {
  description = "List of roles to assign to the service account"
  type        = list(string)
  default     = []
}

variable "create_key" {
  description = "If true, creates and exports a service account key"
  type        = bool
  default     = false
}
