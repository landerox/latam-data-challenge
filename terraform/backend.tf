terraform {
  backend "gcs" {
    bucket  = "latam-data-challenge-terraform-state" # <- Edit this with your state bucket name
    prefix  = "terraform/state"
  }
}
