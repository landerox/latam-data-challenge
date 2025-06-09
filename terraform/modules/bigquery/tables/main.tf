resource "google_bigquery_table" "big_query_table" {
  dataset_id          = var.dataset_id
  table_id            = var.name_table
  project             = var.project_id
  schema              = var.schema
  deletion_protection = var.deletion_protection
  description         = var.description != "" ? var.description : null
  labels              = var.labels != null ? var.labels : {}

  dynamic "time_partitioning" {
    for_each = var.partition_type != null ? [1] : []
    content {
      type          = var.partition_type
      field         = var.partition_field
      expiration_ms = var.partition_expiration_ms
    }
  }

  require_partition_filter = var.require_partition_filter
  clustering               = var.clustering_fields
  expiration_time          = var.expiration_time
}
