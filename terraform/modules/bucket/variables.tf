variable "name" {
  description = "Name of the GCS bucket"
  type        = string
}

variable "region" {
  description = "Region for the GCS bucket"
  type        = string
}

variable "force_destroy" {
  description = "Force destroy bucket when not empty"
  type        = bool
  default     = false
}

variable "versioning" {
  description = "Enable object versioning"
  type        = bool
  default     = false
}

variable "labels" {
  description = "Labels to apply to the bucket"
  type        = map(string)
  default     = {}
}

variable "storage_class" {
  description = "Storage class (eg. STANDARD, NEARLINE, COLDLINE, ARCHIVE)"
  type        = string
  default     = "STANDARD"
}

variable "lifecycle_rules" {
  description = "List of lifecycle rules"
  type = list(object({
    action = object({
      type          = string
      storage_class = optional(string)
    })
    condition = object({
      age                   = optional(number)
      created_before        = optional(string)
      with_state            = optional(string)
      matches_storage_class = optional(list(string))
      num_newer_versions    = optional(number)
    })
  }))
  default = []
}
