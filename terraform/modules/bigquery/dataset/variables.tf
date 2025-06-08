variable "dataset_id" {
  description = "The dataset ID."
  type        = string
}

variable "friendly_name" {
  description = "The friendly name of the dataset."
  type        = string
}

variable "dataset_location" {
  description = "Location for the dataset."
  type        = string
  default     = "US"
}

variable "description" {
  description = "Description of the dataset."
  type        = string
  default     = ""
}

variable "delete_contents_on_destroy" {
  description = "Whether to delete contents on destroy."
  type        = bool
  default     = false
}
