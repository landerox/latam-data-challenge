variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "dataset_id" {
  type        = string
  description = "ID of the dataset where the table resides"
}

variable "name_table" {
  type        = string
  description = "Name of the BigQuery table"
}

variable "schema" {
  type        = string
  description = "Schema for the BigQuery table (JSON string)"
}

variable "deletion_protection" {
  type        = bool
  default     = true
  description = "Enable or disable deletion protection"
}

variable "partition_type" {
  type        = string
  default     = null
  description = "Type of time partitioning (e.g., DAY)"
}

variable "partition_field" {
  type        = string
  default     = null
  description = "Field used for partitioning"
}

variable "partition_expiration_ms" {
  type        = number
  default     = null
  description = "Expiration time for partitions in milliseconds"
}

variable "require_partition_filter" {
  type        = bool
  default     = false
  description = "Require partition filter for querying the table"
}

variable "description" {
  type        = string
  default     = ""
  description = "Description of the BigQuery table"
}

variable "labels" {
  type        = map(string)
  default     = null
  description = "Labels to apply to the BigQuery table"
}

variable "expiration_time" {
  type        = number
  default     = null
  description = "Timestamp when table expires (ms since epoch)"
}

variable "clustering_fields" {
  type        = list(string)
  default     = null
  description = "Fields used for clustering the BigQuery table"
}
