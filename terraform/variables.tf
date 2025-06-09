variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "repository_id" {
  description = "Repository ID"
  type        = string
}

variable "environment" {
  description = "Deployment environment (dev, tst, prd)"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
}

variable "zone" {
  description = "GCP zone"
  type        = string
}

variable "credentials_file" {
  description = "Path to the credentials file"
  type        = string
  default     = ""
}
