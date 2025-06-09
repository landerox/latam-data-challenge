output "table_id" {
  value = google_bigquery_table.big_query_table.id
}

output "table_name" {
  value = google_bigquery_table.big_query_table.table_id
}
